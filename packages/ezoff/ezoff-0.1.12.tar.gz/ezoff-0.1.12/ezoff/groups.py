"""
Covers everything related to groups and subgroups in EZOfficeInventory
"""

import os
from typing import Optional

import requests

from ezoff._auth import Decorators
from ezoff._helpers import _basic_retry, _fetch_page


@Decorators.check_env_vars
def get_subgroups(group_id: Optional[int]) -> list[dict]:
    """
    Get subgroups
    Optionally takes a group_id to get subgroups of a specific group
    """

    url = os.environ["EZO_BASE_URL"] + "groups/get_sub_groups.api"

    params = {}

    if group_id:
        params["group_id"] = group_id

    page = 1

    all_subgroups = []

    while True:
        try:
            response = _fetch_page(
                url,
                headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
                params=params,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"Error, could not get subgroups: {e.response.status_code} - {e.response.content}"
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error, could not get subgroups: {e}")

        data = response.json()

        if "sub_groups" not in data:
            raise Exception(f"Error, could not get subgroups: {response.content}")

        all_subgroups.extend(data["sub_groups"])

        if "total_pages" not in data:
            break

        if page >= data["total_pages"]:
            break

        page += 1

    return all_subgroups
