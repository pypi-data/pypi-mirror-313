from enum import Enum
from pathlib import Path

import yaml
from pydantic import BaseModel, Field
from typing import List, Optional, Tuple
import os

from bayes.model.file.settings import BayesEnvConfig, BayesSettings

DATA_FILE_NAME = ".openbayesdata"


class OpenBayesDataType(str, Enum):
    DATASET = "DATASET"
    CODE = "CODE"


class OpenBayesData(BaseModel):
    user: str
    pid: Optional[str] = None  # project_id
    did: Optional[str] = None  # dataset_id
    path: str  # data_file_path
    location: str = ""
    zip: str = ""  # zip_path
    length: int = 0  # upload_length
    token: str = ""

    def has_last_upload(self) -> bool:
        if self.location and self.token and self.zip:
            try:
                os.stat(self.zip)
                return True
            except FileNotFoundError as e:
                print(f"zip_path:{self.zip} not found")
                return False
        return False

    def has_last_archived_upload(self, zip_path: str) -> bool:
        if self.location and self.token and self.zip == zip_path:
            return self.has_last_upload()
        return False

    def update_upload(
        self, location: str, token: str, zip_path: str, upload_length: int
    ):
        self.location = location
        self.zip = zip_path
        self.length = upload_length
        self.token = token


def empty_openbayes_datas() -> List[OpenBayesData]:
    return []


def new_openbayes_dataset_data(did: str, data_file_path: str) -> OpenBayesData:
    default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
    return OpenBayesData(
        user=default_env.username, did=did, path=data_file_path
    )


def new_openbayes_code_data(pid: str, data_file_path: str) -> OpenBayesData:
    default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
    return OpenBayesData(
        user=default_env.username, pid=pid, path=data_file_path
    )


class OpenBayesDataSettings:
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path: Path = Path(config_path) if isinstance(config_path, str) else config_path or Path(DATA_FILE_NAME)
        if self.config_path.is_dir():
            self.config_path = self.config_path / DATA_FILE_NAME
        self.configuration: List[OpenBayesData] = []
        self.load_from_file()

    def load_from_file(self):
        if self.config_path.exists():
            with self.config_path.open("r") as f:
                config_data = yaml.safe_load(f)
            self.configuration = [OpenBayesData(**data) for data in config_data] if config_data else []

    def save_to_file(self):
        with self.config_path.open("w") as f:
            yaml.dump([item.model_dump() for item in self.configuration], f, default_flow_style=False)

    def update_or_add_data(self, new_data: OpenBayesData):
        for i, data in enumerate(self.configuration):
            if data.user == new_data.user and ((data.pid and data.pid == new_data.pid) or (data.did and data.did == new_data.did)):
                self.configuration[i] = new_data
                return
        self.configuration.append(new_data)

    def get_data_by_user_and_id(self, username: str, id: str) -> Optional[OpenBayesData]:
        for data in self.configuration:
            if data.user == username and ((data.pid and data.pid == id) or (data.did and data.did == id)):
                return data
        return None

    def remove_data_by_user_and_id(self, username: str, id: str):
        self.configuration = [
            data for data in self.configuration
            if not (data.user == username and ((data.pid and data.pid == id) or (data.did and data.did == id)))
        ]

    def write(self, new_data: OpenBayesData):
        self.update_or_add_data(new_data)
        self.save_to_file()

    def read_by_cur_user(self, id: str) -> Tuple[Optional[OpenBayesData], Optional[Exception]]:
        default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
        data = self.get_data_by_user_and_id(default_env.username, id)
        if data:
            return data, None
        return None, FileNotFoundError("No matching upload configuration found")

    def remove_by_cur_user(self, id: str) -> Optional[Exception]:
        default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
        self.remove_data_by_user_and_id(default_env.username, id)
        try:
            self.save_to_file()
        except Exception as e:
            return e
        return None