import os
import shutil
import pytest
from unittest.mock import patch, MagicMock
from footium_api import GqlConnection, CachedGqlConnection
from gql.transport.exceptions import TransportQueryError
from box import Box, BoxList


@pytest.fixture
def gql_connection():
    with patch('footium_api.gql_connection.Client') as MockClient:
        yield GqlConnection()
        MockClient.reset_mock()

def test_send_query_success(gql_connection):
    cached_gql_connection = CachedGqlConnection(gql_connection, ttl=0, cache_dir='./test_cache')
    mock_response = {'data': {'some_query': 'some_data'}}
    gql_connection.client.execute = MagicMock(return_value=mock_response)
    
    query = """
    query {
        some_query
    }
    """
    response = cached_gql_connection.send_query(query)
    
    assert isinstance(response, Box)
    assert response.data.some_query == 'some_data'
    gql_connection.client.execute.assert_called_once()


def test_send_query_with_variables(gql_connection):
    cached_gql_connection = CachedGqlConnection(gql_connection, ttl=0, cache_dir='./test_cache')
    mock_response = {'data': {'some_query': 'some_data'}}
    gql_connection.client.execute = MagicMock(return_value=mock_response)
    
    query = """
    query($var: String) {
        some_query(var: $var)
    }
    """
    variables = {"var": "test_value"}
    response = cached_gql_connection.send_query(query, variables=variables)
    
    assert isinstance(response, Box)
    assert response.data.some_query == 'some_data'
    gql_connection.client.execute.assert_called_once_with(
        gql_connection.client.execute.call_args[0][0],
        variable_values=variables,
        operation_name=None
    )


def test_send_paging_query(gql_connection):
    # delete the chache ./test_cache/test_send_paging_query
    test_path = os.path.join('.', 'test_cache/test_send_paging_query')
    if os.path.exists(test_path):
        shutil.rmtree(test_path)
    cached_gql_connection_ttl_300 = CachedGqlConnection(gql_connection, ttl=300, cache_dir=test_path)
    # Mock response for the first page
    mock_response_page1 = {'some_query': ['data1', 'data2']}
    # Mock response for the second page, which ends the pagination
    mock_response_page2 = {'some_query': []}
    
    gql_connection.client.execute = MagicMock(side_effect=[
        mock_response_page1, mock_response_page2,
        mock_response_page1, mock_response_page2,
        ])

    query = """
    query($skip: Int, $take: Int) {
        some_query(skip: $skip, take: $take)
    }
    """
    response = cached_gql_connection_ttl_300.send_paging_query(query, page_size=2)

    # Check that the response is a list wrapped in a BoxList
    assert isinstance(response, BoxList)
    assert len(response) == 2
    assert response[0] == 'data1'
    assert response[1] == 'data2'
    assert gql_connection.client.execute.call_count == 2  # Ensure the execute method was called twice

    # check caching
    # ...ttl_300 should load the response from the cache
    # so call_count will not be incremented (2 and not 4)
    response = cached_gql_connection_ttl_300.send_paging_query(query, page_size=2)
    assert isinstance(response, BoxList)
    assert len(response) == 2
    assert response[0] == 'data1'
    assert response[1] == 'data2'
    assert gql_connection.client.execute.call_count == 2  # Ensure the execute method was called twice




def test_send_mutation_success(gql_connection):
    cached_gql_connection = CachedGqlConnection(gql_connection, ttl=0, cache_dir='./test_cache')
    mock_response = {'submitAction': {'result': 'success'}}
    gql_connection.client.execute = MagicMock(return_value=mock_response)
    
    query = """
    mutation {
        submitAction {
            result
        }
    }
    """
    response = cached_gql_connection.send_mutation(query)
    
    assert isinstance(response, Box)
    assert response.result == 'success'
    gql_connection.client.execute.assert_called_once()


def test_send_mutation_failure(gql_connection):
    cached_gql_connection = CachedGqlConnection(gql_connection, ttl=0, cache_dir='./test_cache')
    gql_connection.client.execute = MagicMock(side_effect=TransportQueryError('Error message'))

    query = """
    mutation {
        submitAction {
            result
        }
    }
    """
    response = cached_gql_connection.send_mutation(query)
    
    assert isinstance(response, Box)
    assert response.code == '500'
    assert response.error == 'Internal Server Error'
    assert response.message == 'Error message'
    gql_connection.client.execute.assert_called_once()
