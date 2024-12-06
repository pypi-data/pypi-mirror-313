# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Module tests."""

from flask import Flask

from invenio_preservation_sync import InvenioPreservationSync


def test_version():
    """Test version import."""
    from invenio_preservation_sync import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    ext = InvenioPreservationSync()
    assert "invenio-preservation-sync" not in app.extensions

    app = Flask("testapp")
    ext = InvenioPreservationSync(app)
    assert "invenio-preservation-sync" in app.extensions

    app = Flask("testapp")
    ext = InvenioPreservationSync()
    assert "invenio-preservation-sync" not in app.extensions
    ext.init_app(app)
    assert "invenio-preservation-sync" in app.extensions
