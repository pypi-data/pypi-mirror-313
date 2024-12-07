#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Patches to invenio service to allow for more flexible requests handling."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, Callable

from flask_resources import JSONSerializer, ResponseHandler
from invenio_records_resources.resources.records.headers import etag_headers
from invenio_records_resources.services.records.params import FilterParam
from invenio_requests.resources.events.config import RequestCommentsResourceConfig
from invenio_requests.resources.requests.config import (
    RequestSearchRequestArgsSchema,
    RequestsResourceConfig,
)
from invenio_requests.services.requests.config import (
    RequestSearchOptions,
    RequestsServiceConfig,
)
from invenio_requests.services.requests.params import IsOpenParam
from invenio_search.engine import dsl
from marshmallow import fields
from opensearch_dsl.query import Bool

from oarepo_requests.resources.ui import (
    OARepoRequestEventsUIJSONSerializer,
    OARepoRequestsUIJSONSerializer,
)
from oarepo_requests.services.oarepo.config import OARepoRequestsServiceConfig

if TYPE_CHECKING:
    from flask.blueprints import BlueprintSetupState
    from flask_principal import Identity
    from flask_resources.serializers.base import BaseSerializer
    from opensearch_dsl.query import Query


class RequestOwnerFilterParam(FilterParam):
    """Filter requests by owner."""

    def apply(self, identity: Identity, search: Query, params: dict[str, str]) -> Query:
        """Apply the filter to the search."""
        value = params.pop(self.param_name, None)
        if value is not None:
            search = search.filter("term", **{self.field_name: identity.id})
        return search


class RequestNotOwnerFilterParam(FilterParam):
    """Filter requests that are not owned by the current user.

    Note: invenio still does check that the user has the right to see the request,
    so this is just a filter to narrow down the search to requests, that the user
    can approve.
    """

    def apply(self, identity: Identity, search: Query, params: dict[str, str]) -> Query:
        """Apply the filter to the search."""
        value = params.pop(self.param_name, None)
        if value is not None:
            search = search.filter(
                Bool(must_not=[dsl.Q("term", **{self.field_name: identity.id})])
            )
        return search


class IsClosedParam(IsOpenParam):
    """Get just the closed requests."""

    def apply(self, identity: Identity, search: Query, params: dict[str, str]) -> Query:
        """Evaluate the is_closed parameter on the search."""
        if params.get("is_closed") is True:
            search = search.filter("term", **{self.field_name: True})
        elif params.get("is_closed") is False:
            search = search.filter("term", **{self.field_name: False})
        return search


class EnhancedRequestSearchOptions(RequestSearchOptions):
    """Searched options enhanced with additional filters."""

    params_interpreters_cls = RequestSearchOptions.params_interpreters_cls + [
        RequestOwnerFilterParam.factory("mine", "created_by.user"),
        RequestNotOwnerFilterParam.factory("assigned", "created_by.user"),
        IsClosedParam.factory("is_closed"),
    ]


class ExtendedRequestSearchRequestArgsSchema(RequestSearchRequestArgsSchema):
    """Marshmallow schema for the extra filters."""

    mine = fields.Boolean()
    assigned = fields.Boolean()
    is_closed = fields.Boolean()


def override_invenio_requests_config(
    state: BlueprintSetupState, *args: Any, **kwargs: Any
) -> None:
    """Override the invenio requests configuration.

    This function is called from the blueprint setup function as this should be a safe moment
    to monkey patch the invenio requests configuration.
    """
    with state.app.app_context():
        # this monkey patch should be done better (support from invenio)
        RequestsServiceConfig.search = EnhancedRequestSearchOptions
        RequestsResourceConfig.request_search_args = (
            ExtendedRequestSearchRequestArgsSchema
        )
        # add extra links to the requests
        for k, v in OARepoRequestsServiceConfig.links_item.items():
            if k not in RequestsServiceConfig.links_item:
                RequestsServiceConfig.links_item[k] = v

        class LazySerializer:
            def __init__(self, serializer_cls: type[BaseSerializer]) -> None:
                self.serializer_cls = serializer_cls

            @cached_property
            def __instance(self) -> BaseSerializer:
                return self.serializer_cls()

            @property
            def serialize_object_list(self) -> Callable:
                return self.__instance.serialize_object_list

            @property
            def serialize_object(self) -> Callable:
                return self.__instance.serialize_object

        RequestsResourceConfig.response_handlers = {
            "application/json": ResponseHandler(JSONSerializer(), headers=etag_headers),
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                LazySerializer(OARepoRequestsUIJSONSerializer), headers=etag_headers
            ),
        }

        RequestCommentsResourceConfig.response_handlers = {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                LazySerializer(OARepoRequestEventsUIJSONSerializer),
                headers=etag_headers,
            ),
            **RequestCommentsResourceConfig.response_handlers,
        }

        from invenio_requests.proxies import current_request_type_registry
        from invenio_requests.services.requests.facets import status, type
        from oarepo_runtime.i18n import lazy_gettext as _

        status._value_labels = {
            "submitted": _("Submitted"),
            "expired": _("Expired"),
            "accepted": _("Accepted"),
            "declined": _("Declined"),
            "cancelled": _("Cancelled"),
        }
        status._label = _("Request status")

        # add extra request types dynamically
        type._value_labels = {
            rt.type_id: rt.name for rt in iter(current_request_type_registry)
        }
        type._label = _("Type")
