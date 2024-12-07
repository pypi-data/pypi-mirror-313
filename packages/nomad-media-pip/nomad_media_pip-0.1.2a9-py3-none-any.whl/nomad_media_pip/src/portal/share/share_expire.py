"""
This module contains the logic to expire a share.

Functions:
    _share_expire: expire a share
"""

from nomad_media_pip.src.helpers.send_request import _send_request


def _share_expire(self, share_id: str) -> None:
    """
    Expire a share

    Args:
        share_id (str): The share id of the shareExpire.

    Returns:
        Unknown Type: If the request succeeds.
    Exceptions:
        InvalidAPITypeException: If the API type is not portal.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/share/expire/{share_id}"

    return _send_request(self, "Share Expire", api_url, "POST", None, None)
