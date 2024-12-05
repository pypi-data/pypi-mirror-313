import base64
import json
import os
import sys
from pathlib import Path
from typing import Tuple, Optional, Callable, List
from urllib.parse import urlparse, urlencode, urlunparse

import typer
from requests import RequestException
from rich.progress import Progress, TextColumn, BarColumn, TransferSpeedColumn, TimeRemainingColumn
from tusclient import client
from tusclient.exceptions import TusCommunicationError
from tusclient.storage import filestorage

from bayes.client import dataset_upload_client
from bayes.model.file.bayes_file import BayesFile
from bayes.model.file.openbayes_data import OpenBayesData, OpenBayesDataSettings, OpenBayesDataType
from bayes.model.file.openbayes_ignore import IGNORE_FILE_NAME, IGNORE_CLEANUPS, OpenBayesIgnoreSettings
from bayes.model.file.settings import BayesSettings, BayesEnvConfig
from bayes.usercases import gear_upload_usecase, openbayes_data_usecase
from bayes.usercases.disk_usecase import IgnoreService, DiskService
from bayes.usercases.gear_upload_usecase import is_upload_url_valid, remove_after_upload_success, UPLOAD_DATASET_LIMIT, \
    TUS_STORAGE_FILE
from bayes.utils import Utils


def has_last_upload(did: str, path: str) -> Tuple[bool, Optional[OpenBayesData]]:
    try:
        os.stat(path)
    except OSError as err:
        print(f"Error checking file stat: {err}")
        return False, None

    data_settings = OpenBayesDataSettings(path)
    data, err = data_settings.read_by_cur_user(did)

    # print(f"has_last_upload data: {data}")
    # print(f"has_last_upload err: {err}")
    if data is None:
        return False, None

    if Path(path).is_dir():
        if data is not None and data.has_last_upload() and is_upload_url_valid(data.location, data.token):
            return True, data
    else:
        if data is not None and data.has_last_archived_upload(path) and is_upload_url_valid(data.location, data.token):
            return True, data

    return False, None


def format_metadata(metadata: dict) -> dict:
    formatted_metadata = {}
    for key, value in metadata.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                formatted_metadata[f"{key}.{sub_key}"] = str(sub_value)
        else:
            formatted_metadata[key] = str(value)
    return formatted_metadata


def upload_dataset(path: str, upload_url: str, token: str, callback: bool, wait: bool, retries=0, max_retries=3) -> \
        Tuple[
            bool, Optional[Exception]]:
    if retries > max_retries:
        return False, Exception("Max retries exceeded")

    try:
        my_client = client.TusClient(
            upload_url, headers={
                "Authorization": f"Bearer {token}",
                "X-OpenBayes-Upload-Callback": str(callback).lower(),  # storage service
                "X-OpenBayes-Upload-Wait": str(wait).lower()  # storage service
            }
        )
        # print(f"upload_url :{upload_url}")
        # print(f"upload_dataset my_client headers: {my_client.headers}")
    except RequestException as e:
        print("Error initializing TUS client:", e)
        return False, e

    file_size = os.path.getsize(path)
    # print(f"upload_dataset path:{path}")
    # print(f"file_size:{file_size}")

    url_storage_file = os.path.join(os.path.dirname(path), TUS_STORAGE_FILE)
    storage = filestorage.FileStorage(url_storage_file)
    # print(f"storage :{storage}")

    bayes_file, err = BayesFile.new_file_info_from_file_path(path)
    # print(f"bayes_file:{bayes_file}, err:{err}")
    metadata = {
        "fileids": bayes_file.MD5,
        "filename": bayes_file.Name,
        "filesize": bayes_file.Size,
    }

    # Format metadata properly
    formatted_metadata = format_metadata(metadata)
    # print(f"formatted_metadata: {formatted_metadata}")

    try:
        with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TransferSpeedColumn(),
                TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task("Uploading", total=file_size)
            uploader = my_client.uploader(path,
                                          chunk_size=2 * 1024 * 1024,
                                          store_url=True,
                                          url_storage=storage,
                                          metadata=formatted_metadata)

            while uploader.offset < file_size:
                uploader.upload_chunk()
                # print(f"Uploader initialized: URL={uploader.url}, File Path={uploader.file_path}")
                progress.update(task, completed=uploader.offset)

        print(f"File uploaded successfully: {path}")

        # if os.path.exists(storage_path):
        os.remove(url_storage_file)
        # print(f"Removed filestorage: {url_storage_file}")

        return True, None

    except TusCommunicationError as e:
        if e.status_code == 404 or e.status_code == 502:
            print("Upload resource not found, restarting upload...")
            with open(url_storage_file, 'w') as f:
                f.write('')  # 清空文件内容
            print("Upload resource not found, restarting upload...")
            return upload_dataset(path, upload_url, token, callback, wait, retries + 1, max_retries)
        else:
            print(f"Response status: {e.status_code}")
            print(f"Response body: {e.response_content}")
            return False, e
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False, e


