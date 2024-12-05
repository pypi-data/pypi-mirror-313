import sys

from gql.transport.exceptions import TransportQueryError

from bayes.client.base import BayesGQLClient
from bayes.model.dataset import Dataset


def get_dataset_by_id(client: BayesGQLClient, id):
    query = """
    query Dataset($datasetId: String!) {
      dataset(datasetId: $datasetId) {
        size
        id
        name
        links {
          name
          value
        }
      }
    }
    """
    variables = {"datasetId": id}

    try:
        response = client.exec(query, variables)
    except TransportQueryError as e:
        error_message = e.errors[0]['message'] if e.errors else str(e)
        print(error_message, file=sys.stderr)  # 打印错误消息到标准错误流
        sys.exit(1)

    dataset_data = response.get("dataset", {})
    if not dataset_data:
        return None

    return Dataset(**dataset_data)


def create(client: BayesGQLClient, party_name, name, message):
    query = """
        mutation CreateDataset($userId: String!, $name: String!, $description: String) {
          createDataset(userId: $userId, name: $name, description: $description) {
            id
            name
            links {
              name
              value
            }
          }
        }
    """
    variables = {"userId": party_name, "name": name, "description": message}

    try:
        response = client.exec(query, variables)
    except TransportQueryError as e:
        error_message = e.errors[0]['message'] if e.errors else str(e)
        print(error_message, file=sys.stderr)  # 打印错误消息到标准错误流
        sys.exit(1)

    dataset_data = response.get("createDataset", {})
    if not dataset_data:
        return None

    return Dataset(**dataset_data)
