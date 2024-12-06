from footium_api.gql_connection import GqlConnection


def get_all_clubs_basic_info(gql: GqlConnection, wallet_address: str):
    query = """
query AllClubsBasicInfo ($ownerAddress: String!){
  allClubsBasicInfo (ownerAddress: $ownerAddress){
    id
    name
  }
}
"""
    variables = {"ownerAddress": wallet_address}
    response = gql.send_query(query, variables)
    return response["allClubsBasicInfo"]
