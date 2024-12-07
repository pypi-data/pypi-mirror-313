#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Request type for requesting new version of a published record."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import marshmallow as ma
from invenio_records_resources.services.uow import RecordCommitOp, UnitOfWork
from invenio_requests.proxies import current_requests_service
from marshmallow.validate import OneOf
from oarepo_runtime.i18n import lazy_gettext as _
from typing_extensions import override

from ..actions.new_version import NewVersionAcceptAction
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


class NewVersionRequestType(NonDuplicableOARepoRequestType):
    """Request type for requesting new version of a published record."""

    type_id = "new_version"
    name = _("New Version")
    payload_schema = {
        "draft_record.links.self": ma.fields.Str(
            attribute="draft_record:links:self",
            data_key="draft_record:links:self",
        ),
        "draft_record.links.self_html": ma.fields.Str(
            attribute="draft_record:links:self_html",
            data_key="draft_record:links:self_html",
        ),
        "keep_files": ma.fields.String(validate=OneOf(["true", "false"])),
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
            "accept": NewVersionAcceptAction,
        }

    description = _("Request requesting creation of new version of a published record.")
    allowed_topic_ref_types = ModelRefTypes(published=True, draft=True)
    editable = False

    form = {
        "field": "keep_files",
        "ui_widget": "BooleanCheckbox",
        "props": {
            "label": _("Keep files:"),
            "placeholder": _("Keep files in the new version?"),
            "description": _(
                "If you choose yes, the current record's files will be linked to the new version of the record. Then you will be able to add/remove files in the form."
            ),
            "falseLabel": _("No"),
            "trueLabel": _("Yes"),
        },
    }

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
        """Check if the request can be created."""
        if topic.is_draft:
            raise ValueError(
                "Trying to create new version request on draft record"
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
            return _("Request new version access")
        match request.status:
            case "submitted":
                return _("New version access requested")
            case _:
                return _("Request new version access")

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
            return _("Click to start creating a new version of the record.")

        if not request:
            return _(
                "Request permission to update record (including files). "
                "You will be notified about the decision by email."
            )
        match request.status:
            case "submitted":
                if request_identity_matches(request.created_by, identity):
                    return _(
                        "Permission to update record (including files) requested. "
                        "You will be notified about the decision by email."
                    )
                if request_identity_matches(request.receiver, identity):
                    return _(
                        "You have been asked to approve the request to update the record. "
                        "You can approve or reject the request."
                    )
                return _("Permission to update record (including files) requested. ")
            case _:
                if request_identity_matches(request.created_by, identity):
                    return _("Submit request to get edit access to the record.")
                return _("You do not have permission to update the record.")
