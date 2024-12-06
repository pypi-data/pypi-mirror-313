import pytest
from unittest.mock import patch, MagicMock
from footium_api.gql_connection import GqlConnection
from gql.transport.exceptions import TransportQueryError
from box import Box, BoxList


@pytest.fixture
def gql_connection():
    with patch('footium_api.gql_connection.Client') as MockClient:
        yield GqlConnection()
        MockClient.reset_mock()


def test_send_query_success(gql_connection):
    mock_response = {'data': {'some_query': 'some_data'}}
    gql_connection.client.execute = MagicMock(return_value=mock_response)
    
    query = """
    query {
        some_query
    }
    """
    response = gql_connection.send_query(query)
    
    assert isinstance(response, Box)
    assert response.data.some_query == 'some_data'
    gql_connection.client.execute.assert_called_once()


def test_send_query_with_variables(gql_connection):
    mock_response = {'data': {'some_query': 'some_data'}}
    gql_connection.client.execute = MagicMock(return_value=mock_response)
    
    query = """
    query($var: String) {
        some_query(var: $var)
    }
    """
    variables = {"var": "test_value"}
    response = gql_connection.send_query(query, variables=variables)
    
    assert isinstance(response, Box)
    assert response.data.some_query == 'some_data'
    gql_connection.client.execute.assert_called_once_with(
        gql_connection.client.execute.call_args[0][0],
        variable_values=variables,
        operation_name=None
    )


def test_send_paging_query(gql_connection):
    # Mock response for the first page
    mock_response_page1 = {'some_query': ['data1', 'data2']}
    # Mock response for the second page, which ends the pagination
    mock_response_page2 = {'some_query': []}
    
    gql_connection.client.execute = MagicMock(side_effect=[mock_response_page1, mock_response_page2])

    query = """
    query($skip: Int, $take: Int) {
        some_query(skip: $skip, take: $take)
    }
    """
    response = gql_connection.send_paging_query(query, page_size=2)

    # Check that the response is a list wrapped in a BoxList
    assert isinstance(response, BoxList)
    assert len(response) == 2
    assert response[0] == 'data1'
    assert response[1] == 'data2'
    assert gql_connection.client.execute.call_count == 2  # Ensure the execute method was called twice



def test_send_mutation_success(gql_connection):
    mock_response = {'submitAction': {'result': 'success'}}
    gql_connection.client.execute = MagicMock(return_value=mock_response)
    
    query = """
    mutation {
        submitAction {
            result
        }
    }
    """
    response = gql_connection.send_mutation(query)
    
    assert isinstance(response, Box)
    assert response.result == 'success'
    gql_connection.client.execute.assert_called_once()


def test_send_mutation_failure(gql_connection):
    gql_connection.client.execute = MagicMock(side_effect=TransportQueryError('Error message'))
    
    query = """
    mutation {
        submitAction {
            result
        }
    }
    """
    response = gql_connection.send_mutation(query)
    
    assert isinstance(response, Box)
    assert response.code == '500'
    assert response.error == 'Internal Server Error'
    assert response.message == 'Error message'
    gql_connection.client.execute.assert_called_once()
