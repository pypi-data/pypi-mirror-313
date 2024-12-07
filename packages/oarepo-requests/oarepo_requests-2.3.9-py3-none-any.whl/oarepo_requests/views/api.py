#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""API views."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Blueprint, Flask


def create_oarepo_requests(app: Flask) -> Blueprint:
    """Create requests blueprint."""
    ext = app.extensions["oarepo-requests"]
    blueprint = ext.requests_resource.as_blueprint()

    from oarepo_requests.invenio_patches import override_invenio_requests_config

    blueprint.record_once(override_invenio_requests_config)

    return blueprint


def create_oarepo_requests_events(app: Flask) -> Blueprint:
    """Create events blueprint."""
    ext = app.extensions["oarepo-requests"]
    blueprint = ext.request_events_resource.as_blueprint()
    return blueprint
