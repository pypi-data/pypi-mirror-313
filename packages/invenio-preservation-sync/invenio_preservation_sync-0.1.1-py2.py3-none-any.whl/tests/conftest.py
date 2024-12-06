# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import uuid

import pytest
from flask_principal import ActionNeed
from invenio_access.models import ActionRoles
from invenio_accounts.models import Role
from invenio_app.factory import create_api as _create_api
from invenio_oauth2server.models import Token
from invenio_pidstore.errors import PIDDoesNotExistError


@pytest.fixture(scope="module")
def app_config(app_config):
    """Application config override."""
    app_config["PRESERVATION_SYNC_ENABLED"] = True
    app_config["PRESERVATION_SYNC_PID_RESOLVER"] = test_resolve_record_pid
    return app_config


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""
    return _create_api


@pytest.fixture(scope="session", autouse=True)
def generate_uuids():
    """Random generate uuids as global vars."""
    global TEST_UUID
    TEST_UUID = uuid.uuid4()


def test_resolve_record_pid(pid):
    """PID resolver."""
    if pid == "test_pid":
        return TEST_UUID
    raise PIDDoesNotExistError("recid", pid)


@pytest.fixture()
def archiver_role_need(db):
    """Store 1 role with 'archiver' ActionNeed.

    WHY: This is needed because expansion of ActionNeed is
         done on the basis of a User/Role being associated with that Need.
         If no User/Role is associated with that Need (in the DB), the
         permission is expanded to an empty list.
    """
    role = Role(name="archiver")
    db.session.add(role)

    action_role = ActionRoles.create(action=ActionNeed("archiver"), role=role)
    db.session.add(action_role)
    db.session.commit()

    return action_role.need


@pytest.fixture()
def archiver(UserFixture, app, db, archiver_role_need):
    """Archiver user for requests."""
    u = UserFixture(
        email="archiver@inveniosoftware.org",
        password="archiver",
    )
    u.create(app, db)

    datastore = app.extensions["security"].datastore
    _, role = datastore._prepare_role_modify_args(u.user, "archiver")

    datastore.add_role_to_user(u.user, role)
    db.session.commit()
    return u


@pytest.fixture()
def access_token(app, db, archiver):
    """Fixture that create an access token."""
    token = Token.create_personal(
        "test-personal-{0}".format(archiver.user.id),
        archiver.user.id,
        scopes=["webhooks:event"],
        is_internal=True,
    ).access_token
    db.session.commit()
    return token


@pytest.fixture()
def headers():
    """Default headers for making requests."""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


@pytest.fixture()
def access_token_headers(access_token):
    """Bearer token headers for making requests."""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer " + access_token,
    }
