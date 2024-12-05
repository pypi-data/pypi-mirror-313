import logging
import os
import base64
import json
from pathlib import Path
from typing import Optional, Tuple, Callable

import requests
from tusclient import client
from tusclient.storage import filestorage
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
)
from tusclient.exceptions import TusCommunicationError

from bayes.error import request_failed
from bayes.client.job_upload_client import RequestUploadUrl
from bayes.model.file.settings import BayesSettings
from bayes.model.file.openbayes_data import (
    OpenBayesData,
    OpenBayesDataSettings,
    OpenBayesDataType,
    DATA_FILE_NAME,
)
from bayes.model.file.openbayes_ignore import IGNORE_FILE_NAME, IGNORE_CLEANUPS
from bayes.usercases import openbayes_data_usecase, archive_usecase
from bayes.usercases.disk_usecase import IgnoreService, DiskService
from bayes.utils import Utils

UPLOAD_PART_SIZE = 268435456  # -1 or 0 means unlimited
UPLOAD_CODE_LIMIT = 500  # 500MB
TUS_STORAGE_FILE = ".tus_storage"
UPLOAD_DATASET_LIMIT = 512000  # 512000 MB


def upload_request() -> Tuple[Optional[RequestUploadUrl], Optional[Exception]]:
    default_env = BayesSettings().default_env
    url = f"{default_env.endpoint}/api/users/{default_env.username}/jobs/upload-request?protocol=tusd"
    # print(f"upload_request url:{url}")
    auth_token = default_env.token

    try:
        response = requests.post(url, headers={"Authorization": f"Bearer {auth_token}"})
    except requests.RequestException as e:
        return None, e

    logging.info(response)

    if response.status_code != 200:
        err = request_failed(response.status_code)
        return None, err

    try:
        result = response.json()
        upload_request = RequestUploadUrl(**result)
        return upload_request, None
    except ValueError as e:
        return None, e


def _upload_file(
        file_path: str, upload_url: str, token: str, retries=0, max_retries=3
) -> Tuple[bool, Optional[str], Optional[Exception]]:
    print(f"_upload_file file_path:{file_path},upload_url:{upload_url},token:{token}")
    if retries > max_retries:
        return False, None, Exception("Max retries exceeded")

    try:
        my_client = client.TusClient(upload_url, headers={"Authorization": f"Bearer {token}"})
        file_size = os.path.getsize(file_path)
        url_storage_file = os.path.join(os.path.dirname(file_path), TUS_STORAGE_FILE)
        storage = filestorage.FileStorage(url_storage_file)
        metadata = {"filename": os.path.basename(file_path)}

        with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TransferSpeedColumn(),
                TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task("Uploading", total=file_size)
            uploader = my_client.uploader(file_path,
                                          chunk_size=2 * 1024 * 1024,
                                          store_url=True,
                                          url_storage=storage,
                                          metadata=metadata)
            print(f"Uploader initialized: URL={uploader.url}, File Path={uploader.file_path}")
            while uploader.offset < file_size:
                uploader.upload_chunk()
                print(f"Uploader initialized: URL={uploader.url}, File Path={uploader.file_path}")
                progress.update(task, completed=uploader.offset)

        # print(f"File uploaded successfully: {file_path}")
        print_url_storage_file_contents(url_storage_file)
        os.remove(url_storage_file)
        # print(f"Removed filestorage: {url_storage_file}")

        payload_part = token.split(".")[1]
        padded_payload = payload_part + "=" * (4 - len(payload_part) % 4)
        decoded_payload = base64.urlsafe_b64decode(padded_payload).decode("utf-8")
        payload_data = json.loads(decoded_payload)
        sub_payload = json.loads(payload_data["sub"])["payload"]

        return True, sub_payload, None

    except TusCommunicationError as e:
        print(f"TUS Communication Error: {e}")
        if e.status_code == 404:
            print("Upload resource not found, restarting upload...")
            with open(url_storage_file, 'w') as f:
                f.write('')  # 清空文件内容
            print("Upload resource not found, restarting upload...")
            return _upload_file(file_path, upload_url, token, retries + 1, max_retries)
        else:
            print(f"Response status: {e.status_code}")
            print(f"Response body: {e.response_content}")
            return False, None, e
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False, None, e


