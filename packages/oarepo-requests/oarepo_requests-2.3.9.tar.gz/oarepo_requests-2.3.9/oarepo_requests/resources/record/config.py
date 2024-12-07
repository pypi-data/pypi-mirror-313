#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Configuration of the record requests resource."""

from __future__ import annotations

import marshmallow as ma
from flask_resources import JSONSerializer, ResponseHandler
from invenio_records_resources.resources import RecordResourceConfig
from invenio_records_resources.resources.records.headers import etag_headers

from oarepo_requests.resources.ui import OARepoRequestsUIJSONSerializer


class RecordRequestsResourceConfig:
    """Configuration of the record requests resource.

    This configuration is merged with the configuration of a record on top of which
    the requests resource lives.
    """

    blueprint_name: str | None = (
        None  # will be merged from the record's resource config
    )

    routes = {
        "list-requests": "/<pid_value>/requests",
        "request-type": "/<pid_value>/requests/<request_type>",
    }
    request_view_args = RecordResourceConfig.request_view_args | {
        "request_type": ma.fields.Str()
    }

    @property
    def response_handlers(self) -> dict[str, ResponseHandler]:
        """Response handlers for the record requests resource."""
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                OARepoRequestsUIJSONSerializer()
            ),
            "application/json": ResponseHandler(JSONSerializer(), headers=etag_headers),
        }
