#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Actions for delete published record request."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from oarepo_runtime.datastreams.utils import get_record_service_for_record
from oarepo_runtime.i18n import lazy_gettext as _

from .cascade_events import cancel_requests_on_topic_delete
from .generic import OARepoAcceptAction, OARepoDeclineAction

if TYPE_CHECKING:
    from flask_principal import Identity
    from invenio_drafts_resources.records import Record
    from invenio_records_resources.services.uow import UnitOfWork
    from invenio_requests.customizations import RequestType


class DeletePublishedRecordAcceptAction(OARepoAcceptAction):
    """Accept request for deletion of a published record and delete the record."""

    name = _("Permanently delete")

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
        topic_service = get_record_service_for_record(topic)
        if not topic_service:
            raise KeyError(f"topic {topic} service not found")
        topic_service.delete(identity, topic["id"], *args, uow=uow, **kwargs)
        cancel_requests_on_topic_delete(self.request, topic, uow)


class DeletePublishedRecordDeclineAction(OARepoDeclineAction):
    """Decline request for deletion of a published record."""

    name = _("Keep the record")
