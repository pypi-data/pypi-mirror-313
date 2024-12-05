from typing import List

from gql.transport.exceptions import TransportQueryError

from .base import BayesGQLClient

from pydantic import BaseModel
from bayes.error import Error


class OrgModel(BaseModel):
    id: str
    displayName: str


class UserOrgsModel(BaseModel):
    role: str
    org: OrgModel


def get_org(client: BayesGQLClient, org_id: str) -> OrgModel:
    query = """
        query Org($orgId: ID!) {
            org(id: $orgId) {
                id
                displayName
           }
        }
        """
    variables = {"orgId": org_id}
    try:
        response = client.exec(query, variables)
    except TransportQueryError as e:
        raise Error(e.errors[0]['message'] if e.errors else str(e))

    org_data = response.get("org")
    if org_data is None:
        raise Error("get org is none")

    return OrgModel(**org_data)


def get_user_orgs(client: BayesGQLClient, username: str) -> List[UserOrgsModel]:
    query = """
        query Orgs($username: String!) {
            user(username: $username) {
              orgs {
                role
                org {
                  id
                  displayName
                }
              }
            }
        }
    """
    variables = {"username": username}
    try:
        response = client.exec(query, variables)
    except TransportQueryError as e:
        raise Error(e.errors[0]['message'] if e.errors else str(e))

    user_orgs_data = response.get("user", {}).get("orgs")
    if not user_orgs_data:
        return None

    return [UserOrgsModel(**org) for org in user_orgs_data]
