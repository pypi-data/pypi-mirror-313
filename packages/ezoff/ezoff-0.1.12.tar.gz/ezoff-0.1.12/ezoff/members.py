"""
This module contains functions for interacting with members/roles/user setup in EZOfficeInventory
"""

import os
import time
from typing import Optional

import requests

from ezoff._auth import Decorators
from ezoff._helpers import _basic_retry, _fetch_page


@Decorators.check_env_vars
def get_members(filter: Optional[dict]) -> list[dict]:
    """
    Get members from EZOfficeInventory
    Optionally filter by email, employee_identification_number, or status
    https://ezo.io/ezofficeinventory/developers/#api-retrieve-members
    """

    if filter is not None:
        if "filter" not in filter or "filter_val" not in filter:
            raise ValueError("filter must have 'filter' and 'filter_val' keys")
        if filter["filter"] not in [
            "email",
            "employee_identification_number",
            "status",
        ]:
            raise ValueError(
                "filter['filter'] must be one of 'email', 'employee_identification_number', 'status'"
            )

    url = os.environ["EZO_BASE_URL"] + "members.api"

    page = 1
    all_members = []

    while True:
        params = {"page": page, "include_custom_fields": "true"}
        if filter is not None:
            params.update(filter)

        try:
            response = _fetch_page(
                url,
                headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
                params=params,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"Error, could not get members: {e.response.status_code} - {e.response.content}"
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error, could not get members: {e}")

        data = response.json()
        if "members" not in data:
            raise Exception(f"Error, could not get members: {response.content}")

        all_members.extend(data["members"])

        if "total_pages" not in data:
            break

        if page >= data["total_pages"]:
            break

        page += 1

        # Potentially running into rate limiting issues with this endpoint
        # Sleep for a second to avoid this
        time.sleep(1)

    return all_members


@_basic_retry
@Decorators.check_env_vars
def get_member_details(member_id: int) -> dict:
    """
    Get member from EZOfficeInventory by member_id
    https://ezo.io/ezofficeinventory/developers/#api-member-details
    """

    url = os.environ["EZO_BASE_URL"] + "members/" + str(member_id) + ".api"

    try:
        response = requests.get(
            url,
            headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
            params={"include_custom_fields": "true"},
            timeout=30,
        )
    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"Error, could not get member details: {e.response.status_code} - {e.response.content}"
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error getting member details: {e}")

    return response.json()


@Decorators.check_env_vars
def create_member(member: dict) -> dict:
    """
    Create a new member
    https://ezo.io/ezofficeinventory/developers/#api-create-member
    """

    # Required fields
    if "user[email]" not in member:
        raise ValueError("member must have 'user[email]' key")
    if "user[first_name]" not in member:
        raise ValueError("member must have 'user[first_name]' key")
    if "user[last_name]" not in member:
        raise ValueError("member must have 'user[last_name]' key")
    if "user[role_id]" not in member:
        raise ValueError("member must have 'user[role_id]' key")

    # Remove any keys that are not valid
    valid_keys = [
        "user[email]",
        "user[employee_id]",
        "user[employee_identification_number]",
        "user[role_id]",
        "user[team_id]",
        "user[user_listing_id]",
        "user[first_name]",
        "user[last_name]",
        "user[address_name]",
        "user[address]",
        "user[address_line_2]",
        "user[city]",
        "user[state]",
        "user[country]",
        "user[phone_number]",
        "user[fax]",
        "user[login_enabled]",
        "user[subscribed_to_emails]",
        "user[display_picture]",
        "skip_confirmation_email",
    ]

    # Check for custom attributes
    member = {
        k: v
        for k, v in member.items()
        if k in valid_keys or k.startswith("user[custom_attributes]")
    }

    url = os.environ["EZO_BASE_URL"] + "members.api"

    try:
        response = requests.post(
            url,
            headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
            data=member,
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"Error, could not create member: {e.response.status_code} - {e.response.content}"
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error creating member: {e}")

    return response.json()


@Decorators.check_env_vars
def update_member(member_id: int, member: dict) -> dict:
    """
    Update a member
    https://ezo.io/ezofficeinventory/developers/#api-update-member
    """

    # Remove any keys that are not valid
    valid_keys = [
        "user[email]",
        "user[employee_id]",
        "user[employee_identification_number]",
        "user[role_id]",
        "user[team_id]",
        "user[user_listing_id]",
        "user[first_name]",
        "user[last_name]",
        "user[address_name]",
        "user[address]",
        "user[address_line_2]",
        "user[city]",
        "user[state]",
        "user[country]",
        "user[phone_number]",
        "user[fax]",
        "user[login_enabled]",
        "user[subscribed_to_emails]",
        "user[display_picture]",
        "skip_confirmation_email",
    ]

    # Check for custom attributes
    member = {
        k: v
        for k, v in member.items()
        if k in valid_keys or k.startswith("user[custom_attributes]")
    }

    url = os.environ["EZO_BASE_URL"] + "members/" + str(member_id) + ".api"

    try:
        response = requests.patch(
            url,
            headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
            data=member,
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"Error, could not update member: {e.response.status_code} - {e.response.content}"
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error updating member: {e}")

    return response.json()


@Decorators.check_env_vars
def deactivate_member(member_id: int) -> dict:
    """
    Deactivate a member
    https://ezo.io/ezofficeinventory/developers/#api-deactivate-user
    """

    url = os.environ["EZO_BASE_URL"] + "members/" + str(member_id) + "/deactivate.api"

    try:
        response = requests.put(
            url,
            headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"Error, could not deactivate member: {e.response.status_code} - {e.response.content}"
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error deactivating member: {e}")

    return response.json()


@Decorators.check_env_vars
def activate_member(member_id: int) -> dict:
    """
    Activate a member
    https://ezo.io/ezofficeinventory/developers/#api-activate-user
    """

    url = os.environ["EZO_BASE_URL"] + "members/" + str(member_id) + "/activate.api"

    try:
        response = requests.put(
            url,
            headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"Error, could not activate member: {e.response.status_code} - {e.response.content}"
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error activating member: {e}")

    return response.json()


@Decorators.check_env_vars
def get_custom_roles() -> list[dict]:
    """
    Get list of custom roles
    Results are technically paginated but the number of custom roles
    is usually small enough that it can be returned in one page.
    https://ezo.io/ezofficeinventory/developers/#api-retrieve-roles
    """

    url = os.environ["EZO_BASE_URL"] + "custom_roles.api"

    pages = 1
    all_custom_roles = []

    while True:
        try:
            response = _fetch_page(
                url,
                headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
                params={"page": pages},
            )
        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"Error, could not update member: {e.response.status_code} - {e.response.content}"
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error updating member: {e}")

        data = response.json()

        if "custom_roles" not in data:
            raise Exception(f"Error, could not get custom roles: {response.content}")

        all_custom_roles.extend(data["custom_roles"])

        if "total_pages" not in data:
            break

        if pages >= data["total_pages"]:
            break

        pages += 1

    return all_custom_roles


@Decorators.check_env_vars
def get_teams() -> list[dict]:
    """
    Get teams
    https://ezo.io/ezofficeinventory/developers/#api-retrieve-teams
    """

    url = os.environ["EZO_BASE_URL"] + "teams.api"

    page = 1
    all_teams = []

    while True:
        try:
            response = _fetch_page(
                url,
                headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
                params={"page": page},
            )
        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"Error, could not get teams: {e.response.status_code} - {e.response.content}"
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error getting teams: {e}")

        data = response.json()

        if "teams" not in data:
            raise Exception(f"Error, could not get teams: {response.content}")

        all_teams.extend(data["teams"])

        if "total_pages" not in data:
            break

        if page >= data["total_pages"]:
            break

        page += 1

    return all_teams
