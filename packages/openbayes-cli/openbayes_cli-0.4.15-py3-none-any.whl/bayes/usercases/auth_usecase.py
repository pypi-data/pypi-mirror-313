from typing import Optional

from bayes.client import user_client
from bayes.client.base import BayesGQLClient
from bayes.model.file.settings import BayesSettings, BayesEnvConfig


def get_default_credential_userinfo():
    default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
    gql_client = BayesGQLClient(default_env.graphQL, None)

    if not default_env.token:
        print("用户还未登陆")
        return

    login_model = user_client.login_with_token(gql_client, default_env.token)
    # 登陆成功，获得用户信息，去修改文件
    BayesSettings().login(login_model.username, login_model.token)
    return login_model


def check_login():
    default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
    if default_env.name and default_env.token:
        return True
    else:
        return False


def is_working_on_org():
    default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
    if default_env.token and default_env.orgName:
        return True
    else:
        return False