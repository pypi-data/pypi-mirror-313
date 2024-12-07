#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Publish draft request type."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import marshmallow as ma
from invenio_records_resources.services.uow import RecordCommitOp, UnitOfWork
from invenio_requests.proxies import current_requests_service
from oarepo_runtime.datastreams.utils import get_record_service_for_record
from oarepo_runtime.i18n import lazy_gettext as _
from typing_extensions import override

from oarepo_requests.actions.publish_draft import (
    PublishDraftAcceptAction,
    PublishDraftDeclineAction,
    PublishDraftSubmitAction,
)

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


class PublishDraftRequestType(NonDuplicableOARepoRequestType):
    """Publish draft request type."""

    type_id = "publish_draft"
    name = _("Publish draft")
    payload_schema = {
        "published_record.links.self": ma.fields.Str(
            attribute="published_record:links:self",
            data_key="published_record:links:self",
        ),
        "published_record.links.self_html": ma.fields.Str(
            attribute="published_record:links:self_html",
            data_key="published_record:links:self_html",
        ),
        "version": ma.fields.Str(),
    }

    form = {
        "field": "version",
        "ui_widget": "Input",
        "props": {
            "label": _("Resource version"),
            "placeholder": _("Write down the version (first, second…)."),
            "required": False,
        },
    }

    @classproperty
    def available_actions(cls) -> dict[str, type[RequestAction]]:
        """Return available actions for the request type."""
        return {
            **super().available_actions,
            "submit": PublishDraftSubmitAction,
            "accept": PublishDraftAcceptAction,
            "decline": PublishDraftDeclineAction,
        }

    description = _("Request publishing of a draft")
    receiver_can_be_none = True
    allowed_topic_ref_types = ModelRefTypes(published=True, draft=True)

    editable = False  # type: ignore

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
        """Check if the request can be created."""
        if not topic.is_draft:
            raise ValueError("Trying to create publish request on published record")
        super().can_create(identity, data, receiver, topic, creator, *args, **kwargs)
        self.validate_topic(identity, topic)

    @classmethod
    def validate_topic(cls, identity: Identity, topic: Record) -> None:
        """Validate the topic.

        :param: identity: identity of the caller
        :param: topic: topic of the request

        :raises: ValidationError: if the topic is not valid
        """
        topic_service = get_record_service_for_record(topic)
        topic_service.validate_draft(identity, topic["id"])

        # if files support is enabled for this topic, check if there are any files
        if hasattr(topic, "files"):
            can_toggle_files = topic_service.check_permission(
                identity, "manage_files", record=topic
            )
            draft_files = topic.files  # type: ignore
            if draft_files.enabled and not draft_files.items():
                if can_toggle_files:
                    my_message = _(
                        "Missing uploaded files. To disable files for this record please mark it as metadata-only."
                    )
                else:
                    my_message = _("Missing uploaded files.")

                raise ma.ValidationError({"files.enabled": [my_message]})

    @classmethod
    def is_applicable_to(
        cls, identity: Identity, topic: Record, *args: Any, **kwargs: Any
    ) -> bool:
        """Check if the request type is applicable to the topic."""
        if not topic.is_draft:
            return False
        super_ = super().is_applicable_to(identity, topic, *args, **kwargs)
        return super_

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
            return _("Publish draft")
        if not request:
            return _("Submit for review")
        match request.status:
            case "submitted":
                return _("Submitted for review")
            case _:
                return _("Submit for review")

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
            return _(
                "Click to immediately publish the draft. "
                "The draft will be a subject to embargo as requested in the side panel. "
                "Note: The action is irreversible."
            )

        if not request:
            return _(
                "By submitting the draft for review you are requesting the publication of the draft. "
                "The draft will become locked and no further changes will be possible until the request "
                "is accepted or declined. You will be notified about the decision by email."
            )
        match request.status:
            case "submitted":
                if request_identity_matches(request.created_by, identity):
                    return _(
                        "The draft has been submitted for review. "
                        "It is now locked and no further changes are possible. "
                        "You will be notified about the decision by email."
                    )
                if request_identity_matches(request.receiver, identity):
                    return _(
                        "The draft has been submitted for review. "
                        "You can now accept or decline the request."
                    )
                return _("The draft has been submitted for review.")
            case _:
                if request_identity_matches(request.created_by, identity):
                    return _(
                        "Submit for review. After submitting the draft for review, "
                        "it will be locked and no further modifications will be possible."
                    )
                return _("Request not yet submitted.")
