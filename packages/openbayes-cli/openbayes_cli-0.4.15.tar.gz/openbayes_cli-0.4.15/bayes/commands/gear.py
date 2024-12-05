import os
import time
from pathlib import Path
from typing import Optional, List

import typer

from bayes.client import job_run_client
from bayes.model.file.openbayes_gear import OpenBayesGearSettings, FILE_NAME as GEAR_FILE_NAME
from bayes.model.file.openbayes_yaml import OpenBayesYamlSettings, FILE_NAME, DEFAULT_JOB_RESOURCE, DEFAULT_JOB_RUNTIME
from bayes.model.file.settings import BayesEnvConfig
from bayes.model.party import ModeEnum
from bayes.usercases import auth_usecase, gear_usecase, open_usecase, resource_usecase, runtime_usecase, \
    gear_logs_usecase, gear_download_usecese, gear_run_usecase
from bayes.utils import Utils

app = typer.Typer()


@app.command()
def init(ctx: typer.Context, id_or_name: str,
         message: str = typer.Option(None, "-m", "--message", help="容器描述"),
         open: bool = typer.Option(False, "-o", "--open", help="成功初始化容器后，在浏览器打开")):
    """
    初始化容器
    用法：
       bayes gear init [容器名称 或 容器编码] [选项]

    可用选项：
        -h, --help             查看 init 的帮助
        -m, --message string   [可选] 容器描述
        -o, --open             [可选] 成功初始化容器后，在浏览器打开
    """

    # 检查用户是否已登录
    login = auth_usecase.check_login()
    if not login:
        print("尚未授权，请先登录")
        raise typer.Exit(code=1)
    # 检查现在是处于 组织/用户 状态
    bayes_settings = ctx.obj
    default_env: Optional[BayesEnvConfig] = bayes_settings.default_env

    party_name = ""
    if auth_usecase.is_working_on_org():
        party_name = default_env.orgName
        print(f"当前正在组织 {party_name} 上进行操作...")
    else:
        party_name = default_env.username
        print(f"当前正在个人账号 {party_name} 上进行操作...")

    # 获取当前工作目录
    current_path = Path(os.getcwd())

    #  创建 OpenBayesYamlSettings 去读取 openbayes.yaml ,如果不存在就创建默认的
    OpenBayesYamlSettings(config_path=current_path / FILE_NAME)

    get_project_tags = ["BUSINESS_CHANNEL_ML"]
    project = gear_usecase.get_project_by_id_or_name(party_name, id_or_name, get_project_tags, 1, 200)
    if project is None:
        create_project_tags = [
            {
                "name": "BUSINESS_CHANNEL_ML"
            }
        ]
        project = gear_usecase.create_project(party_name, id_or_name, message, create_project_tags)

    gear_usecase.init_project(current_path, project.id, project.name)

    print("容器初始化成功")
    if open:
        print("正在跳转到浏览器...")
        open_usecase.open_browser(project.get_link_value("frontend"))


@app.command()
def ls(ctx: typer.Context,
       page: int = typer.Option(1, "-p", "--page", help="跳转页码")):
    """
    查看所有容器
    用法：
        bayes gear ls [选项]

    可用选项：
        -h, --help          查看 ls 的帮助
        -p, --page string   [可选] 跳转页码

    """

    # 检查用户是否已登录
    login = auth_usecase.check_login()
    if not login:
        print("尚未授权，请先登录")
        raise typer.Exit(code=1)
    # 检查现在是处于 组织/用户 状态
    bayes_settings = ctx.obj
    default_env: Optional[BayesEnvConfig] = bayes_settings.default_env

    party_name = ""
    if auth_usecase.is_working_on_org():
        party_name = default_env.orgName
        print(f"当前正在组织 {party_name} 上进行操作...")
    else:
        party_name = default_env.username
        print(f"当前正在个人账号 {party_name} 上进行操作...")

    get_projects_tags = ["BUSINESS_CHANNEL_ML"]
    project_data_list = gear_usecase.get_party_projects(party_name, get_projects_tags, page)
    gear_usecase.list_projects_display_table(project_data_list)


