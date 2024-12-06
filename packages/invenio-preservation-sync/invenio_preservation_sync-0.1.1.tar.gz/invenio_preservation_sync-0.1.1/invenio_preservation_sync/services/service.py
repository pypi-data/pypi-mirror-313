# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Service layer to process the Preservation Sync requests."""


from flask import current_app
from invenio_db.uow import ModelCommitOp, unit_of_work

from ..errors import PermissionDeniedError


class PreservationInfoService(object):
    """Invenio Preservation Sync service."""

    def __init__(self, config=None, perm_policy_cls=None):
        """Configuration."""
        self.record_cls = config.record_cls
        self.result_item = config.result_item_cls
        self.result_list = config.result_list_cls
        self.schema = config.schema
        self.permission_policy = config.permission_policy_cls
        if perm_policy_cls:
            self.permission_policy = perm_policy_cls

    @property
    def pid_resolver(self):
        """Return the pid resolver function."""
        pid_resolver_config_str = "PRESERVATION_SYNC_PID_RESOLVER"
        assert current_app.config[pid_resolver_config_str], (
            "Missing config: " + pid_resolver_config_str
        )
        return current_app.config[pid_resolver_config_str]

    def check_permission(self, identity, action_name, **kwargs):
        """Check a permission against the identity."""
        return self.permission_policy(action_name, **kwargs).allows(identity)

    def require_permission(self, identity, action_name, **kwargs):
        """Require a specific permission from the permission policy."""
        if not self.check_permission(identity, action_name, **kwargs):
            raise PermissionDeniedError(action_name)

    @unit_of_work()
    def create_or_update(
        self,
        identity,
        data,
        event_id=None,
        uow=None,
    ):
        """Process the preservation event info."""
        valid_data = self.schema.load(data)

        object_uuid = self.pid_resolver(valid_data.get("pid"))

        self.require_permission(identity, "create")

        existing_preservation = self.record_cls.get_existing_preservation(
            object_uuid=object_uuid, data=valid_data
        )

        if existing_preservation:
            preservation = self.record_cls.update_existing_preservation(
                obj=existing_preservation,
                data=valid_data,
                event_id=event_id,
            )
        else:
            preservation = self.record_cls.create(
                object_uuid=object_uuid, data=valid_data, event_id=event_id
            )

        uow.register(ModelCommitOp(preservation))
        return self.result_item(preservation, schema=self.schema)

    def read(self, identity, id, latest=False):
        """Returns preservation info based on the record id."""
        object_uuid = self.pid_resolver(id)

        self.require_permission(identity, "read")

        preservation = self.record_cls.get(object_uuid, latest=latest, pid=id)
        if latest:
            return self.result_item(preservation, schema=self.schema)
        else:
            return self.result_list(preservation, schema=self.schema)
