..
    Copyright (C) 2024 CERN.

    Invenio-Preservation-Sync is free software; you can redistribute it
    and/or modify it under the terms of the MIT License; see LICENSE file for
    more details.


Configuration
=============

.. automodule:: invenio_preservation_sync.config
   :members:


To enable the UI element in the External resources side bar element, the following has to be added to the instance configuration:

.. code-block:: python

    from invenio_preservation_sync.utils import (
        preservation_info_render,
    )

    APP_RDM_RECORD_LANDING_PAGE_EXTERNAL_LINKS = [
        {"id": "preservation", "render": preservation_info_render},
    ]