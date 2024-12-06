import pytest
from unittest.mock import MagicMock
from footium_api.queries import get_all_clubs_basic_info
from footium_api.gql_connection import GqlConnection

@pytest.fixture
def gql_connection():
    return MagicMock(spec=GqlConnection)

def test_get_all_clubs_basic_info_success(gql_connection):
    mock_response = {'allClubsBasicInfo': [{'id': '1', 'name': 'Club One'}, {'id': '2', 'name': 'Club Two'}]}
    gql_connection.send_query.return_value = mock_response

    wallet_address = "0x123"
    result = get_all_clubs_basic_info(gql_connection, wallet_address)

    assert result == mock_response['allClubsBasicInfo']
    gql_connection.send_query.assert_called_once_with(
        """
query AllClubsBasicInfo ($ownerAddress: String!){
  allClubsBasicInfo (ownerAddress: $ownerAddress){
    id
    name
  }
}
""",
        {"ownerAddress": wallet_address}
    )

def test_get_all_clubs_basic_info_failure(gql_connection):
    gql_connection.send_query.side_effect = Exception("Query failed")

    wallet_address = "0x123"
    with pytest.raises(Exception):
        get_all_clubs_basic_info(gql_connection, wallet_address)