def upload_all_files_in_directory(directory_path: str, upload_url: str, token: str) -> Tuple[
    bool, Optional[Exception], List[str]]:
    if not os.path.isdir(directory_path):
        print(f"The path is not a directory: {directory_path}")
        return False, Exception("Provided path is not a directory"), []

    try:
        OpenBayesIgnoreSettings(Path(directory_path)).load_or_create_default_yaml()
        ignore_file_path = Path(directory_path) / IGNORE_FILE_NAME
        ignore_service = IgnoreService(str(ignore_file_path), IGNORE_CLEANUPS)
        left_files, _, error = ignore_service.left(directory_path)
        # print(f"upload_all_files_in_directory left_files:{left_files},directory_path:{directory_path}")
    except Exception as e:
        # print(f"e:{e}")
        return False, Exception(f"ignore_service left error:{e}"), []

    total_files = len(left_files)
    success_count = 0
    failure_count = 0
    failed_files = []

    # 遍历所有文件并上传
    for i, file_path in enumerate(left_files):
        print(f"Uploading file: {file_path}")
        # 根据是否是最后一个文件设置callback和wait参数
        # is_last_file = (i == total_files - 1)
        success, err = upload_dataset(file_path, upload_url, token, callback=True, wait=True)
        # success, err = upload_dataset(file_path, base_upload_url, token)
        if success:
            success_count += 1
        else:
            failure_count += 1
            failed_files.append(file_path)
            print(f"Failed to upload {file_path}: {err}")

    print(f"Upload complete with {success_count} successes and {failure_count} failures.")
    if failure_count > 0:
        return False, Exception(f"{failure_count} files failed to upload.failed_files:{failed_files}"), failed_files
    return True, None, failed_files


def uploadWith(data: OpenBayesData) -> Tuple[bool, Exception]:
    try:
        if os.path.isdir(Path(data.zip)):
            success, err, failed_files = upload_all_files_in_directory(data.zip, data.location, data.token)
        else:
            success, err = upload_dataset(data.zip, data.location, data.token, True, True)
        if success:
            print("正在进行清理工作")
            remove_after_dataset_upload_success(data.path, data.did)
            return True, None
        else:
            return False, err
    except Exception as e:
        return False, e


