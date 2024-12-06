"""
This module contains the function to update user.

Functions:
    _update_user: Updates user.
"""

import logging

from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.portal.account_updates.get_lookups import _get_lookups
from nomad_media_pip.src.portal.account_updates.get_user import _get_user


def _update_user(
    self,
    address: str | None,
    address2: str | None,
    city: str | None,
    first_name: str | None,
    last_name: str | None,
    phone_number: str | None,
    phone_ext: str | None,
    postal_code: str | None,
    organization: str | None,
    country: str | None,
    state: str | None
) -> dict | None:
    """
    Updates the user.

    Args:
        ADDRESS (str | None): The address of the user.
        ADDRESS2 (str | None): The second address of the user.
        CITY (str | None): The city of the user.
        FIRST_NAME (str | None): The first name of the user.
        LAST_NAME (str | None): The last name of the user.
        PHONE_NUMBER (str | None): The phone number of the user.
        PHONE_EXT (str | None): The phone extension of the user.
        POSTAL_CODE (str | None): The postal code of the user.
        ORGANIZATION (str | None): The organization of the user.
        COUNTRY (str | None): The country of the user.
        STATE (str | None): The state of the user.

    Returns:
        dict: The JSON response from the server if the request is successful.
        None: If the request fails or the response cannot be parsed as JSON.
    """

    api_url: str = f"{self.config["serviceApiUrl"]}/api/account/user"

    user_info: dict | None = _get_user(self)

    lookups: dict | None = _get_lookups(self)
    if lookups is None:
        logging.error("Failed to get lookups.")
        return None

    countries_info: dict | None = next(
        (
            lookup for lookup in lookups if lookup["label"] == "Countries"
        ), None
    )
    country_selected: dict | None = next(
        (
            c for c in countries_info["children"] if c["label"] == country
        ), None
    )

    state_info: dict | None = next(
        (
            lookup for lookup in lookups if lookup["label"] == "States"
        ), None
    )
    state_selected: dict | None = next(
        (
            s for s in state_info["children"] if s["label"] == state
        ), None
    )

    body: dict = {
        key: value if value is not None else user_info.get(key)
        for key, value in {
            "address": address,
            "address2": address2,
            "city": city,
            "stateId": state_selected,
            "country": country_selected,
            "firstName": first_name,
            "lastName": last_name,
            "phone": phone_number,
            "phoneExt": phone_ext,
            "postalCode": postal_code,
            "organization": organization,
        }.items()
    }

    return _send_request(self, "Update user", api_url, "PUT", None, body)
