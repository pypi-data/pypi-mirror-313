# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module that adds Preservation Sync integration to the platform."""

from flask.blueprints import Blueprint

from . import config
from .resources import PreservationInfoResource, PreservationInfoResourceConfig
from .services import PreservationInfoService
from .services.config import PreservationInfoServiceConfig

blueprint = Blueprint(
    "invenio_preservation_sync",
    __name__,
    template_folder="templates",
)


class InvenioPreservationSync(object):
    """Invenio-Preservation-Sync extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        self.init_service(app)
        self.init_resources(app)
        app.extensions["invenio-preservation-sync"] = self
        if self.is_enabled(app):
            app.register_blueprint(self.preservation_info_resource.as_blueprint())
            app.register_blueprint(blueprint)

    def init_service(self, app):
        """Initialize the service."""
        self.service = PreservationInfoService(
            config=PreservationInfoServiceConfig,
            perm_policy_cls=app.config["PRESERVATION_SYNC_PERMISSION_POLICY"],
        )

    def init_resources(self, app):
        """Initialize the resources for preservation info."""
        self.preservation_info_resource = PreservationInfoResource(
            config=PreservationInfoResourceConfig,
            service=self.service,
            latest_path=app.config["PRESERVATION_SYNC_GET_LATEST_PATH"],
            list_path=app.config["PRESERVATION_SYNC_GET_LIST_PATH"],
        )

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("PRESERVATION_SYNC_"):
                app.config.setdefault(k, getattr(config, k))

    def is_enabled(self, app):
        """Return whether the extension is enabled."""
        return app.config["PRESERVATION_SYNC_ENABLED"]
