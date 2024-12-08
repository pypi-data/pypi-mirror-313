from __future__ import annotations

import requests
from typing import Optional, Tuple, Any
from grpclib.client import Channel
from glitter_proto.glitterchain.index import QueryStub as IndexQueryStub, QueryDatesetRequest, \
    QueryDatesetResponse, QueryDatesetsRequest, QueryDatesetsResponse
from glitter_proto.glitterchain.consumer import QueryStub as ConsumerQueryStub

__all__ = ["QueryNode", ]


class QueryArgument:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value


class QueryNode(IndexQueryStub, ConsumerQueryStub):
    def __init__(self, host: str, port: int, timeout: int):
        self.timeout = timeout
        self.channel = Channel(host, port)
        super().__init__(self.channel, timeout=self.timeout)

    def query(self, dataset_name: str, sql: str, arguments: list[QueryArgument] = None) -> Tuple[Any, str]:
        """
        Execute a SQL query statement against a specified QueryNode.

        Args:
            dataset_name (str): The name of the QueryNode to query.
            sql (str): The SQL query string to be executed.
            arguments (Optional[List[QueryArgument]]): 
                An optional list of QueryArgument objects to substitute into the query.
                Each argument should be an instance of QueryArgument with the necessary attributes.

        Returns:
            Tuple[Optional[str], Optional[str]]:
                A tuple containing:
                - A string representing the response text from the query execution (or an empty string in case of an error).
                - An optional string containing an error message (or None if the query was successful).

        Raises:
            requests.RequestException: If there is an issue with the HTTP request.
        """
        host, err = self.get_dataset_host(dataset_name)
        if err is not None or host == "":
            return "", err

        engine_host = f"{host}/api/v1/simple_sql_query"
        engine_param = {"sql": sql, "arguments": [arg.__dict__ for arg in arguments]}

        try:
            response = requests.post(engine_host, json=engine_param)
            response.raise_for_status()
            return response.json(), ""
        except requests.RequestException as e:
            return "", str(e)

    def get_dataset_host(self, dataset_name: str) -> Tuple[str, str]:
        """
        Retrieve the host information for a specified QueryNode.

        Args:
            dataset_name (str): The name of the QueryNode for which to retrieve the host information.

        Returns:
            Tuple[str, str]:
                A tuple containing:
                - A string representing the host(s) associated with the QueryNode (or an empty string in case of an error).
                - An string containing an error message (or an empty string if the operation was successful).
        """
        path = "/glitterchain/index/QueryNode/"
        url = f"{self.url}{path}{dataset_name}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data['hosts'], ""
        except requests.RequestException as e:
            return "", str(e)

    async def query_cpdts(
            self,
            query_cpd_ts_request: "QueryCpdTsRequest",
            *,
            timeout: Optional[float] = None,
            deadline: Optional["Deadline"] = None,
            metadata: Optional["MetadataLike"] = None
    ) -> "QueryCpdTsResponse":
        return await super().query_cpd_ts(query_cpd_ts_request, timeout=timeout, deadline=deadline, metadata=metadata)

    def close(self):
        self.channel.close()
