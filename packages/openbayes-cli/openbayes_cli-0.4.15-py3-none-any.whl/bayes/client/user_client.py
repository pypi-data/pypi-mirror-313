from gql.transport.exceptions import TransportQueryError

from .base import BayesGQLClient

from pydantic import BaseModel

from ..error import Error


class LoginModel(BaseModel):
    email: str
    token: str
    username: str


def login(client: BayesGQLClient, username: str, password: str) -> LoginModel:
    query = """
    mutation Login($username: String!, $password: String!) {
      login(username: $username, password: $password) {
        email
        token
        username
      }
    }
    """
    variables = {"username": username, "password": password}
    try:
        response = client.exec(query, variables)
    except TransportQueryError as e:
        raise Error(e.errors[0]['message'] if e.errors else str(e))

    login_data = response.get("login")
    if login_data is None:
        raise Error("Login failed: Unexpected response format")

    return LoginModel(**login_data)


def login_with_token(client: BayesGQLClient, token):
    query = """
        query LoginWithToken($token: String!) {
            loginWithToken(token: $token) {
                email
                username
            }
        }
        """
    variables = {"token": token}
    try:
        response = client.exec(query, variables)
    except TransportQueryError as e:
        raise Error(e.errors[0]['message'] if e.errors else str(e))

    login_data = response.get("loginWithToken")
    if login_data is None:
        raise Error("Login failed: Unexpected response format")

    return LoginModel(token=token, **login_data)