@app.command()
def run(
        ctx: typer.Context,
        mode: ModeEnum = typer.Argument(..., help="task 或 workspace 或 hypertuning", case_sensitive=True, clamp=True),
        data: List[str] = typer.Option([], "-d", "--data", help="绑定数据"),
        env: str = typer.Option("", "-e", "--env", help="选择镜像"),
        resource: str = typer.Option("", "-r", "--resource", help="选择算力"),
        follow: bool = typer.Option(False, "-f", "--follow", help="运行容器的状态跟踪"),
        message: str = typer.Option("", "-m", "--message", help="执行描述"),
        open_browser: bool = typer.Option(False, "-o", "--open", help="成功创建容器后，在浏览器打开"),
        node: int = typer.Option(-1, "-n", "--node", help="指定运行节点数量"),
        extra_args: Optional[List[str]] = typer.Argument(None, help="task command 额外参数")
):
    """
    运行容器
    用法：
        bayes gear run [task 或 workspace 或 hypertuning] [选项]

    可用选项：
        -d, --data strings      绑定数据
        -e, --env string        选择镜像
        -f, --follow            [可选] 运行容器的状态跟踪
        -h, --help              查看 run 的帮助
        -m, --message string    执行描述
        -o, --open              [可选] 成功创建容器后，在浏览器打开
        -r, --resource string   选择算力
    """
    # 检查用户是否已登录
    login = auth_usecase.check_login()
    if not login:
        print("尚未授权，请先登录")
        raise typer.Exit(code=1)
    # 检查现在是处于 组织/用户 状态
    bayes_settings = ctx.obj
    default_env: Optional[BayesEnvConfig] = bayes_settings.default_env

    party_name = ""
    if auth_usecase.is_working_on_org():
        party_name = default_env.orgName
        print(f"当前正在组织 {party_name} 上进行操作...")
    else:
        party_name = default_env.username
        print(f"当前正在个人账号 {party_name} 上进行操作...")

    # 获得当前路径   去读取 openbayesgear 文件获得 init 的 id（projectId）
    current_path = Path(os.getcwd())
    gear_settings = OpenBayesGearSettings(config_path=current_path / GEAR_FILE_NAME)

    if gear_settings.configuration is None or not gear_settings.configuration.id:
        print('项目编号不存在，请先使用 "bayes gear init [项目编码 或 项目名称]" 完成初始化')
        raise typer.Exit(code=1)
    pid = gear_settings.configuration.id

    try:
        yaml_settings = OpenBayesYamlSettings(config_path=current_path / FILE_NAME)
    except Exception as e:

        print("访问文档可查看示例，文档地址: https://openbayes.com/docs/cli/#创建python-脚本执行")
        raise typer.Exit(code=1)

    if mode == "":
        print("请先设置 mode")
        raise typer.Exit(code=1)

    if len(data) == 0 and yaml_settings is not None and yaml_settings.configuration is not None:
        data = yaml_settings.configuration.get_dataset_bindings()

    if resource == "" and yaml_settings is not None and yaml_settings.configuration is not None:
        resource = yaml_settings.configuration.resource

    if resource == "":
        resource = DEFAULT_JOB_RESOURCE

    if env == "" and yaml_settings is not None and yaml_settings.configuration is not None:
        env = yaml_settings.configuration.get_runtime()

    if env == "":
        env = DEFAULT_JOB_RUNTIME

    task_command = ""
    if yaml_settings is not None and yaml_settings.configuration is not None:
        task_command = yaml_settings.configuration.command

    if extra_args:
        extra_command = " ".join(extra_args)
        task_command = f"{task_command} {extra_command}".strip()

    if mode == ModeEnum.task and task_command == "":
        print("准备创建 task，执行命令不能为空")
        raise typer.Exit(code=1)

    cid = gear_usecase.upload_code(str(current_path), pid)
    # print(f"code id: {cid}")

    print("正在向服务器请求创建容器...")

    frontend_value, job_id, err = gear_run_usecase.create(party_name, current_path, "", mode, yaml_settings.configuration,
                                                    data, node, env, resource, cid, task_command, message)

    if err is not None and frontend_value == "":
        print(f"create err:{err}")
        raise typer.Exit(code=1)

    print("容器创建成功")
    open_url = Utils.replace_last_id(frontend_value, job_id)
    print(f"打开网页 {open_url} 可查看容器的详细信息")

    if open_browser:
        open_usecase.open_browser(open_url)

    gear_settings.update_jid(str(current_path), job_id)

    time.sleep(3)

    if follow and mode != ModeEnum.hypertuning:
        gear_usecase.follow_status(job_id, party_name, True)
        gear_usecase.print_last_status(job_id, party_name)


