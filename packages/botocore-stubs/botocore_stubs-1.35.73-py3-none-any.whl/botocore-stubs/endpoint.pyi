"""
Copyright 2024 Vlad Emelianov
"""

from logging import Logger
from typing import Any, Mapping

from botocore.awsrequest import create_request_object as create_request_object
from botocore.exceptions import HTTPClientError as HTTPClientError
from botocore.history import get_global_history_recorder as get_global_history_recorder
from botocore.hooks import BaseEventHooks
from botocore.hooks import first_non_none_response as first_non_none_response
from botocore.httpsession import URLLib3Session as URLLib3Session
from botocore.model import OperationModel, ServiceModel
from botocore.response import StreamingBody as StreamingBody
from botocore.utils import get_environ_proxies as get_environ_proxies
from botocore.utils import is_valid_endpoint_url as is_valid_endpoint_url

logger: Logger = ...

history_recorder: Any
DEFAULT_TIMEOUT: int
MAX_POOL_CONNECTIONS: int

def convert_to_response_dict(http_response: Any, operation_model: OperationModel) -> Any: ...

class Endpoint:
    def __init__(
        self,
        host: str,
        endpoint_prefix: str,
        event_emitter: BaseEventHooks,
        response_parser_factory: Any | None = ...,
        http_session: URLLib3Session | None = ...,
    ) -> None:
        self.host: str
        self.http_session: URLLib3Session

    def close(self) -> None: ...
    def make_request(self, operation_model: OperationModel, request_dict: Any) -> Any: ...
    def create_request(
        self, params: Mapping[str, Any], operation_model: OperationModel | None = ...
    ) -> Any: ...
    def prepare_request(self, request: Any) -> Any: ...

class EndpointCreator:
    def __init__(self, event_emitter: BaseEventHooks) -> None: ...
    def create_endpoint(
        self,
        service_model: ServiceModel,
        region_name: str,
        endpoint_url: str,
        verify: Any | None = ...,
        response_parser_factory: Any | None = ...,
        timeout: float = ...,
        max_pool_connections: Any = ...,
        http_session_cls: type[URLLib3Session] = ...,
        proxies: Any | None = ...,
        socket_options: Any | None = ...,
        client_cert: Any | None = ...,
        proxies_config: Any | None = ...,
    ) -> Any: ...
