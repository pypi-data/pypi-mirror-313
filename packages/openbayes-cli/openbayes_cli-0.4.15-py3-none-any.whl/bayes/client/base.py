from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


class BayesGQLClient:
    def __init__(self, endpoint, token) -> None:
        headers = {
            "Origin": endpoint
        }
        if token is not None:
            headers['Authorization'] = f'Bearer {token}'

        transport = AIOHTTPTransport(
            url=endpoint,
            headers=headers)
        self.client = Client(transport=transport)

    def exec(self, query, variable_values={}):
        return self.client.execute(gql(query), variable_values=variable_values)

