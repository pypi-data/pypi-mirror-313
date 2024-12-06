# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Preservation Sync module to create REST APIs."""

from flask import g
from flask_resources import (
    Resource,
    from_conf,
    request_parser,
    resource_requestctx,
    response_handler,
    route,
)

from ..errors import ErrorHandlersMixin

request_view_args = request_parser(from_conf("request_view_args"), location="view_args")


class PreservationInfoResource(ErrorHandlersMixin, Resource):
    """Preservation Info resource."""

    def __init__(self, config, service, latest_path=None, list_path=None):
        """Constructor."""
        super().__init__(config)
        self.service = service
        self.latest_route = latest_path
        self.list_route = list_path

    def create_url_rules(self):
        """Create the URL rules for the preservation info resource.

        * **GET** latest preservation path can be configured in :attr:`invenio_preservation_sync.config.PRESERVATION_SYNC_GET_LATEST_PATH`.
            (Default: */records/<pid_id>/preservations/latest*).

        * **GET** list of preservations path can be configured in :attr:`invenio_preservation_sync.config.PRESERVATION_SYNC_GET_LIST_PATH`
             (Default: */records/<pid_id>/preservations/*).
        """
        routes = self.config.routes
        if not self.latest_route:
            self.latest_route = routes["latest"]
        if not self.list_route:
            self.list_route = routes["list"]
        return [
            route("GET", self.latest_route, self.get_latest),
            route("GET", self.list_route, self.get_list),
        ]

    @request_view_args
    @response_handler()
    def get_latest(self):
        """GET endpoint to return the latest preservation info for a given record.

        Request param: **pid_id** PersistentIdentifier ID for the record.

        :returns: Response status code, see *message* for more details

        * **200** - Latest preservation is returned as a JSON object.
        * **400** - Parameter was not valid.
        * **403** - Permission requirement was not met.
        * **404** - PID could not be resolved or there are no preservations for the given record or the module is disabled.
        * **503** - Mandatory config was missing.
        """
        pid_id = resource_requestctx.view_args["pid_id"]
        preservation = self.service.read(g.identity, pid_id, latest=True)
        return preservation.to_dict(), 200

    @request_view_args
    @response_handler()
    def get_list(self):
        """GET endpoint to return list of preservation info for a given record.

        Request param: **pid_id** PersistentIdentifier ID for the record.

        :returns: Response status code, see *message* for more details

        * **200** - List of preservations (*hits, hits*) and total number of results (*hits, total*).
            * If there are no preservation info for the given Persistent ID then it returns an empty list.
        * **400** - Params were not valid.
        * **403** - Permission requirement was not met.
        * **404** - PID could not be resolved or the module is disabled.
        * **503** - Mandatory config was missing.
        """
        pid_id = resource_requestctx.view_args["pid_id"]
        preservations = self.service.read(g.identity, pid_id)
        return preservations.to_dict(), 200
