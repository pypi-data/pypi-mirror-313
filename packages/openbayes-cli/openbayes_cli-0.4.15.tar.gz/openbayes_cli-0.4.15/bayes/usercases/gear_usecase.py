import os
import sys
import time
from pathlib import Path
from typing import Optional, List, Tuple

import typer
from rich import filesize
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    ProgressColumn,
)

from bayes.client import gear_client, job_run_client
from bayes.client.base import BayesGQLClient
from bayes.client.gear_client import ProjectModel
from bayes.error import Error
from bayes.model.file.openbayes_data import OpenBayesData
from bayes.model.file.openbayes_gear import (
    OpenBayesGearSettings,
    FILE_NAME as GEAR_FILE_NAME,
)
from bayes.model.file.openbayes_ignore import OpenBayesIgnoreSettings
from bayes.model.file.settings import BayesEnvConfig, BayesSettings
from bayes.usercases import auth_usecase, dataset_version_usecase, gear_upload_usecase
from bayes.usercases.org_usecase import display_table
from bayes.utils import Utils


def get_project_by_id_or_name(party_name, id_or_name, tagsNames, page, perPage):
    default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
    gql_client = BayesGQLClient(default_env.graphQL, default_env.token)

    return gear_client.get_party_project_by_id_or_name(
        gql_client, party_name, id_or_name, tagsNames, page, perPage
    )


def create_project(party_name, name, desc, tags):
    default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
    gql_client = BayesGQLClient(default_env.graphQL, default_env.token)
    return gear_client.create_project(gql_client, party_name, name, desc, tags)


def init_project(current_path, pid, project_name):
    gear_settings = OpenBayesGearSettings()
    gear_settings.create_or_update(current_path, pid, project_name)
    OpenBayesIgnoreSettings().create_default(current_path)


def get_party_projects(party_name, tags, page):
    default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
    gql_client = BayesGQLClient(default_env.graphQL, default_env.token)
    return gear_client.get_party_projects(gql_client, party_name, tags, page)


def process_project_datas(project_data_list: List[ProjectModel]):
    if project_data_list is None:
        project_data_list = []

    data = [
        [
            project.latestJob.status if project.latestJob is not None else None,
            project.id,
            project.name,
            project.latestVersion,
            Utils.byte_size(project.size, True),
            Utils.date_from_now(project.updatedAt),
        ]
        for project in project_data_list
    ]
    return data


def list_projects_display_table(project_data_list):
    headers = ["STATUS", "PROJECT", "NAME", "VERSIONS", "SIZE", "UPDATED AT"]
    result = process_project_datas(project_data_list)
    display_table(result, headers)


def get_project_jobs_by_id(party_name, project_id, page):
    default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
    gql_client = BayesGQLClient(default_env.graphQL, default_env.token)
    return gear_client.get_project_jobs_by_id(gql_client, party_name, project_id, page)


def process_project_jobs_data(project: ProjectModel):
    data = []

    if project.jobs and project.jobs.data:
        for job in project.jobs.data:
            data.append(
                [
                    job.status,
                    job.id,
                    job.version,
                    job.mode,
                    job.resource.name,
                    job.runtime.framework,
                    Utils.byte_size(job.size, True),
                    Utils.date_from_now(job.createdAt),
                ]
            )
    return data


def list_project_jobs_display_table(project: ProjectModel):
    headers = [
        "STATUS",
        "ID",
        "VERSION",
        "MODE",
        "RESOURCE",
        "RUNTIME",
        "SIZE",
        "UPDATED AT",
    ]
    result = process_project_jobs_data(project)
    return display_table(result, headers)


def list_binding_datasets(party_name, flag):
    return dataset_version_usecase.get_dataset_version_for_gear_binding(
        party_name, flag
    )


def list_binding_datasets_display_table(binding_datasets):
    headers = ["TYPE", "NAME", "CREATED_AT", "USAGE"]
    return display_table(binding_datasets, headers)


