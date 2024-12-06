"""
This module contains helper functions for GUIDs.

Functions:
    _new_guid: Generates a new GUID.
"""

import uuid


def _new_guid() -> str:
    return str(uuid.uuid4())
