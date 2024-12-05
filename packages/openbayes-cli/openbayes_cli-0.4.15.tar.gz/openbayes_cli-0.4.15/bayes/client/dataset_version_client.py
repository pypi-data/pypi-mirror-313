import sys

from gql.transport.exceptions import TransportQueryError

from bayes.client.base import BayesGQLClient
from bayes.model.dataset_version import PublicDatasetVersions, DatasetVersion
from bayes.model.party import Party, JobData, DatasetVersionData


def get_public_dataset_version_for_gear_binding(client: BayesGQLClient):
    query = """
    query PublicDatasetVersions($status: [DatasetStatusInput], $tagIds: [Int!]) {
      publicDatasetVersions(status: $status, tagIds: $tagIds) {
        data {
          semanticBindingName
          createdAt
        }
      }
    }
    """
    variables = {"status": "VALID", "tagIds": [0]}
    try:
        response = client.exec(query, variables)
    except TransportQueryError as e:
        error_message = e.errors[0]['message'] if e.errors else str(e)
        print(error_message, file=sys.stderr)
        sys.exit(1)

    result = response.get("publicDatasetVersions", {}).get("data", [])
    if not result:
        return None

    return PublicDatasetVersions(data=[DatasetVersion(**dataset) for dataset in result])


def get_party_private_dataset_version_for_gear_binding(client: BayesGQLClient, party_name):
    query = """
        query Data($partyId: ID!, $status: [DatasetStatusInput]) {
          party(id: $partyId) {
            datasetVersions(status: $status) {
              data {
                semanticBindingName
                createdAt
              }
            }
          }
        }
    """
    variables = {"partyId": party_name, "status": ["ALL"]}
    try:
        response = client.exec(query, variables)
    except TransportQueryError as e:
        error_message = e.errors[0]['message'] if e.errors else str(e)
        print(error_message, file=sys.stderr)
        sys.exit(1)

    result = response.get("party", {})
    if not result or not result.get("datasetVersions"):
        return None

    return DatasetVersionData(**result["datasetVersions"])


def get_party_job_output_for_gear_binding(client: BayesGQLClient, party_name):
    query = """
      query Jobs($partyId: ID!, $status: [JobStatusInput]) {
          party(id: $partyId) {
            jobs(status: $status) {
              data {
                output {
                  path
                }
                createdAt
              }
            }
          }
        }  
    """
    variables = {"partyId": party_name, "status": ["CANCELLING","RUNNING","CANCELLED", "SUCCEEDED", "FAILED"]}
    try:
        response = client.exec(query, variables)
    except TransportQueryError as e:
        error_message = e.errors[0]['message'] if e.errors else str(e)
        print(error_message, file=sys.stderr)
        sys.exit(1)

    result = response.get("party", {})
    if not result or not result.get("jobs"):
        return None

    return JobData(**result["jobs"])
