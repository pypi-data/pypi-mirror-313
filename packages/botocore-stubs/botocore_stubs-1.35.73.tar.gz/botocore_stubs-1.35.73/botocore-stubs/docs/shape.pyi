"""
Copyright 2024 Vlad Emelianov
"""

from typing import Any

from botocore.hooks import BaseEventHooks
from botocore.model import Shape

class ShapeDocumenter:
    EVENT_NAME: str = ...
    def __init__(
        self,
        service_name: str,
        operation_name: str,
        event_emitter: BaseEventHooks,
        context: Any = ...,
    ) -> None: ...
    def traverse_and_document_shape(
        self,
        section: Any,
        shape: Shape,
        history: Any,
        include: Any = ...,
        exclude: Any = ...,
        name: str | None = ...,
        is_required: bool = ...,
    ) -> None: ...
