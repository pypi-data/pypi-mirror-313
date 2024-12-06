# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Models for Preservation Sync integration."""

import uuid
from enum import Enum

from invenio_db import db
from invenio_webhooks.models import Event
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils.models import Timestamp
from sqlalchemy_utils.types import ChoiceType, JSONType, UUIDType

from .errors import (
    InvalidStatusError,
    PreservationAlreadyReceivedError,
    PreservationInfoNotFoundError,
)


class PreservationStatus(str, Enum):
    """Constants for possible statuses of a preservation."""

    __order__ = "PRESERVED PROCESSING FAILED DELETED"

    PRESERVED = "P"
    """Record was successfully processed and preserved."""

    PROCESSING = "I"
    """Record is still being processed."""

    FAILED = "F"
    """Record preservation has failed."""

    DELETED = "D"
    """Record preservation has been deleted."""

    def __eq__(self, other):
        """Equality test."""
        return self.value == other

    def __str__(self):
        """Return its value."""
        return self.value


class PreservationInfoModel(db.Model, Timestamp):
    """Information about the preservation."""

    __tablename__ = "preservation_info"

    id = db.Column(
        UUIDType,
        primary_key=True,
        default=uuid.uuid4,
    )
    """Preservation Info identifier."""

    object_uuid = db.Column(
        UUIDType,
        index=True,
        nullable=False,
        unique=False,
    )
    """Weak reference to a record identifier."""

    revision_id = db.Column(
        db.Integer,
        index=True,
        nullable=True,
        unique=False,
    )

    status = db.Column(
        ChoiceType(PreservationStatus, impl=db.CHAR(1)),
        nullable=False,
    )
    """Status of the preservation, e.g. 'preserved', 'processing', 'failed', etc."""

    harvest_timestamp = db.Column(
        db.DateTime,
        unique=False,
        index=False,
        nullable=True,
    )
    """Timestamp when the record's data was harvested."""

    archive_timestamp = db.Column(
        db.DateTime,
        unique=False,
        index=True,
        nullable=True,
    )
    """Timestamp when the record was archived."""

    uri = db.Column(db.String(255), unique=False, index=False, nullable=True)
    """URI to the preserved record."""

    path = db.Column(db.String(255), unique=False, index=False, nullable=True)
    """Path to the preserved record."""

    event_id = db.Column(UUIDType, db.ForeignKey(Event.id), nullable=True)
    """Incoming webhook event identifier."""

    description = db.Column(
        db.JSON()
        .with_variant(
            postgresql.JSONB(none_as_null=True),
            "postgresql",
        )
        .with_variant(
            JSONType(),
            "sqlite",
        )
        .with_variant(
            JSONType(),
            "mysql",
        ),
        default=lambda: dict(),
        nullable=True,
    )
    """Additional details in JSON format"""

    event = db.relationship(Event)

    @classmethod
    def create(cls, object_uuid, data, event_id):
        """Create a preservation info object."""
        status = cls._convert_status(data["status"])
        obj = cls(
            object_uuid=object_uuid,
            revision_id=data.get("revision_id"),
            status=status,
            harvest_timestamp=data.get("harvest_timestamp"),
            archive_timestamp=data.get("archive_timestamp"),
            uri=data.get("uri"),
            path=data.get("path"),
            event_id=event_id,
            description=data.get("description"),
        )
        return obj

    @classmethod
    def get(cls, object_uuid, latest=False, pid=None):
        """Get preservation info by object uuid."""
        obj = cls.query.filter_by(object_uuid=object_uuid).order_by(
            cls.created.desc(),
            cls.revision_id.desc(),
            cls.archive_timestamp.desc(),
        )
        results = obj.first() if latest else obj.all()
        if not results and latest:
            raise PreservationInfoNotFoundError(pid=pid)
        return results

    @classmethod
    def get_existing_preservation(cls, object_uuid, data):
        """Return preservation info if it already exists."""
        if data.get("revision_id") and data.get("archive_timestamp"):
            return PreservationInfoModel.query.filter_by(
                object_uuid=object_uuid,
                revision_id=data.get("revision_id"),
                archive_timestamp=data.get("archive_timestamp"),
            ).first()
        return None

    @classmethod
    def update_existing_preservation(
        cls,
        obj,
        data,
        event_id=None,
    ):
        """Update existing preservation."""
        status = cls._convert_status(data["status"])

        if (
            obj.status == status
            and obj.harvest_timestamp == data.get("harvest_timestamp")
            and obj.uri == data.get("uri")
            and obj.path == data.get("path")
            and obj.description == data.get("description")
        ):
            raise PreservationAlreadyReceivedError(data["pid"])

        obj.status = status
        obj.harvest_timestamp = data.get("harvest_timestamp")
        obj.uri = data.get("uri")
        obj.path = data.get("path")
        obj.description = data.get("description")
        obj.event_id = event_id

        return obj

    @classmethod
    def _convert_status(cls, value):
        """Convert the status of the preservation info."""
        if isinstance(value, PreservationStatus):
            return value
        elif isinstance(value, str):
            return PreservationStatus(value.upper())
        else:
            raise InvalidStatusError(
                f"Status value must be a PreservationStatus or a string. Got {value}"
            )
