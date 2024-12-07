#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Default configuration of oarepo-requests."""

from __future__ import annotations

import invenio_requests.config
import oarepo_workflows  # noqa
from invenio_requests.customizations import CommentEventType, LogEventType
from invenio_requests.services.permissions import (
    PermissionPolicy as InvenioRequestsPermissionPolicy,
)
from oarepo_workflows.requests.events import WorkflowEvent

from oarepo_requests.actions.components import (
    AutoAcceptComponent,
    RequestIdentityComponent,
    WorkflowTransitionComponent,
)
from oarepo_requests.resolvers.ui import (
    AutoApproveUIEntityResolver,
    FallbackEntityReferenceUIResolver,
    GroupEntityReferenceUIResolver,
    UserEntityReferenceUIResolver,
)
from oarepo_requests.types import (
    DeletePublishedRecordRequestType,
    EditPublishedRecordRequestType,
    PublishDraftRequestType,
)
from oarepo_requests.types.events import TopicDeleteEventType
from oarepo_requests.types.events.topic_update import TopicUpdateEventType

REQUESTS_REGISTERED_TYPES = [
    DeletePublishedRecordRequestType(),
    EditPublishedRecordRequestType(),
    PublishDraftRequestType(),
]

REQUESTS_REGISTERED_EVENT_TYPES = [
    TopicUpdateEventType(),
    TopicDeleteEventType(),
] + invenio_requests.config.REQUESTS_REGISTERED_EVENT_TYPES

REQUESTS_ALLOWED_RECEIVERS = ["user", "group", "auto_approve"]

DEFAULT_WORKFLOW_EVENTS = {
    CommentEventType.type_id: WorkflowEvent(
        submitters=InvenioRequestsPermissionPolicy.can_create_comment
    ),
    LogEventType.type_id: WorkflowEvent(
        submitters=InvenioRequestsPermissionPolicy.can_create_comment
    ),
    TopicUpdateEventType.type_id: WorkflowEvent(
        submitters=InvenioRequestsPermissionPolicy.can_create_comment
    ),
}


ENTITY_REFERENCE_UI_RESOLVERS = {
    "user": UserEntityReferenceUIResolver("user"),
    "fallback": FallbackEntityReferenceUIResolver("fallback"),
    "group": GroupEntityReferenceUIResolver("group"),
    "auto_approve": AutoApproveUIEntityResolver("auto_approve"),
}

REQUESTS_UI_SERIALIZATION_REFERENCED_FIELDS = ["created_by", "receiver", "topic"]

workflow_action_components = [WorkflowTransitionComponent]

REQUESTS_ACTION_COMPONENTS = {
    "accepted": [
        *workflow_action_components,
        RequestIdentityComponent,
    ],
    "submitted": [
        *workflow_action_components,
        AutoAcceptComponent,
        RequestIdentityComponent,
    ],
    "declined": [
        *workflow_action_components,
        RequestIdentityComponent,
    ],
    "cancelled": [
        *workflow_action_components,
        RequestIdentityComponent,
    ],
    "expired": [
        *workflow_action_components,
        RequestIdentityComponent,
    ],
}