@app.command()
def status(ctx: typer.Context,
           page: int = typer.Option(1, "-p", "--page", help="跳转页码")):
    """
    查看容器下的所有任务
    用法：
        bayes gear status [选项]

    可用选项：
        -h, --help          查看 status 的帮助
        -p, --page string   [可选] 跳转页码

    """
    login = auth_usecase.check_login()
    if not login:
        print("尚未授权，请先登录")
        raise typer.Exit(code=1)
    # 检查现在是处于 组织/用户 状态
    bayes_settings = ctx.obj
    default_env: Optional[BayesEnvConfig] = bayes_settings.default_env

    party_name = ""
    if auth_usecase.is_working_on_org():
        party_name = default_env.orgName
        print(f"当前正在组织 {party_name} 上进行操作...")
    else:
        party_name = default_env.username
        print(f"当前正在个人账号 {party_name} 上进行操作...")

    #     获取当前路径下的 gear 文件中的 projectId，不存在提示信息
    current_path = Path(os.getcwd())
    gear_settings = OpenBayesGearSettings(config_path=current_path / GEAR_FILE_NAME)
    gear_settings.load_from_file()
    if gear_settings.configuration is None or not gear_settings.configuration.id:
        print('项目编号不存在，请先使用 "bayes gear init [项目编码 或 项目名称]" 完成初始化')
        return

    project_id = gear_settings.configuration.id
    project = gear_usecase.get_project_jobs_by_id(party_name, project_id, page)
    gear_usecase.list_project_jobs_display_table(project)


@app.command()
def restart(ctx: typer.Context,
            id: str,
            data: List[str] = typer.Option([], "-d", "--data", help="绑定数据"),
            env: str = typer.Option("", "-e", "--env", help="选择镜像"),
            resource: str = typer.Option("", "-r", "--resource", help="选择算力"),
            follow: bool = typer.Option(False, "-f", "--follow", help="运行容器的状态跟踪"),
            message: str = typer.Option("", "-m", "--message", help="执行描述"),
            open_browser: bool = typer.Option(False, "-o", "--open", help="成功创建容器后，在浏览器打开"),
            node: int = typer.Option(-1, "-n", "--node", help="指定运行节点数量"),
            extra_args: Optional[List[str]] = typer.Argument(None, help="task command 额外参数")
            ):
    """
    继续执行容器
    用法：
        bayes gear restart [任务编码] [选项]

    可用选项：
        -d, --data strings      绑定数据
        -e, --env string        选择镜像
        -f, --follow            [可选] 继续执行容器的状态跟踪
        -h, --help              查看 restart 的帮助
        -m, --message string    执行描述
        -o, --open              [可选] 继续执行容器后，在浏览器打开
        -r, --resource string   选择算力

    """
    # 检查用户是否已登录
    login = auth_usecase.check_login()
    if not login:
        print("尚未授权，请先登录")
        raise typer.Exit(code=1)
    # 检查现在是处于 组织/用户 状态
    bayes_settings = ctx.obj
    default_env: Optional[BayesEnvConfig] = bayes_settings.default_env

    party_name = ""
    if auth_usecase.is_working_on_org():
        party_name = default_env.orgName
        print(f"当前正在组织 {party_name} 上进行操作...")
    else:
        party_name = default_env.username
        print(f"当前正在个人账号 {party_name} 上进行操作...")

    job = gear_usecase.get_job_by_id(id, party_name)
    if job is None:
        print("请输入正确的任务编码")
        raise typer.Exit(code=1)

    project_name = job.project.name
    frontend_url = job.get_link_value("frontend")
    open_url = Utils.replace_last_id(frontend_url, job.id)

    task_command = ""
    if extra_args:
        extra_command = " ".join(extra_args)
        task_command = f"{task_command} {extra_command}".strip()

    try:
        new_frontend_value, job_id = gear_run_usecase.restart(id, party_name, data, env, resource, task_command, node,
                                                              message)
    except Exception as e:
        print(f"e:{e}")
        print("重启失败")
        if open_url is not None:
            print(f"打开网页 {open_url} 可查看容器 {project_name} 的详细信息")
        raise typer.Exit(code=1)

    print("容器继续执行...")
    if new_frontend_value is not None:
        new_open_url = Utils.replace_last_id(new_frontend_value, job_id)
        print(f"打开网页 {new_open_url} 可查看容器 {project_name} 的详细信息")

    if message != "":
        gear_usecase.update_job_description(party_name, job_id, message)

    if open_browser:
        open_usecase.open_browser(new_open_url)

    if follow:
        gear_usecase.follow_status(job_id, party_name, True)
        gear_usecase.print_last_status(job_id, party_name)


