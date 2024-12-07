#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Actions for publishing draft requests."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from invenio_access.permissions import system_identity
from invenio_records_resources.services.uow import RecordCommitOp, UnitOfWork
from oarepo_runtime.datastreams.utils import get_record_service_for_record
from oarepo_runtime.i18n import lazy_gettext as _

from .cascade_events import update_topic
from .generic import (
    AddTopicLinksOnPayloadMixin,
    OARepoAcceptAction,
    OARepoDeclineAction,
    OARepoSubmitAction,
)

if TYPE_CHECKING:
    from flask_principal import Identity
    from invenio_drafts_resources.records import Record
    from invenio_requests.customizations import RequestType
    from invenio_requests.customizations.actions import RequestAction


class PublishMixin:
    """Mixin for publish actions."""

    def can_execute(self: RequestAction) -> bool:
        """Check if the action can be executed."""
        if not super().can_execute():  # type: ignore
            return False

        try:
            from ..types.publish_draft import PublishDraftRequestType

            topic = self.request.topic.resolve()
            PublishDraftRequestType.validate_topic(system_identity, topic)
            return True
        except:  # noqa E722: used for displaying buttons, so ignore errors here
            return False


class PublishDraftSubmitAction(PublishMixin, OARepoSubmitAction):
    """Submit action for publishing draft requests."""


class PublishDraftAcceptAction(
    PublishMixin, AddTopicLinksOnPayloadMixin, OARepoAcceptAction
):
    """Accept action for publishing draft requests."""

    self_link = "published_record:links:self"
    self_html_link = "published_record:links:self_html"

    name = _("Publish")

    def apply(
        self,
        identity: Identity,
        request_type: RequestType,
        topic: Record,
        uow: UnitOfWork,
        *args: Any,
        **kwargs: Any,
    ) -> Record:
        """Publish the draft."""
        topic_service = get_record_service_for_record(topic)
        if not topic_service:
            raise KeyError(f"topic {topic} service not found")
        id_ = topic["id"]

        if "payload" in self.request and "version" in self.request["payload"]:
            topic.metadata["version"] = self.request["payload"]["version"]
            uow.register(RecordCommitOp(topic, indexer=topic_service.indexer))

        published_topic = topic_service.publish(
            identity, id_, *args, uow=uow, expand=False, **kwargs
        )
        update_topic(self.request, topic, published_topic._record, uow)
        return super().apply(
            identity, request_type, published_topic, uow, *args, **kwargs
        )


class PublishDraftDeclineAction(OARepoDeclineAction):
    """Decline action for publishing draft requests."""

    name = _("Return for correction")
