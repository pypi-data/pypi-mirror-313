#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""EditPublishedRecordRequestType."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import marshmallow as ma
from invenio_records_resources.services.uow import RecordCommitOp, UnitOfWork
from invenio_requests.proxies import current_requests_service
from invenio_requests.records.api import Request
from oarepo_runtime.i18n import lazy_gettext as _
from typing_extensions import override

from oarepo_requests.actions.edit_topic import EditTopicAcceptAction

from ..utils import classproperty, is_auto_approved, request_identity_matches
from .generic import NonDuplicableOARepoRequestType
from .ref_types import ModelRefTypes

if TYPE_CHECKING:
    from flask_babel.speaklater import LazyString
    from flask_principal import Identity
    from invenio_drafts_resources.records import Record
    from invenio_requests.customizations.actions import RequestAction
    from invenio_requests.records.api import Request

    from oarepo_requests.typing import EntityReference


class EditPublishedRecordRequestType(NonDuplicableOARepoRequestType):
    """Request type for requesting edit of a published record.

    This request type is used to request edit access to a published record. This access
    is restricted to the metadata of the record, not to the files.
    """

    type_id = "edit_published_record"
    name = _("Edit metadata")
    payload_schema = {
        "draft_record.links.self": ma.fields.Str(
            attribute="draft_record:links:self",
            data_key="draft_record:links:self",
        ),
        "draft_record.links.self_html": ma.fields.Str(
            attribute="draft_record:links:self_html",
            data_key="draft_record:links:self_html",
        ),
    }

    def extra_entity_links(self, request: Request, entity: dict, entity_type: str, **kwargs) -> dict:
        if request.status == "accepted" and entity_type == "topic":
            return {"topic_redirect_link": entity["links"]["edit_html"]}
        else:
            return {}

    @classproperty
    def available_actions(cls) -> dict[str, type[RequestAction]]:
        """Return available actions for the request type."""
        return {
            **super().available_actions,
            "accept": EditTopicAcceptAction,
        }

    description = _("Request re-opening of published record")
    receiver_can_be_none = True
    allowed_topic_ref_types = ModelRefTypes(published=True, draft=True)

    @classmethod
    def is_applicable_to(
        cls, identity: Identity, topic: Record, *args: Any, **kwargs: Any
    ) -> bool:
        """Check if the request type is applicable to the topic."""
        if topic.is_draft:
            return False
        return super().is_applicable_to(identity, topic, *args, **kwargs)

    def can_create(
        self,
        identity: Identity,
        data: dict,
        receiver: EntityReference,
        topic: Record,
        creator: EntityReference,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Check if the request can be created.

        :param identity:        identity of the caller
        :param data:            data of the request
        :param receiver:        receiver of the request
        :param topic:           topic of the request
        :param creator:         creator of the request
        :param args:            additional arguments
        :param kwargs:          additional keyword arguments
        """
        if topic.is_draft:
            raise ValueError(
                "Trying to create edit request on draft record"
            )  # todo - if we want the active topic thing, we have to allow published as allowed topic and have to check this somewhere else
        super().can_create(identity, data, receiver, topic, creator, *args, **kwargs)

    def topic_change(self, request: Request, new_topic: dict, uow: UnitOfWork) -> None:
        """Change the topic of the request."""
        request.topic = new_topic
        uow.register(RecordCommitOp(request, indexer=current_requests_service.indexer))

    @override
    def stateful_name(
        self,
        identity: Identity,
        *,
        topic: Record,
        request: Request | None = None,
        **kwargs: Any,
    ) -> str | LazyString:
        """Return the stateful name of the request."""
        if is_auto_approved(self, identity=identity, topic=topic):
            return self.name
        if not request:
            return _("Request edit access")
        match request.status:
            case "submitted":
                return _("Edit access requested")
            case _:
                return _("Request edit access")

    @override
    def stateful_description(
        self,
        identity: Identity,
        *,
        topic: Record,
        request: Request | None = None,
        **kwargs: Any,
    ) -> str | LazyString:
        """Return the stateful description of the request."""
        if is_auto_approved(self, identity=identity, topic=topic):
            return _("Click to start editing the metadata of the record.")

        if not request:
            return _(
                "Request edit access to the record. "
                "You will be notified about the decision by email."
            )
        match request.status:
            case "submitted":
                if request_identity_matches(request.created_by, identity):
                    return _(
                        "Edit access requested. You will be notified about "
                        "the decision by email."
                    )
                if request_identity_matches(request.receiver, identity):
                    return _(
                        "You have been requested to grant edit access to the record."
                    )
                return _("Edit access requested.")
            case _:
                return _(
                    "Request edit access to the record. "
                    "You will be notified about the decision by email."
                )
