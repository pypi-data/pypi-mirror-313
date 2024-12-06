# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Configs for the service layer to process the Preservation Sync requests."""

from ..models import PreservationInfoModel
from .permissions import DefaultPreservationInfoPermissionPolicy
from .results import PreservationInfoItem, PreservationInfoList
from .schemas import PreservationInfoSchema


class PreservationInfoServiceConfig(object):
    """Service factory configuration."""

    result_item_cls = PreservationInfoItem
    result_list_cls = PreservationInfoList
    permission_policy_cls = DefaultPreservationInfoPermissionPolicy
    schema = PreservationInfoSchema()

    record_cls = PreservationInfoModel
