#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Mixin for all oarepo actions."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any

from invenio_requests.customizations import actions
from oarepo_runtime.i18n import lazy_gettext as _

from oarepo_requests.proxies import current_oarepo_requests

if TYPE_CHECKING:
    from flask_babel.speaklater import LazyString
    from flask_principal import Identity
    from invenio_records_resources.records import Record
    from invenio_records_resources.services.uow import UnitOfWork
    from invenio_requests.customizations import RequestType
    from invenio_requests.records.api import Request

    from oarepo_requests.actions.components import RequestActionComponent


class OARepoGenericActionMixin:
    """Mixin for all oarepo actions."""

    name: str

    @classmethod
    def stateful_name(cls, identity: Identity, **kwargs: Any) -> str | LazyString:
        """Return the name of the action.

        The name can be a lazy multilingual string and may depend on the state of the action,
        request or identity of the caller.
        """
        return cls.name

    def apply(
        self,
        identity: Identity,
        request_type: RequestType,
        topic: Any,
        uow: UnitOfWork,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Apply the action to the topic."""
        pass

    def _execute_with_components(
        self,
        components: list[RequestActionComponent],
        identity: Identity,
        request_type: RequestType,
        topic: Any,
        uow: UnitOfWork,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Execute the action with the given components.

        Each component has an apply method that must return a context manager.
        The context manager is entered and exited in the order of the components
        and the action is executed inside the most inner context manager.
        """
        if not components:
            self.apply(identity, request_type, topic, uow, *args, **kwargs)
            super().execute(identity, uow, *args, **kwargs)  # type: ignore
        else:
            with components[0].apply(
                identity, request_type, self, topic, uow, *args, **kwargs
            ):
                self._execute_with_components(
                    components[1:], identity, request_type, topic, uow, *args, **kwargs
                )

    @cached_property
    def components(self) -> list[RequestActionComponent]:
        """Return a list of components for this action."""
        return [
            component_cls()
            for component_cls in current_oarepo_requests.action_components(self)
        ]

    def execute(
        self, identity: Identity, uow: UnitOfWork, *args: Any, **kwargs: Any
    ) -> None:
        """Execute the action."""
        request: Request = self.request  # type: ignore
        request_type = request.type
        topic = request.topic.resolve()
        self._execute_with_components(
            self.components, identity, request_type, topic, uow, *args, **kwargs
        )


class AddTopicLinksOnPayloadMixin:
    """A mixin for action that takes links from the topic and stores them inside the payload."""

    self_link: str | None = None
    self_html_link: str | None = None

    def apply(
        self,
        identity: Identity,
        request_type: RequestType,
        topic: Any,
        uow: UnitOfWork,
        *args: Any,
        **kwargs: Any,
    ) -> Record:
        """Apply the action to the topic."""
        topic_dict = topic.to_dict()

        request: Request = self.request  # type: ignore

        if "payload" not in request:
            request["payload"] = {}

        # invenio does not allow non-string values in the payload, so using colon notation here
        # client will need to handle this and convert to links structure
        # can not use dot notation as marshmallow tries to be too smart and does not serialize dotted keys
        request["payload"][self.self_link] = topic_dict["links"]["self"]
        request["payload"][self.self_html_link] = topic_dict["links"]["self_html"]
        return topic._record


class OARepoSubmitAction(OARepoGenericActionMixin, actions.SubmitAction):
    """Submit action extended for oarepo requests."""

    name = _("Submit")


class OARepoDeclineAction(OARepoGenericActionMixin, actions.DeclineAction):
    """Decline action extended for oarepo requests."""

    name = _("Decline")


class OARepoAcceptAction(OARepoGenericActionMixin, actions.AcceptAction):
    """Accept action extended for oarepo requests."""

    name = _("Accept")


class OARepoCancelAction(actions.CancelAction):
    """Cancel action extended for oarepo requests."""

    status_from = ["created", "submitted"]
    status_to = "cancelled"
