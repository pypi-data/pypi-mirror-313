import os
from pathlib import Path
from typing import Tuple, Optional

from bayes.model.file.openbayes_data import DATA_FILE_NAME as DATA_FILE_NAME, OpenBayesDataSettings, OpenBayesDataType, \
    OpenBayesData, new_openbayes_dataset_data, new_openbayes_code_data
from bayes.model.file.openbayes_ignore import IGNORE_FILE_NAME
from bayes.utils import Utils


def remove_by_cur_user(data_file_path, id) -> Optional[Exception]:
    # print(f"remove_by_cur_user data_file_path: {data_file_path}")
    data_settings = OpenBayesDataSettings(Path(data_file_path))
    return data_settings.remove_by_cur_user(id)


def write_file(directory: str, data_type: OpenBayesDataType, id: str) -> Tuple[str, Optional[Exception]]:
    file_path, err = create_file(directory)
    if err is not None:
        return "", err

    data_settings = OpenBayesDataSettings(Path(file_path))
    info, err = data_settings.read_by_cur_user(id)
    print(f"write_file data_type:{data_type}")
    if err is not None or info is None:
        if data_type == OpenBayesDataType.DATASET:
            new_info = new_openbayes_dataset_data(id, file_path)
        elif data_type == OpenBayesDataType.CODE:
            new_info = new_openbayes_code_data(id, file_path)
        else:
            return file_path, ValueError("Invalid data type")
        
        data_settings.write(new_info)

    return file_path, None


def create_file(directory: str) -> Tuple[str, Optional[Exception]]:
    path = os.path.join(directory, DATA_FILE_NAME)
    if not os.path.exists(path):
        try:
            with open(path, 'w') as file:
                pass
        except Exception as e:
            return "", e

    return path, None


def read_by_cur_user(directory: str, id: str) -> Tuple[Optional[OpenBayesData], Optional[Exception]]:
    path = Utils.get_file_path(directory, DATA_FILE_NAME)
    data_settings = OpenBayesDataSettings(Path(path))
    return data_settings.read_by_cur_user(id)


def update_by_cur_user(directory: str, id: str, location: str, token: str, zip_path: str,
                       upload_length: int) -> Tuple[Optional[OpenBayesData], Optional[Exception]]:
    path = Utils.get_file_path(directory, DATA_FILE_NAME)
    try:
        data_settings = OpenBayesDataSettings(Path(path))
        data, err = data_settings.read_by_cur_user(id)
        if err is not None:
            return None, err
        if data is None:
            return None, FileNotFoundError("No unfinished upload configuration exists")

        # print(f"update_by_cur_user update_upload before data:{data}")
        # print(f"update_by_cur_user location:{location}, token:{token},zip_path:{zip_path},upload_length:{upload_length}")
        data.update_upload(location, token, zip_path, upload_length)
        data_settings.write(data)
        return data, None
    except Exception as e:
        print(f"e:{e}")
        return None, e