@app.command()
def stop(ctx: typer.Context,
         id: str = typer.Argument(None, help="指定下载的任务 ID"),
         follow: bool = typer.Option(False, "-f", "--follow", help="停止容器的状态跟踪"),
         open: bool = typer.Option(False, "-o", "--open", help="在浏览器打开正在关闭的容器")):
    """
    停止容器
    用法：
        bayes gear stop [任务编码] [选项]

    可用选项：
        -f, --follow   [可选] 停止容器的状态跟踪
        -h, --help     查看 stop 的帮助
        -o, --open     [可选] 在浏览器打开正在关闭的容器
    """
    login = auth_usecase.check_login()
    if not login:
        print("尚未授权，请先登录")
        raise typer.Exit(code=1)
    # 检查现在是处于 组织/用户 状态
    bayes_settings = ctx.obj
    default_env: Optional[BayesEnvConfig] = bayes_settings.default_env

    party_name = ""
    if auth_usecase.is_working_on_org():
        party_name = default_env.orgName
        print(f"当前正在组织 {party_name} 上进行操作...")
    else:
        party_name = default_env.username
        print(f"当前正在个人账号 {party_name} 上进行操作...")

    if id is None:
        # 获得当前路径   去读取 openbayesgear 文件获得 init 的 id（projectId）
        current_path = Path(os.getcwd())
        gear_settings = OpenBayesGearSettings(config_path=current_path / GEAR_FILE_NAME)
        if gear_settings.configuration is None or not gear_settings.configuration.id or not gear_settings.configuration.jid:
            print('项目编号不存在，请先使用 "bayes gear run [task 或 workspace 或 hypertuning] [选项]" 完成项目创建')
            raise typer.Exit(code=1)
        else:
            id = gear_settings.configuration.jid

    job = gear_usecase.stopJob(id, party_name)
    print("同步数据并关闭容器")
    frontend = job.get_link_value("frontend")
    link_value = Utils.replace_last_id(frontend, job.id)
    if link_value is not None:
        print(f"打开网页 {link_value} 可查看容器 {job.project.name} 的详细信息")
        if open:
            open_usecase.open_browser(link_value)

    if follow:
        gear_usecase.follow_status(id, party_name, True)
        gear_usecase.print_last_status(id, party_name)


@app.command()
def bindings(ctx: typer.Context):
    """
    查看运行容器可绑定的数据
    用法：
        bayes gear bindings [选项]

    可用选项：
        -h, --help           查看 bindings 的帮助
        -q, --query string   输入关键字查询可绑定的数据
    """
    # 检查用户是否已登录
    login = auth_usecase.check_login()
    if not login:
        print("尚未授权，请先登录")
        raise typer.Exit(code=1)
    # 检查现在是处于 组织/用户 状态
    bayes_settings = ctx.obj
    default_env: Optional[BayesEnvConfig] = bayes_settings.default_env

    party_name = ""
    if auth_usecase.is_working_on_org():
        party_name = default_env.orgName
        print(f"当前正在组织 {party_name} 上进行操作...")
    else:
        party_name = default_env.username
        print(f"当前正在个人账号 {party_name} 上进行操作...")

    binding_datasets = gear_usecase.list_binding_datasets(party_name, "--data")
    gear_usecase.list_binding_datasets_display_table(binding_datasets)


