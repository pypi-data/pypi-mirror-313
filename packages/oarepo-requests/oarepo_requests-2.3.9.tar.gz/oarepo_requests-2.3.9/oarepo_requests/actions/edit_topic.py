#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Actions for creating a draft of published record for editing metadata."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from oarepo_runtime.datastreams.utils import get_record_service_for_record

from .cascade_events import update_topic
from .generic import AddTopicLinksOnPayloadMixin, OARepoAcceptAction

if TYPE_CHECKING:
    from flask_principal import Identity
    from invenio_drafts_resources.records import Record
    from invenio_records_resources.services.uow import UnitOfWork
    from invenio_requests.customizations import RequestType


class EditTopicAcceptAction(AddTopicLinksOnPayloadMixin, OARepoAcceptAction):
    """Accept creation of a draft of a published record for editing metadata."""

    self_link = "draft_record:links:self"
    self_html_link = "draft_record:links:self_html"

    @override
    def apply(
        self,
        identity: Identity,
        request_type: RequestType,
        topic: Record,
        uow: UnitOfWork,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Apply the action, creating a draft of the record for editing metadata."""
        topic_service = get_record_service_for_record(topic)
        if not topic_service:
            raise KeyError(f"topic {topic} service not found")
        edit_topic = topic_service.edit(identity, topic["id"], uow=uow)
        update_topic(self.request, topic, edit_topic._record, uow)
        super().apply(identity, request_type, edit_topic, uow, *args, **kwargs)
