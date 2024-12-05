from bayes.client.dataset_upload_client import DatasetRequestUploadUrl
from bayes.model.file.settings import BayesSettings

import requests


def merge_dataset_request(did: str, version: str, directory: str):
    # https://beta.openbayes.com/api/users/QionBeta1/datasets/62PadeCE8XU/versions/25/upload-request?protocol=tusd&key=/%2F/
    default_env = BayesSettings().default_env
    url = f"{default_env.endpoint}/api/users/{default_env.username}/datasets/{did}/versions/{version}/upload-request"
    params = {'protocol': 'tusd'}
    auth_token = default_env.token
    headers = {"Authorization": f"Bearer {auth_token}"}

    # 如果 directory 参数被提供且不为空
    if directory:
        # 确保 directory 以 '/' 开头
        if not directory.startswith('/'):
            directory = '/' + directory
        if not directory.endswith('/'):
            directory += '/'

        params['key'] = directory

    try:
        response = requests.post(url, headers=headers, params=params)
        print(f"merge_dataset_request url:{url} with params: {params}")
    except requests.RequestException as e:
        print(f"merge_dataset_request exception:{e}")
        return None, e

    print(f"merge_dataset_request response.content:{response.content}")

    if response.status_code != 200:
        return None, Exception(f"Request failed with status code {response.status_code}")

    try:
        result = response.json()
        upload_request = DatasetRequestUploadUrl(**result)
        return upload_request, None
    except ValueError as e:
        return None, e