@app.command()
def download(ctx: typer.Context,
             id: str = typer.Argument(None, help="指定下载的任务 ID"),
             download_from: str = typer.Option("", "--from", "-f", help="指定下载的子路径，不填则下载整个输出"),
             download_target: str = typer.Option("", "--target", "-t", help="本地存在位置，不填则使用当前路径"),
             unarchive: bool = typer.Option(False, "--unarchive", "-u", help="是否自动解压压缩包并删除源文件")):
    """
    下载容器输出
    用法：
       bayes gear download [任务编码] [选项]

    可用选项：
        -f, --from string     [可选] 指定下载的子路径，不填则下载整个输出
        -h, --help            查看 download 的帮助
        -t, --target string   [可选] 本地存在位置，不填则使用当前路径
        -u, --unarchive       [可选] 是否自动解压压缩包并删除源文件
    """
    # 检查用户是否已登录
    login = auth_usecase.check_login()
    if not login:
        print("尚未授权，请先登录")
        raise typer.Exit(code=1)
    # 检查现在是处于 组织/用户 状态
    bayes_settings = ctx.obj
    default_env: Optional[BayesEnvConfig] = bayes_settings.default_env

    party_name = ""
    if auth_usecase.is_working_on_org():
        party_name = default_env.orgName
        print(f"当前正在组织 {party_name} 上进行操作...")
    else:
        party_name = default_env.username
        print(f"当前正在个人账号 {party_name} 上进行操作...")

    target = gear_usecase.get_download_target(download_target)

    id = gear_usecase.get_jobId_from_curPath(id)

    if unarchive and not gear_download_usecese.is_folder_empty(target):
        print(f"下载无法完成，{target} 已存在，且不是一个空文件夹，请选择其他路径后重试")
        raise typer.Exit(code=1)

    payload = gear_download_usecese.get_download_url(id, party_name, download_from)
    if payload is None:
        print(f"{download_from} 文件或路径不存在，请检查你所填写的参数")
        raise typer.Exit(code=1)

    filename = gear_download_usecese.get_target_file_name(target, payload)
    if gear_download_usecese.is_file_exist(filename) and not gear_download_usecese.is_continuing(filename):
        print("已终止下载")
        raise typer.Exit(code=1)

    zip, err = gear_download_usecese.download(target, payload)
    if err is not None:
        print("下载失败，请重试")
        raise typer.Exit(code=1)

    if zip != "" and unarchive:
        new_zip = gear_download_usecese.rename_zip(zip, payload.get_file_name())
        time.sleep(1)
        print("正在解压中，请稍候")
        if new_zip != zip:
            print(f"压缩包被重命名为 {new_zip}")

        err = gear_download_usecese.unzip(new_zip, target)
        if err is not None:
            print("自动解压无法完成")
            raise typer.Exit(code=1)

        print(f"解压完成，文件保存在 {target}")
        print(f"压缩包 {new_zip} 已删除")


@app.command()
def env(ctx: typer.Context):
    """
    查看运行容器可选的环境
    用法：
        bayes gear env [选项]

    可用选项：
        -h, --help   查看 env 的帮助
    """
    # 检查用户是否已登录
    login = auth_usecase.check_login()
    if not login:
        print("尚未授权，请先登录")
        raise typer.Exit(code=1)
    # 检查现在是处于 组织/用户 状态
    bayes_settings = ctx.obj
    default_env: Optional[BayesEnvConfig] = bayes_settings.default_env

    party_name = ""
    if auth_usecase.is_working_on_org():
        party_name = default_env.orgName
        print(f"当前正在组织 {party_name} 上进行操作...")
    else:
        party_name = default_env.username
        print(f"当前正在个人账号 {party_name} 上进行操作...")

    runtimes = runtime_usecase.get_list_runtimes(party_name, ["JOB"], ["MACHINE_LEARNING"],
                                                 ["CONTAINER", "VIRTUAL_MACHINE"])
    runtime_usecase.list_runtimes_display_table(runtimes, "--env")


