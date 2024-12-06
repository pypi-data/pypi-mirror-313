# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Utils for Preservation Sync module."""

from flask import current_app, g, url_for
from flask_principal import ActionNeed
from invenio_access import Permission
from invenio_i18n import lazy_gettext as _

from invenio_preservation_sync.models import PreservationStatus

from .proxies import current_preservation_sync_service as service


def preservation_info_render(record):
    """Render the preservation info."""
    permission = Permission(ActionNeed("superuser-access"))
    is_superuser = permission.allows(g.identity)

    pid = record._record.pid.pid_value
    result = service.read(g.identity, pid, latest=True).data

    if not result or result["status"] != PreservationStatus.PRESERVED:
        return []

    title = current_app.config.get(
        "PRESERVATION_SYNC_UI_TITLE", _("Preservation Platform")
    )
    url = None
    if is_superuser:
        url = result["uri"]
    info_link = current_app.config.get("PRESERVATION_SYNC_UI_INFO_LINK", None)
    icon_path = current_app.config.get("PRESERVATION_SYNC_UI_ICON_PATH", None)

    return [
        {
            "content": {
                "url": url,
                "title": title,
                "info_link": info_link,
                "icon": (url_for("static", filename=icon_path) if icon_path else None),
                "section": _("Preserved in"),
            },
            "template": "invenio_preservation_sync/preservation_link.html",
        }
    ]
