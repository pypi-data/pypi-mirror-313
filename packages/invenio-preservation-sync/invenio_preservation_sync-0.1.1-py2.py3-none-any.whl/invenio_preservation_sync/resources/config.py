# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Preservation Info Resource Configuration."""

import marshmallow as ma
from flask_resources import JSONSerializer, ResourceConfig, ResponseHandler


class PreservationInfoResourceConfig(ResourceConfig):
    """Preservation Info resource config."""

    blueprint_name = "preservations"
    url_prefix = "/"
    routes = {
        "latest": "/records/<pid_id>/preservations/latest",
        "list": "/records/<pid_id>/preservations",
    }

    request_view_args = {
        "pid_id": ma.fields.String(),
    }

    response_handlers = {"application/json": ResponseHandler(JSONSerializer())}