@app.command()
def logs(id: str, ctx: typer.Context,
         follow: bool = typer.Option(False, "--follow", "-f", help="日志自动更新")):
    """
    查看容器日志
    用法：
        bayes gear logs [选项]

    可用选项：
        -f, --follow   [可选] 日志自动更新
        -h, --help     查看 logs 的帮助

    """
    # 检查用户是否已登录
    login = auth_usecase.check_login()
    if not login:
        print("尚未授权，请先登录")
        raise typer.Exit(code=1)
    # 检查现在是处于 组织/用户 状态
    bayes_settings = ctx.obj
    default_env: Optional[BayesEnvConfig] = bayes_settings.default_env

    party_name = ""
    if auth_usecase.is_working_on_org():
        party_name = default_env.orgName
        print(f"当前正在组织 {party_name} 上进行操作...")
    else:
        party_name = default_env.username
        print(f"当前正在个人账号 {party_name} 上进行操作...")

    logs = gear_logs_usecase.get_logs(id, party_name)
    if follow:
        ws, error = gear_logs_usecase.get_logs_follow(id, party_name)
        if error is not None:
            print(error)
            raise typer.Exit(code=1)
        if ws is None:
            print(logs)

        while True:
            data, error = gear_logs_usecase.receive_logs(ws, id)
            if error is None:
                print(data)
            else:
                print(error)
                raise typer.Exit(code=1)
    else:
        print(logs)


@app.command()
def open(ctx: typer.Context, id_or_name: Optional[str] = typer.Argument(None, help="容器名称 或 容器ID 或 任务ID")):
    """
    在浏览器打开容器页面

    用法：
        bayes gear open [容器名称 或 容器ID 或 任务ID] [选项]

    可用选项：
        -h, --help   查看 open 的帮助
    """
    # 检查用户是否已登录
    login = auth_usecase.check_login()
    if not login:
        print("尚未授权，请先登录")
        raise typer.Exit(code=1)
    # 检查现在是处于 组织/用户 状态
    bayes_settings = ctx.obj
    default_env: Optional[BayesEnvConfig] = bayes_settings.default_env

    party_name = ""
    if auth_usecase.is_working_on_org():
        party_name = default_env.orgName
        print(f"当前正在组织 {party_name} 上进行操作...")
    else:
        party_name = default_env.username
        print(f"当前正在个人账号 {party_name} 上进行操作...")

    if id_or_name is None:
        # 获得当前路径   去读取 openbayesgear 文件获得 init 的 id（projectId）
        current_path = Path(os.getcwd())
        gear_settings = OpenBayesGearSettings(config_path=current_path / GEAR_FILE_NAME)
        if gear_settings.configuration is None or not gear_settings.configuration.id:
            print('项目编号不存在，请先使用 "bayes gear init [项目编码 或 项目名称]" 完成初始化')
            raise typer.Exit(code=1)
        id_or_name = gear_settings.configuration.id

    job = gear_usecase.get_job_by_id(id_or_name, party_name)
    if job:
        frontend = job.get_link_value("frontend")
        link = Utils.replace_last_id(frontend, job.id)
        print(f"正在打开任务 {link}")
        print("正在跳转到浏览器...")
        open_usecase.open_browser(link)
        return

    project = gear_usecase.get_project_by_id_or_name(party_name, id_or_name, [], 1, 200)
    if project:
        link = project.get_link_value("frontend")
        print(f"正在打开容器 {link}")
        print("正在跳转到浏览器...")
        open_usecase.open_browser(link)
    else:
        print(f"未查询到容器 {id_or_name}, 请输入正确的容器名称或ID")


@app.command()
def resource(ctx: typer.Context):
    """
    查看运行容器可选的资源

    用法：
        bayes gear resource [选项]

    可用选项：
        -h, --help   查看 open 的帮助

    """

    # 检查用户是否已登录
    login = auth_usecase.check_login()
    if not login:
        print("尚未授权，请先登录")
        raise typer.Exit(code=1)
    # 检查现在是处于 组织/用户 状态
    bayes_settings = ctx.obj
    default_env: Optional[BayesEnvConfig] = bayes_settings.default_env

    party_name = ""
    if auth_usecase.is_working_on_org():
        party_name = default_env.orgName
        print(f"当前正在组织 {party_name} 上进行操作...")
    else:
        party_name = default_env.username
        print(f"当前正在个人账号 {party_name} 上进行操作...")

    resource_usecase.list_resources_display_table("--resource", party_name, ["JOB"], ["MACHINE_LEARNING", "CONTAINER"])


if __name__ == "__main__":
    app()
