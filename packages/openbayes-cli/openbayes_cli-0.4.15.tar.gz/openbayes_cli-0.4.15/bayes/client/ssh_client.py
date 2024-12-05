import sys
from datetime import datetime

from gql.transport.exceptions import TransportQueryError
from pydantic import BaseModel

from bayes.client.base import BayesGQLClient


class SSHKey(BaseModel):
    id: int
    name: str
    fingerprint: str
    createdAt: datetime


def get_keys(client: BayesGQLClient, username: str):
    query = """
    query Keys($userId: String!) {
      keys(userId: $userId) {
        id
        name
        fingerprint
        createdAt
      }
    }  
    """
    variables = {"userId": username}
    try:
        response = client.exec(query, variables)
    except TransportQueryError as e:
        error_message = e.errors[0]['message'] if e.errors else str(e)
        print(error_message, file=sys.stderr)
        sys.exit(1)

    keys_list = response.get("keys", [])
    if keys_list is None or not keys_list:
        return None

    return [SSHKey(**key) for key in keys_list]


def create_key(client: BayesGQLClient, userId, name, content):
    query = """
    mutation CreateSSHKey($userId: String!, $name: String!, $content: String!) {
      createSSHKey(userId: $userId, name: $name, content: $content) {
        id
        name
        fingerprint
        createdAt
      }
    }
    """
    variables = {"userId": userId, "name": name, "content": content}
    try:
        response = client.exec(query, variables)
    except TransportQueryError as e:
        error_message = e.errors[0]['message'] if e.errors else str(e)
        print(error_message, file=sys.stderr)
        sys.exit(1)

    result = response.get("createSSHKey")
    if result is None:
        raise Exception("create SSHKey result is none")

    return SSHKey(**result)