def get_cur_path_string():
    return os.getcwd()


def get_download_target(download_target):
    if download_target == "":
        return get_cur_path_string()

    if not os.path.exists(download_target):
        try:
            os.makedirs(download_target, mode=0o755)
        except OSError as e:
            print(e)
            return get_cur_path_string()

    return download_target


def stopJob(id, party_name):
    default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
    gql_client = BayesGQLClient(default_env.graphQL, default_env.token)
    return gear_client.stopJob(gql_client, id, party_name)


def follow_status(id, party_name, stop_with_running):
    default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
    gql_client = BayesGQLClient(default_env.graphQL, default_env.token)

    with Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
    ) as progress:
        task = progress.add_task(f"[purple]Checking job status...", start=False)

        while True:
            # 获取最新的任务状态
            job = gear_client.get_job_by_id(gql_client, id, party_name)
            if job is None:
                progress.update(task, description=f"[red]Failed to fetch job details.")
                break

            # 更新任务描述
            progress.update(task, description=f"[cyan]{job.status}")

            # 判断任务是否已完成或应该停止
            if job.is_finished() or (stop_with_running and job.is_running()):
                progress.stop_task(task)
                # 清空进度条中的旋转器和描述
                progress.update(task, description="")
                progress.remove_task(task)
                break

            # 模拟时间延迟
            for _ in range(50):
                time.sleep(0.1)


def print_last_status(id, party_name):
    default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
    gql_client = BayesGQLClient(default_env.graphQL, default_env.token)

    job = gear_client.get_job_by_id(gql_client, id, party_name)
    if job.is_finished():
        print("容器已关闭")
    elif job.is_running():
        print("容器运行中")
    else:
        print(f"容器状态：{job.status}")

def upload_code(cur_path, pid):
    is_exist, data = gear_upload_usecase.has_last_upload(cur_path, pid)

    if is_exist and data is not None:
        print("OpenBayes 容器上传")
        is_continuing = typer.prompt("存在一个尚未完成的上传，是否需要继续？ [y/N]")
        if is_continuing.lower() in ("y", "yes"):
            print(
                f"正在继续上传压缩包。总共上传大小：{Utils.byte_size(data.length, True)}"
            )
            _, cid, err = gear_upload_usecase.upload(data)
            if err is None:
                print("代码上传成功")
                return cid
            else:
                print(f"上传失败: {err}")
                sys.exit(1)
        else:
            gear_upload_usecase.clear_last_upload(data)

    err = None
    data, err = gear_upload_usecase.pre_upload(cur_path, pid, lambda s: print(s))
    if err is not None or data is None:
        print(f"pre_upload err:{err}, data is: {data}")
        sys.exit(1)

    _, cid, err = gear_upload_usecase.upload(data)
    if err is None:
        print("代码上传成功")
        return cid
    else:
        print(f"上传失败: {err}")
        sys.exit(1)


def read(directory: str) -> Tuple[str, str, str, Exception]:
    try:
        gear_settings = OpenBayesGearSettings(config_path=directory / GEAR_FILE_NAME)
        gear_settings.load_from_file()
        gear = gear_settings.configuration
    except Error as e:
        return "", "", "", e

    return gear.id, gear.jid, gear.name, None


def get_jobId_from_curPath(id):
    if id is not None:
        return id

    cur_path = Path(os.getcwd())
    _, jid, _, _ = read(cur_path)
    if Utils.is_empty_or_none(jid):
        print("未输入任务编码ID，且初始化容器信息获取失败，无法完成下载")
        raise typer.Exit(code=1)

    return jid


def get_job_by_id(id, party_name):
    default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
    gql_client = BayesGQLClient(default_env.graphQL, default_env.token)

    return gear_client.get_job_by_id(gql_client, id, party_name)


def update_job_description(party_name, jid, message):
    default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
    gql_client = BayesGQLClient(default_env.graphQL, default_env.token)

    job_run_client.update_job_description(gql_client, party_name, jid, message)
