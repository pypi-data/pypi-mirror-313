import os
import sys
from pathlib import Path
from typing import Tuple, Optional, Callable

import typer

from bayes.client import dataset_merge_client
from bayes.model.file.openbayes_data import OpenBayesData, OpenBayesDataSettings, OpenBayesDataType
from bayes.model.file.openbayes_ignore import OpenBayesIgnoreSettings, IGNORE_FILE_NAME, IGNORE_CLEANUPS
from bayes.model.file.settings import BayesSettings, BayesEnvConfig
from bayes.usercases import openbayes_data_usecase
from bayes.usercases.dataset_upload_usecase import clear_dataset_last_upload, upload_all_files_in_directory, \
    upload_dataset, remove_after_dataset_upload_success
from bayes.usercases.disk_usecase import IgnoreService, DiskService
from bayes.usercases.gear_upload_usecase import is_upload_url_valid, UPLOAD_DATASET_LIMIT
from bayes.utils import Utils


def has_last_merge(did: str, path: str) -> Tuple[bool, Optional[OpenBayesData]]:
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
        if data is not None and data.has_last_upload():
            return True, data
    else:
        if data is not None and data.has_last_archived_upload(path):
            return True, data

    return False, None


def pre_merge(did: str, version: str, directory: str, path: str, process: Callable) -> Tuple[
    Optional[OpenBayesData], Optional[Exception]]:
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

    print("正在向服务器发送合并请求...")
    # 向 api server 发送 /datasets/{dataset_id}/versions/{version}/upload-request 请求
    req, err = dataset_merge_client.merge_dataset_request(did, version, directory)
    if err is not None:
        return None, err

    print("服务器已响应")
    print("正在初始化上传中...")

    data_settings = OpenBayesDataSettings(path)
    openbayes_data, err = data_settings.read_by_cur_user(did)
    # print(f"openbayes_data:{openbayes_data},req:{req}")

    default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
    location = f"{default_env.endpoint}/storages/datasets/merge/v2"
    print(f"定义 openbayes data merge location 为:{location}")

    data, err = openbayes_data_usecase.update_by_cur_user(
        data_file_path, did, location, req.token, openbayes_data.zip, openbayes_data.length
    )
    # print(f"update_by_cur_user err:{err}")
    if err is not None:
        return None, err

    return data, None


def mergeWith(did: str, version: str, directory: str, data: OpenBayesData) -> Tuple[bool, Exception]:
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


def merge(did: str, abd_dataset_path: str, version: str, directory: str):
    is_exist, data = has_last_merge(did, abd_dataset_path)
    if is_exist and data is not None:
        print("OpenBayes 数据集上传")
        is_continuing = typer.prompt("存在一个尚未完成合并的上传，是否需要继续？ [y/N]")
        if is_continuing.lower() in ("y", "yes"):
            print(f"正在合并。总共合并大小：{Utils.byte_size(data.length, True)}")
            mergeWith(did, version, directory, data)
            sys.exit(1)

    clear_dataset_last_upload(data)

    data, err = pre_merge(did, version, directory, abd_dataset_path, lambda s: print(s))
    if err is not None or data is None:
        print(f"pre_merge err:{err}, data is: {data}")
        sys.exit(1)

    mergeWith(did, version, directory, data)
