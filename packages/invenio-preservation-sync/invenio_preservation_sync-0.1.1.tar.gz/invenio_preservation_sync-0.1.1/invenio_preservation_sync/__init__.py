# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module that adds preservation sync integration to the platform.."""

from .ext import InvenioPreservationSync

__version__ = "0.1.1"

__all__ = ("__version__", "InvenioPreservationSync")
