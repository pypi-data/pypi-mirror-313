import os
import queue
import sys
import threading
import time
from typing import Optional

import typer

from bayes.client import gear_client
from bayes.client.base import BayesGQLClient
from bayes.client.gear_client import DownloadInfoPayload
from bayes.model.file.settings import BayesSettings
from bayes.usercases import archive_usecase
from bayes.utils import Utils


def is_folder_empty(target):
    if not os.path.exists(target):
        return True

    files = os.listdir(target)
    return len(files) == 0


def get_download_url(id, party_name, download_from):
    default_env = BayesSettings().default_env
    gql_client = BayesGQLClient(default_env.graphQL, default_env.token)

    return gear_client.get_output_download_link(gql_client, id, party_name, download_from)


def get_target_file_name(target, payload: DownloadInfoPayload):
    return os.path.join(target, payload.get_file_name())


def is_file_exist(filename):
    if os.path.exists(filename):
        return True
    else:
        return False


def is_continuing(filename: str) -> bool:
    is_continuing = typer.prompt(f"{filename} 已存在在目标路径中，是否需要覆盖？ [y/N]")
    if not is_continuing:
        print("Operation cancelled by the user.")
        sys.exit(1)
    if is_continuing.lower() in ("y", "yes"):
        return True
    return False


def download(target, payload):
    filename = get_target_file_name(target, payload)
    is_finished = queue.Queue()

    print("正在下载中，请稍候")

    def download_process():
        is_done = False
        while not is_done:
            if not is_finished.empty():
                result = is_finished.get()
                if isinstance(result, tuple):
                    is_done, err = result
                else:
                    raise TypeError("Queue item is not a tuple")

                if is_done:
                    print(f"\r下载完成，文件保存在 {filename}")
                else:
                    print(f"\r下载失败: {err}")
                print()
                break
            else:
                try:
                    file_stat = os.stat(filename)
                    size = Utils.byte_size(file_stat.st_size, False)
                    print(f"\r已下载 {size}", end="")
                except FileNotFoundError:
                    pass
                time.sleep(1)

    download_thread = threading.Thread(target=download_process)
    download_thread.start()

    err = gear_client.download(payload.url, filename, is_finished)

    if payload.is_file():
        print(f"payload.is_file:{payload.is_file()}")
        return "", err

    return filename, err


def rename_zip(zip_name, filename):
    is_exist, err = archive_usecase.is_file_exist(zip_name, filename)
    if is_exist and err is None:
        new_file_name = zip_name.replace(".zip", "_" + Utils.generate_uid() + ".zip")
        os.rename(zip_name, new_file_name)
        return new_file_name
    return zip_name


def unzip(source, target):
    try:
        err = archive_usecase.unzip(source, target)
        if err:
            return err
        os.remove(source)
    except Exception as e:
        return e
