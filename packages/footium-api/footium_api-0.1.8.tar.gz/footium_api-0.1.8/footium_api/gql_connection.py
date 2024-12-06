from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from box import Box
from gql.transport.exceptions import TransportQueryError
from .report import ReportStrategy, LogReportStrategy
from typing import Optional, Dict, Any, Union
from tenacity import retry, stop_after_attempt, wait_exponential


class GqlConnection:
    def __init__(
        self,
        url: str = "https://live.api.footium.club/api/graphql",
        load_schema: Optional[str] = None,
        report_strategy: ReportStrategy = LogReportStrategy(),
    ):
        self.url = url
        self.report = report_strategy
        self.transport = RequestsHTTPTransport(
            url=self.url,
            use_json=True,
        )
        if load_schema is None:
            self.client = Client(transport=self.transport)
        else:
            try:
                with open(load_schema) as f:
                    schema_str = f.read()
                self.client = Client(transport=self.transport, schema=schema_str)
            except Exception:
                self.client = Client(
                    transport=self.transport, fetch_schema_from_transport=True
                )

    def print_error(retry_state):
        exception = retry_state.outcome.exception()
        print(f"Attempt {retry_state.attempt_number} failed with error: {exception}")

    @retry(
        stop=stop_after_attempt(8),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        before_sleep=print_error
    )
    def send_query(
        self, 
        query: str, 
        variables: Optional[Dict[str, Any]] = None, 
        operation_name: Optional[str] = None
    ) -> Box:
        gql_query = gql(query)
        response = self.client.execute(
            gql_query, variable_values=variables, operation_name=operation_name
        )
        boxed_response = Box(response)
        return boxed_response

    @retry(
        stop=stop_after_attempt(8),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        before_sleep=print_error
    )
    def send_paging_query(
        self, 
        query: str, 
        variables: Dict[str, Any] = None, 
        operation_name: Optional[str] = None, 
        skip: int = 0, 
        page_size: int = 20, 
        take: Optional[int] = None
    ) -> Union[Box, list]:
        gql_query = gql(query)
        results = None
        count = 0
        variables = variables or {}
        while True:
            variables["skip"] = skip
            variables["take"] = page_size
            response = self.client.execute(
                gql_query, variable_values=variables, operation_name=operation_name
            )
            boxed_response = Box(response)
            if len(list(boxed_response.keys())) != 1:
                raise NotImplementedError(
                    f"send_paging_query only supports single key, got {len(list(boxed_response.keys()))}"
                )
            key = list(boxed_response.keys())[0]
            boxed_response = boxed_response[key]
            if results is None:
                results = boxed_response
            else:
                results.extend(boxed_response)
            count += len(boxed_response)
            if take is not None and count >= take:
                break
            if len(boxed_response) < page_size:
                break
            skip += page_size
        return results

    @retry(
        stop=stop_after_attempt(8),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        before_sleep=print_error
    )
    def send_mutation(
        self, 
        query: str, 
        variables: Optional[Dict[str, Any]] = None, 
        operation_name: Optional[str] = None
    ) -> Box:
        gql_query = gql(query)
        try:
            response = self.client.execute(
                gql_query, variable_values=variables, operation_name=operation_name
            )
            boxed_response = Box(response["submitAction"])
        except TransportQueryError as e:
            response = {
                "code": "500",
                "error": "Internal Server Error",
                "message": str(e),
                "__typename": "Error",
            }
            boxed_response = Box(response)
        return boxed_response
