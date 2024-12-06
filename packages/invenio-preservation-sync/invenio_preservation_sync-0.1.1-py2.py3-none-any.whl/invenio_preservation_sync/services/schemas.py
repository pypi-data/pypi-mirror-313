# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Schema class for the Preservation Info object."""

from datetime import timezone

from marshmallow import Schema, fields
from marshmallow_utils.fields import TZDateTime

from ..models import PreservationStatus


class PreservationInfoSchema(Schema):
    """Schema for a Preservation Info object."""

    pid = fields.String(required=True)
    status = fields.Enum(PreservationStatus, required=True, by_value=True)
    revision_id = fields.Integer(allow_none=True)
    archive_timestamp = TZDateTime(timezone=timezone.utc, format="iso", allow_none=True)
    harvest_timestamp = TZDateTime(timezone=timezone.utc, format="iso", allow_none=True)
    uri = fields.String(allow_none=True)
    path = fields.String(allow_none=True)
    description = fields.Dict(allow_none=True)
    event_id = fields.UUID(dump_only=True)