def upload_file(
        file_path: str, upload_url: str, token: str
) -> Tuple[bool, Optional[str], Optional[Exception]]:
    return _upload_file(file_path, upload_url, token)


def remove_after_upload_success(zip_path, data_file_path, pid):
    logging.debug("remove after upload success")
    if os.path.exists(zip_path):
        os.remove(zip_path)
    openbayes_data_usecase.remove_by_cur_user(data_file_path, pid)


def has_last_upload(path: str, pid: str) -> Tuple[bool, Optional[OpenBayesData]]:
    data_settings = OpenBayesDataSettings(path)
    data, err = data_settings.read_by_cur_user(pid)
    if data is None:
        return False, None

    print(f"has_last_upload data.has_last_upload():{data.has_last_upload()}")

    if data.has_last_upload():
        # Check if the zip file still exists
        if os.path.exists(data.zip):
            # Check if the upload URL is still valid
            print(f"is_upload_url_valid(data.location, data.token):{is_upload_url_valid(data.location, data.token)}")
            if is_upload_url_valid(data.location, data.token):
                return True, data

    return False, None


def is_upload_url_valid(upload_url: str, token: str) -> bool:
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.head(upload_url, headers=headers)
        print(f"is_upload_url_valid response.status_code:{response.status_code}")
        if response.status_code != 200:
            err = request_failed(response.status_code)
            print(str(err))
            return False
        return True
    except requests.RequestException as e:
        print(f"is_upload_url_valid error: {e}")
        return False


# Update the upload function to support resuming
def upload(data: OpenBayesData):
    success, payload, err = _upload_file(data.zip, data.location, data.token)
    if success:
        remove_after_upload_success(data.zip, data.path, data.pid)
    return data.length if success else 0, payload, err


def clear_last_upload(data: OpenBayesData):
    if data:
        try:
            os.remove(data.zip)
        except FileNotFoundError:
            print(f"zip_path:{data.zip} not found")

        print(f"OpenBayesDataSettings(data.path):{OpenBayesDataSettings(data.path)}")
        settings = OpenBayesDataSettings(data.path)
        settings.remove_by_cur_user(data.pid or data.did)


def pre_upload(
        path: str, pid: str, process: Callable
) -> Tuple[Optional[dict], Optional[Exception]]:
    process("正在向服务器发送上传请求...")

    req, err = upload_request()
    if err is not None:
        return None, err

    process("服务器已响应")
    process("正在读取文件列表，请稍候...")

    ignore_file_path = Path(path) / IGNORE_FILE_NAME
    ignore_service = IgnoreService(str(ignore_file_path), IGNORE_CLEANUPS)
    disk_service = DiskService(ignore_service)
    files, _, err = disk_service.directory_computing(path, UPLOAD_CODE_LIMIT)
    if err is not None:
        return None, err

    process("剔除在 .openbayesignore 中忽略的文件及文件夹...")
    process(f"共有文件 {files} 个")

    data_file_path, err = openbayes_data_usecase.write_file(
        path, OpenBayesDataType.CODE, pid
    )
    if err is not None:
        return None, err

    process("正在压缩代码...")

    zip_path = Utils.generate_temp_zip_path()
    err = archive_usecase.archive(path, zip_path)
    if err is not None:
        return None, err

    process("压缩代码完成")

    try:
        stat = os.stat(zip_path)
    except Exception as e:
        return None, e

    process("正在初始化上传中...")
    process(f"正在上传压缩包。总共上传大小：{Utils.byte_size(stat.st_size, True)}")

    print(f"data_file_path:{data_file_path},req:{req}")
    data, err = openbayes_data_usecase.update_by_cur_user(
        data_file_path, pid, req.upload_url, req.token, zip_path, stat.st_size
    )

    if err is not None:
        return None, err

    return data, None


def print_url_storage_file_contents(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
            print(f"Contents of {file_path}: {contents}")
    except Exception as e:
        print(f"Failed to read {file_path}: {e}")
