# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Proxy for current previewer."""

from flask import current_app
from werkzeug.local import LocalProxy

current_preservation_sync = LocalProxy(
    lambda: current_app.extensions["invenio-preservation-sync"]
)
"""Helper proxy to access the Preservation Sync extension object. """

current_preservation_sync_service = LocalProxy(
    lambda: current_app.extensions["invenio-preservation-sync"].service
)
"""Helper proxy to access the Preservation Sync service. """
