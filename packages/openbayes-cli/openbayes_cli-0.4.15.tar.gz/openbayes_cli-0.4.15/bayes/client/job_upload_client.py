import http
import logging
import os
import base64
import json
from typing import Optional, Tuple

import requests
from tusclient import client
from tusclient.storage import filestorage
from tqdm import tqdm
from tusclient.exceptions import TusCommunicationError

from pydantic import BaseModel

from bayes.error import Error, request_failed
from bayes.model.file.settings import BayesEnvConfig, BayesSettings
TUS_STORAGE_FILE = ".tus_storage"


class RequestUploadUrl(BaseModel):
    upload_url: str
    token: str


def upload_request() -> Tuple[Optional[RequestUploadUrl], Optional[Exception]]:
    # https://beta.openbayes.com/api/users/Qion1/jobs/upload-request?protocol=tusd
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


def upload_file(
    file_path: str, upload_url: str, token: str, retries=0, max_retries=3
) -> Tuple[bool, Optional[str], Optional[Exception]]:
    if retries > max_retries:
        return False, None, Exception("Max retries exceeded")

    try:
        my_client = client.TusClient(
            upload_url, headers={"Authorization": f"Bearer {token}"}
        )
        file_size = os.path.getsize(file_path)

        # Create a FileStorage instance for resumability
        url_storage_file = os.path.join(os.path.dirname(file_path), TUS_STORAGE_FILE)
        storage = filestorage.FileStorage(url_storage_file)

        # Prepare metadata
        filename = os.path.basename(file_path)
        metadata = {"filename": filename}

        with tqdm(total=file_size, unit="B", unit_scale=True, desc="Uploading") as pbar:
            uploader = my_client.uploader(
                file_path,
                chunk_size=2 * 1024 * 1024,
                store_url=True,
                url_storage=storage,
                upload_checksum=False,
                metadata=metadata,
            )

            while uploader.offset < file_size:
                uploader.upload_chunk()
                pbar.update(uploader.offset - pbar.n)

        # print(f"File uploaded successfully: {file_path}")

        # Remove filestorage after upload successfully
        storage_path = os.path.join(os.path.dirname(file_path), ".tus_storage")
        if os.path.exists(storage_path):
            os.remove(storage_path)
            # print(f"Removed filestorage: {storage_path}")

        # Decode the JWT token to get the payload
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
            return upload_file(file_path, upload_url, token, retries + 1, max_retries)
        else:
            return False, None, e
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False, None, e
