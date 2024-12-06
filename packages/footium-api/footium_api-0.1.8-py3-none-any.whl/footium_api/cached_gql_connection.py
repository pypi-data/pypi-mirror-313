import diskcache as dc
from box import Box
from typing import Optional, Dict, Any, Union
from .gql_connection import GqlConnection

class CachedGqlConnection:
    def __init__(self, gql_connection: GqlConnection, ttl: int = 300, cache_dir: str = './cache'):
        self.gql_connection = gql_connection
        self.cache = dc.Cache(cache_dir)
        self.ttl = ttl

    def _cache_key(self, *args, **kwargs):
        """Generate a cache key based on query and variables."""
        return str(args) + str(kwargs)

    def send_query(
        self, 
        query: str, 
        variables: Optional[Dict[str, Any]] = None, 
        operation_name: Optional[str] = None
    ) -> Box:
        key = self._cache_key(query, variables, operation_name)
        if key in self.cache:
            return self.cache[key]

        result = self.gql_connection.send_query(query, variables, operation_name)
        self.cache.set(key, result, expire=self.ttl)
        return result

    def send_paging_query(
        self, 
        query: str, 
        variables: Dict[str, Any] = None, 
        operation_name: Optional[str] = None, 
        skip: int = 0, 
        page_size: int = 20, 
        take: Optional[int] = None
    ) -> Union[Box, list]:
        key = self._cache_key(query, variables, operation_name, skip, page_size, take)
        if key in self.cache:
            return self.cache[key]

        result = self.gql_connection.send_paging_query(query, variables, operation_name, skip, page_size, take)
        self.cache.set(key, result, expire=self.ttl)
        return result

    def send_mutation(
        self, 
        query: str, 
        variables: Optional[Dict[str, Any]] = None, 
        operation_name: Optional[str] = None
    ) -> Box:
        return self.gql_connection.send_mutation(query, variables, operation_name)
