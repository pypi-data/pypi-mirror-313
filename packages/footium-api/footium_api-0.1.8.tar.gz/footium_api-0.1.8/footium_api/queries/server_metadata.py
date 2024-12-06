from footium_api import GqlConnection


def get_server_timestamp(gql: GqlConnection):
    query = """
query ServerMetadataNew {
  serverMetadata {
    timestamp
  }
}
"""
    response = gql.send_query(query)
    timestamp = response.serverMetadata.timestamp
    return timestamp
