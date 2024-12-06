# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Resource endpoints tests."""

import json


def test_permission_denied(app, client, headers):
    """Test permission denied on get request."""
    r = client.get("/records/test_pid/preservations", headers=headers)
    assert r.status_code == 403
    r = client.get("/records/test_pid/preservations/latest", headers=headers)
    assert r.status_code == 403


def test_get_invalid_pid(app, client, headers):
    """Test permission denied on get request."""
    r = client.get("/records/invalid_pid/preservations", headers=headers)
    assert r.status_code == 404
    r = client.get("/records/invalid_pid/preservations/latest", headers=headers)
    assert r.status_code == 404


def test_get_preservations(app, client, archiver, headers, access_token_headers):
    """Test createm update and get preservation events."""
    client = archiver.login(client)

    r = client.get("/records/test_pid/preservations", headers=headers)
    assert r.status_code == 200
    assert r.json["hits"]["total"] == 0

    r = client.get("/records/test_pid/preservations/latest", headers=headers)
    assert r.status_code == 404

    payload = json.dumps(
        {
            "pid": "test_pid",
            "revision_id": "1",
            "status": "P",
            "uri": "https://test-archive.org/abcd",
            "path": "/test/archive/aips/abcd",
            "harvest_timestamp": "2024-07-30T23:57:18",
            "archive_timestamp": "2024-07-31T13:34:18",
            "description": {"compliance": "OAIS", "sender": "Preservation Platform"},
        }
    )

    r = client.post(
        "hooks/receivers/preservation/events",
        follow_redirects=True,
        headers=access_token_headers,
        data=payload,
    )
    assert r.status_code == 202

    r = client.get("/records/test_pid/preservations", headers=headers)
    assert r.status_code == 200
    assert r.json["hits"]["total"] == 1
    assert r.json["hits"]["hits"][0]["revision_id"] == 1

    r = client.get("/records/test_pid/preservations/latest", headers=headers)
    assert r.status_code == 200
    assert r.json["status"] == "P"
    assert r.json["revision_id"] == 1
    assert r.json["uri"] == "https://test-archive.org/abcd"
    assert r.json["path"] == "/test/archive/aips/abcd"

    r = client.post(
        "hooks/receivers/preservation/events",
        follow_redirects=True,
        headers=access_token_headers,
        data=payload,
    )
    assert r.status_code == 409

    payload = json.dumps(
        {
            "pid": "test_pid",
            "revision_id": "1",
            "status": "P",
            "path": "new_path",
            "archive_timestamp": "2024-07-31T13:34:18",
        }
    )
    r = client.post(
        "hooks/receivers/preservation/events",
        follow_redirects=True,
        headers=access_token_headers,
        data=payload,
    )

    r = client.get("/records/test_pid/preservations", headers=headers)
    assert r.status_code == 200
    assert r.json["hits"]["total"] == 1

    r = client.get("/records/test_pid/preservations/latest", headers=headers)
    assert r.status_code == 200
    assert r.json["status"] == "P"
    assert r.json["revision_id"] == 1
    assert r.json["path"] == "new_path"

    payload = json.dumps(
        {
            "pid": "test_pid",
            "revision_id": "2",
            "status": "F",
            "harvest_timestamp": "2024-07-31T23:59:18",
            "archive_timestamp": "2024-08-01T18:34:18",
        }
    )
    r = client.post(
        "hooks/receivers/preservation/events",
        follow_redirects=True,
        headers=access_token_headers,
        data=payload,
    )
    assert r.status_code == 202

    r = client.get("/records/test_pid/preservations", headers=headers)
    assert r.status_code == 200
    assert r.json["hits"]["total"] == 2

    r = client.get("/records/test_pid/preservations/latest", headers=headers)
    assert r.status_code == 200
    assert r.json["status"] == "F"
    assert r.json["revision_id"] == 2
