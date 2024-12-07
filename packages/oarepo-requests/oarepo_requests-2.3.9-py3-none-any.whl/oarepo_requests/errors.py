#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Errors raised by oarepo-requests."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from oarepo_workflows.errors import (
    EventTypeNotInWorkflow as WorkflowEventTypeNotInWorkflow,
)
from oarepo_workflows.errors import (
    RequestTypeNotInWorkflow as WorkflowRequestTypeNotInWorkflow,
)
from typing_extensions import deprecated

if TYPE_CHECKING:
    from invenio_records_resources.records import Record
    from invenio_requests.customizations import RequestType


@deprecated(
    "This exception is deprecated. Use oarepo_workflows.errors.RequestTypeNotInWorkflow instead."
)
class EventTypeNotInWorkflow(WorkflowEventTypeNotInWorkflow):
    """Raised when an event type is not in the workflow."""

    ...


@deprecated(
    "This exception is deprecated. Use oarepo_workflows.errors.RequestTypeNotInWorkflow instead."
)
class RequestTypeNotInWorkflow(WorkflowRequestTypeNotInWorkflow):
    """Raised when a request type is not in the workflow."""

    ...


class OpenRequestAlreadyExists(Exception):
    """An open request already exists."""

    def __init__(self, request_type: RequestType, record: Record) -> None:
        """Initialize the exception."""
        self.request_type = request_type
        self.record = record

    @property
    def description(self) -> str:
        """Exception's description."""
        return f"There is already an open request of {self.request_type.name} on {self.record.id}."


class UnknownRequestType(Exception):
    """Exception raised when user tries to create a request with an unknown request type."""

    def __init__(self, request_type: str) -> None:
        """Initialize the exception."""
        self.request_type = request_type

    @property
    def description(self) -> str:
        """Exception's description."""
        return f"Unknown request type {self.request_type}."


class ReceiverNonReferencable(Exception):
    """Raised when receiver is required but could not be estimated from the record/caller."""

    def __init__(
        self, request_type: RequestType, record: Record, **kwargs: Any
    ) -> None:
        """Initialize the exception."""
        self.request_type = request_type
        self.record = record
        self.kwargs = kwargs

    @property
    def description(self) -> str:
        """Exception's description."""
        message = f"Receiver for request type {self.request_type} is required but wasn't successfully referenced on record {self.record['id']}."
        if self.kwargs:
            message += "\n Additional keyword arguments:"
            message += f"\n{', '.join(self.kwargs)}"
        return message
