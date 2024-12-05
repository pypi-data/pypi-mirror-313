import logging
import time
import zipfile
import archiver
import shutil
import os

from bayes.model.file.openbayes_ignore import IGNORE_FILE_NAME, IGNORE_CLEANUPS
from bayes.usercases.disk_usecase import IgnoreService


def is_file_exist(zip_name, filename):
    try:
        with zipfile.ZipFile(zip_name, 'r') as zr:
            for file in zr.filelist:
                if not file.is_dir():
                    if file.filename == filename:
                        return True
    except Exception as err:
        return False, err

    return False, None


def unzip(source, target):
    try:
        if source.endswith('.zip'):
            with zipfile.ZipFile(source, 'r') as zip_ref:
                zip_ref.extractall(target)
    except Exception as e:
        return e


def append_file(zip_writer, source, filename):
    path = os.path.join(source, filename)

    try:
        # 打开文件
        with open(path, 'rb') as file_to_zip:
            # 获取文件信息
            info = os.stat(path)

            # 创建 ZIP 文件头
            header = zipfile.ZipInfo(filename)
            header.compress_type = zipfile.ZIP_DEFLATED
            header.file_size = info.st_size

            # 获取文件的修改时间并设置为 ZIP 文件头的时间
            mtime = time.localtime(info.st_mtime)
            header.date_time = mtime[:6]

            # 将文件内容写入 ZIP 文件
            zip_writer.writestr(header, file_to_zip.read())

    except Exception as e:
        return e

    return None


def archive(source, destination):
    continue_on_error = True

    try:
        with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            ignore_service = IgnoreService(IGNORE_FILE_NAME, IGNORE_CLEANUPS)
            left_files, _, error = ignore_service.left(source)
            if error is not None:
                return error

            for filename in left_files:
                err = append_file(zip_file, source, filename)
                if err is not None and not continue_on_error:
                    return err
    except Exception as e:
        logging.error(f"archive: Error calling ignore_service.left: {e}")
        return e

    return None