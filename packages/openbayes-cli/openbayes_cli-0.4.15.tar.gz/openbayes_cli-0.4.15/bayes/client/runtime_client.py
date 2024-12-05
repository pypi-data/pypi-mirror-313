from gql.transport.exceptions import TransportQueryError

from bayes.client.base import BayesGQLClient
from bayes.error import Error
from bayes.model.runtime import ClusterRuntime


def get_runtimes(client: BayesGQLClient, partyId, type, labels, runtimeType):
    query = """
     query NormalClusterRuntimes($partyId: String, $type: [DeployType], $labels: [String!], $runtimeType: [RuntimeType]) {
          normalClusterRuntimes(partyId: $partyId, type: $type, labels: $labels, runtimeType: $runtimeType) {
            framework
            name
            version
            type
            device
            deprecated
            labels
          }
        }
    """
    variables = {"partyId": partyId, "type": type, "labels": labels, "runtimeType": runtimeType}
    try:
        response = client.exec(query, variables)
    except TransportQueryError as e:
        raise Error(e.errors[0]['message'] if e.errors else str(e))

    runtime_data_list = response.get("normalClusterRuntimes", [])
    if runtime_data_list is None or not runtime_data_list:
        return None

    return [ClusterRuntime(**runtime_data) for runtime_data in runtime_data_list]
