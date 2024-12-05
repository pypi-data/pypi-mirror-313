from gql.transport.exceptions import TransportQueryError

from bayes.client.base import BayesGQLClient
from bayes.error import Error
from bayes.model.resource import ResourceData, Quota, Limitations


def get_resources(client: BayesGQLClient, partyId, type, labels):
    query = """
    query NormalClusterResources($partyId: String, $type: [DeployType], $labels: [String]) {
      normalClusterResources(partyId: $partyId, type: $type, labels: $labels) {
        name
        memory
        type
        cpu {
          type
          millicores
          count
        }
        disk {
          type
          size
        }
        gpu {
          verboseName
          vendor
          type
          name
          mode
          memory
          group
          description
          count
        }
        verboseName
        gpuResource
        labels
      }
    }
    """
    variables = {"partyId": partyId, "type": type, "labels": labels}
    try:
        response = client.exec(query, variables)
    except TransportQueryError as e:
        raise Error(e.errors[0]['message'] if e.errors else str(e))

    resource_data_list = response.get("normalClusterResources", [])
    if resource_data_list is None or not resource_data_list:
        return None

    return [ResourceData(**resource_data) for resource_data in resource_data_list]


def get_resource_quota(client: BayesGQLClient, partyId):
    query = """
        query Quota($partyId: ID!) {
          party(id: $partyId) {
            quota {
              computationQuota {
                value {
                  availableMinutes
                }
                key
              }
            }
          }
        }
    """
    variables = {"partyId": partyId}
    try:
        response = client.exec(query, variables)
    except TransportQueryError as e:
        raise Error(e.errors[0]['message'] if e.errors else str(e))

    result = response.get("party", {}).get("quota", {})
    if not result:
        return None

    return Quota(**result)


def get_resource_limitation(client: BayesGQLClient, partyId):
    query = """
       query Resources($partyId: ID!) {
          party(id: $partyId) {
            limitations {
              resources {
                key
                value {
                  current
                  limit
                }
              }
            }
          }
        }
    """
    variables = {"partyId": partyId}
    try:
        response = client.exec(query, variables)
    except TransportQueryError as e:
        raise Error(e.errors[0]['message'] if e.errors else str(e))

    result = response.get("party", {}).get("limitations", {})
    if not result:
        return None

    return Limitations(**result)
