# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Receiver tests."""

import json


def test_send_invalid_pid(app, client, archiver, access_token_headers):
    """Test invalid pid preservation event request."""
    client = archiver.login(client)

    payload = json.dumps(
        {
            "pid": "not_existing_pid",
            "revision_id": "1",
            "status": "I",
            "uri": "https://test-archive.org/abcd",
            "path": "/test/archive/aips/abcd",
            "harvest_timestamp": "2024-07-31T23:59:18",
            "archive_timestamp": "2024-08-01T18:34:18",
            "description": {"compliance": "OAIS", "sender": "Preservation Platform"},
        }
    )
    r = client.post(
        "hooks/receivers/preservation/events",
        follow_redirects=True,
        headers=access_token_headers,
        data=payload,
    )
    assert r.status_code == 404


def test_send_missing_field(app, client, archiver, access_token_headers):
    """Test missing mandatory field preservation event."""
    client = archiver.login(client)

    payload = json.dumps({"pid": "test_pid"})
    r = client.post(
        "hooks/receivers/preservation/events",
        follow_redirects=True,
        headers=access_token_headers,
        data=payload,
    )
    assert r.status_code == 400


def test_send_invalid_status(app, client, archiver, access_token_headers):
    """Test invalid status preservation event."""
    client = archiver.login(client)

    payload = json.dumps({"pid": "test_pid", "revision_id": "1", "status": "invalid"})
    r = client.post(
        "hooks/receivers/preservation/events",
        follow_redirects=True,
        headers=access_token_headers,
        data=payload,
    )
    assert r.status_code == 400


def test_send_invalid_request_key(app, client, archiver, access_token_headers):
    """Test invalid request key preservation event."""
    client = archiver.login(client)

    payload = json.dumps({"invalid_key": "test_pid", "revision_id": "1", "status": "P"})
    r = client.post(
        "hooks/receivers/preservation/events",
        follow_redirects=True,
        headers=access_token_headers,
        data=payload,
    )
    assert r.status_code == 400


def test_send_missing_authorization(app, client, headers):
    """Test missing token preservation event."""
    payload = json.dumps({"pid": "test_pid", "revision_id": "1", "status": "P"})
    r = client.post(
        "hooks/receivers/preservation/events",
        follow_redirects=True,
        headers=headers,
        data=payload,
    )
    assert r.status_code == 401


def test_send_valid_minimal_event(app, client, archiver, access_token_headers):
    """Test valid preservation event."""
    client = archiver.login(client)

    payload = json.dumps({"pid": "test_pid", "status": "P"})
    r = client.post(
        "hooks/receivers/preservation/events",
        follow_redirects=True,
        headers=access_token_headers,
        data=payload,
    )
    assert r.status_code == 202

    r = client.get("/records/test_pid/preservations", headers=access_token_headers)
    assert r.status_code == 200
    assert r.json["hits"]["total"] == 1
    assert r.json["hits"]["hits"][0]["status"] == "P"
