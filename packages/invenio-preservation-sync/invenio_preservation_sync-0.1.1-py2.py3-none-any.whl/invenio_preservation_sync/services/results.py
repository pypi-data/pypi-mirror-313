# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Service results."""

from flask_sqlalchemy import Pagination


class PreservationInfoItem(object):
    """PreservationInfo result item."""

    def __init__(self, obj, errors=None, links_tpl=None, schema=None):
        """Constructor."""
        self._obj = obj
        self._errors = errors
        self._links_tpl = links_tpl
        self._schema = schema
        self._data = None

    @property
    def data(self):
        """Property to get the preservation info."""
        if self._data:
            return self._data

        self._data = self._schema.dump(self._obj)

        if self._links_tpl:
            self._data["links"] = self.links

        return self._data

    def to_dict(self):
        """Get a dictionary for the preservation info result."""
        res = self.data
        if self._errors:
            res["errors"] = self._errors
        return res


class PreservationInfoList(object):
    """List of preservation info results."""

    def __init__(self, results, errors=None, links_tpl=None, schema=None):
        """Constructor."""
        self._results = results
        self._errors = errors
        self._links_tpl = links_tpl
        self._schema = schema

    @property
    def hits(self):
        """Iterator over the hits."""
        for obj in self.preservation_info_result():
            projection = self._schema.dump(obj)

            if self._links_tpl:
                projection["links"] = self._links_tpl.expand(self._identity, obj)

            yield projection

    def to_dict(self):
        """Return result as a dictionary."""
        res = {
            "hits": {
                "hits": list(self.hits),
                "total": self.total,
            }
        }

        if self._errors:
            res["errors"] = self._errors

        return res

    @property
    def total(self):
        """Get total number of results."""
        return (
            self._results.total
            if isinstance(self._results, Pagination)
            else len(self._results)
        )

    def preservation_info_result(self):
        """Get iterable preservation info list."""
        return (
            self._results.items
            if isinstance(self._results, Pagination)
            else self._results
        )
