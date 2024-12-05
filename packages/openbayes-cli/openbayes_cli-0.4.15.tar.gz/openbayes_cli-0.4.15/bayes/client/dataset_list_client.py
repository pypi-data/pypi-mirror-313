import sys

from gql.transport.exceptions import TransportQueryError

from bayes.client.base import BayesGQLClient
from bayes.model.dataset import Dataset
from bayes.model.dataset_version import DatasetVersion


def get_datasets(client: BayesGQLClient, party_name, page):
    query = """
        query Datasets($partyId: ID!, $page: Int!) {
          party(id: $partyId) {
            datasets(page: $page) {
              data {
                status
                id
                name
                latestVersion
                size
                updatedAt
              }
            }
          }
        }
    """
    variables = {"partyId": party_name, "page": page}

    try:
        response = client.exec(query, variables)
    except TransportQueryError as e:
        error_message = e.errors[0]['message'] if e.errors else str(e)
        print(error_message, file=sys.stderr)  # 打印错误消息到标准错误流
        sys.exit(1)

    datasets_data = response.get("party", {}).get("datasets", {}).get("data", [])
    if not datasets_data:
        return None

    return [Dataset(**dataset) for dataset in datasets_data]


def get_dataset_versions(client: BayesGQLClient, id):
    query = """
    query Versions($datasetId: String!) {
      dataset(datasetId: $datasetId) {
        versions {
          version
          name
          description
          status
          deletedAt
          size
          createdAt
        }
      }
    }
    """
    variables = {"datasetId": id}
    try:
        response = client.exec(query, variables)
    except TransportQueryError as e:
        error_message = e.errors[0]['message'] if e.errors else str(e)
        print(error_message, file=sys.stderr)
        sys.exit(1)

    dataset_version_list = response.get("dataset", {}).get("versions", [])
    if not dataset_version_list:
        return None

    return [DatasetVersion(**dataset_version) for dataset_version in dataset_version_list]