def pre_upload(path, did, process: Callable) -> Tuple[Optional[OpenBayesData], Optional[Exception]]:
    try:
        stat = os.stat(path)
    except OSError as e:
        print(f"获取文件信息失败")
        return None, e

    if not os.path.isdir(path):
        # 如果 path 不是目录，则处理单个文件
        try:
            data_file_path = openbayes_data_usecase.write_file(path, OpenBayesDataType.DATASET, did)
        except Exception as e:
            print(str(e))
            return None, e
    else:
        # 如果 path 是目录，则处理整个目录
        process("正在读取文件列表，请稍候...")

        OpenBayesIgnoreSettings(Path(path)).load_or_create_default_yaml()
        ignore_file_path = Path(path) / IGNORE_FILE_NAME
        ignore_service = IgnoreService(str(ignore_file_path), IGNORE_CLEANUPS)
        disk_service = DiskService(ignore_service)
        files, total_bytes, err = disk_service.directory_computing(path, UPLOAD_DATASET_LIMIT)
        if err is not None:
            return None, err

        process("剔除在 .openbayesignore 中忽略的文件及文件夹...")
        total_megabytes = total_bytes / (1024 * 1024)
        process(f"共有文件 {files} 个，文件大小 {total_megabytes} MB")

        try:
            data_file_path, err = openbayes_data_usecase.write_file(path, OpenBayesDataType.DATASET, did)
            # print(f"data_file_path is :{data_file_path}, err:{err}")
        except Exception as e:
            print(str(e))
            return None, e

    data_settings = OpenBayesDataSettings(path)
    openbayes_data, err = data_settings.read_by_cur_user(did)
    if openbayes_data is not None:
        data, err = openbayes_data_usecase.update_by_cur_user(
            data_file_path, did, openbayes_data.location, openbayes_data.token, path, stat.st_size
        )
        # print(f"data:{data}")
        if err is not None:
            return None, err

    print("正在向服务器发送上传请求...")
    # 向 api server 发送 /datasets/upload-request 请求
    req, err = dataset_upload_client.upload_request(did)
    if err is not None:
        return None, err

    print("服务器已响应")
    print("正在初始化上传中...")

    data_settings = OpenBayesDataSettings(path)
    openbayes_data, err = data_settings.read_by_cur_user(did)
    # print(f"openbayes_data:{openbayes_data},req:{req}")

    default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
    location = f"{default_env.endpoint}/storages/datasets/v2"
    print(f"定义 openbayes data upload location 为:{location}")

    data, err = openbayes_data_usecase.update_by_cur_user(
        data_file_path, did, location, req.token, openbayes_data.zip, openbayes_data.length
    )
    # print(f"update_by_cur_user err:{err}")
    if err is not None:
        return None, err

    return data, None


def clear_dataset_last_upload(data: OpenBayesData):
    if data:
        print(f"OpenBayesDataSettings(data.path):{OpenBayesDataSettings(data.path)}")
        settings = OpenBayesDataSettings(data.path)
        settings.remove_by_cur_user(data.pid or data.did)


def upload(id, dataset_path):
    isExist, data = has_last_upload(id, dataset_path)

    if isExist and data is not None:
        print("OpenBayes 数据集上传")
        is_continuing = typer.prompt("存在一个尚未完成的上传，是否需要继续？ [y/N]")
        if is_continuing.lower() in ("y", "yes"):
            print(
                f"正在上传。总共上传大小：{Utils.byte_size(data.length, True)}"
            )
            success, err = uploadWith(data)
            if success and err is None:
                print(f"数据集 {id} 上传成功")
                sys.exit(1)
            else:
                print(f"数据集 {id} 上传失败: {err}")
                sys.exit(1)

    clear_dataset_last_upload(data)

    data, err = pre_upload(dataset_path, id, lambda s: print(s))
    if err is not None or data is None:
        print(f"pre_upload err:{err}, data is: {data}")
        sys.exit(1)

    is_success, err = uploadWith(data)
    if is_success and err is None:
        print("数据集上传成功")
    else:
        print(f"上传失败: {err}")
        sys.exit(1)


def print_url_storage_file_contents(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
            print(f"Contents of {file_path}: {contents}")
    except Exception as e:
        print(f"Failed to read {file_path}: {e}")


def remove_after_dataset_upload_success(data_file_path, pid):
    # print("remove after dataset upload success")
    err = openbayes_data_usecase.remove_by_cur_user(data_file_path, pid)
    if err is None:
        print(f"清理完成")
    else:
        print(f"清理失败，错误如下:{err}")
