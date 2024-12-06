# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio-Preservation-Sync errors."""

import marshmallow as ma
from flask_resources import HTTPJSONException, create_error_handler
from invenio_pidstore.errors import PIDDoesNotExistError


class PreservationSyncError(Exception):
    """General Preservation-Sync error."""


class PermissionDeniedError(PreservationSyncError):
    """Not authorized to read preservation info."""

    message = "User does not have permission for the requested action: {action}."

    def __init__(self, action=None, message=None):
        """Constructor."""
        self.message = self.message.format(action=action)
        super().__init__(message or self.message.format(action=action))


class PreservationAlreadyReceivedError(PreservationSyncError):
    """Same preservation info already received error."""

    message = (
        "The same preservation info has already been received for the given PID: {pid}."
    )

    def __init__(self, pid=None, message=None):
        """Constructor."""
        self.message = self.message.format(pid=pid)
        super().__init__(message or self.message)


class PreservationInfoNotFoundError(PreservationSyncError):
    """Preservation Info not found error."""

    message = "No preservation info was found for the PID: {pid}."

    def __init__(self, pid=None, message=None):
        """Constructor."""
        self.message = self.message.format(pid=pid)
        super().__init__(message or self.message)


class InvalidStatusError(PreservationSyncError):
    """Invalid status error."""

    message = "The given status was not valid: {status}."

    def __init__(self, status=None, message=None):
        """Constructor."""
        self.message = self.message.format(status=status)
        super().__init__(message or self.message)


class ModuleDisabledError(PreservationSyncError):
    """Module disabled error."""

    message = "The preservation-sync module is not enabled, see PRESERVATION_SYNC_ENABLED config"

    def __init__(self, message=None):
        """Constructor."""
        super().__init__(message or self.message)


class ErrorHandlersMixin:
    """Mixin to define error handlers."""

    error_handlers = {
        InvalidStatusError: create_error_handler(
            lambda e: HTTPJSONException(
                code=400,
                description=e.message,
            )
        ),
        ma.ValidationError: create_error_handler(
            lambda e: HTTPJSONException(
                code=400,
                description=e.message,
            )
        ),
        PermissionDeniedError: create_error_handler(
            lambda e: HTTPJSONException(
                code=403,
                description=e.message,
            )
        ),
        PreservationInfoNotFoundError: create_error_handler(
            lambda e: HTTPJSONException(
                code=404,
                description=e.message,
            )
        ),
        PIDDoesNotExistError: create_error_handler(
            lambda e: HTTPJSONException(
                code=404,
                description=str(e),
            )
        ),
        AssertionError: create_error_handler(
            lambda e: HTTPJSONException(
                code=503,
                description=str(e),
            )
        ),
    }
