"""
Covers everything related to fixed assets in EZOffice
"""

import os
import time

import requests

from ezoff._auth import Decorators
from ezoff._helpers import _basic_retry, _fetch_page


@_basic_retry
@Decorators.check_env_vars
def get_asset_details(asset_id: int):
    """
    Gets asset details
    https://ezo.io/ezofficeinventory/developers/#api-asset-details
    """

    url = os.environ["EZO_BASE_URL"] + "assets/" + str(asset_id) + ".api"

    try:
        response = requests.get(
            url,
            headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
            data={
                "include_custom_fields": "true",
                "show_document_urls": "true",
                "show_image_urls": "true",
                "show_services_details": "true",
            },
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"Error, could not get asset details: {e.response.status_code} - {e.response.content}"
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error, could not get asset details: {e}")

    return response.json()


@Decorators.check_env_vars
def get_all_assets() -> list[dict]:
    """
    Get assets
    Recommended to use endpoint that takes a filter instead.
    This endpoint can be slow as it returns all assets in the system. Potentially
    several hundred pages of assets.
    https://ezo.io/ezofficeinventory/developers/#api-retrive-assets
    """

    url = os.environ["EZO_BASE_URL"] + "assets.api"

    page = 1
    all_assets = []

    while True:
        params = {
            "page": page,
            "include_custom_fields": "true",
            "show_document_urls": "true",
            "show_image_urls": "true",
        }

        try:
            response = _fetch_page(
                url,
                headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
                params=params,
            )
        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"Error, could not get assets: {e.response.status_code} - {e.response.content}"
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error, could not get assets: {e}")

        data = response.json()

        if "assets" not in data:
            raise Exception(f"Error, could not get assets: {response.content}")

        all_assets.extend(data["assets"])

        if "total_pages" not in data:
            break

        if page >= data["total_pages"]:
            break

        page += 1

        # Potentially running into rate limiting issues with this endpoint
        # Sleep for a second to avoid this
        time.sleep(1)

    return all_assets


@Decorators.check_env_vars
def get_filtered_assets(filter: dict) -> list[dict]:
    """
    Get assets via filtering. Recommended to use this endpoint rather than
    returning all assets.
    """
    if "status" not in filter:
        raise ValueError("filter must have 'status' key")

    url = os.environ["EZO_BASE_URL"] + "assets/filter.api"

    page = 1
    all_assets = []

    while True:
        params = {
            "page": page,
            "include_custom_fields": "true",
            "show_document_urls": "true",
            "show_image_urls": "true",
            "show_services_details": "true",
        }
        params.update(filter)

        try:
            response = _fetch_page(
                url,
                headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
                params=params,
            )
        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"Error, could not get assets: {e.response.status_code} - {e.response.content}"
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error, could not get assets: {e}")

        data = response.json()

        if "assets" not in data:
            raise Exception(f"Error, could not get assets: {response.content}")

        all_assets.extend(data["assets"])

        if "total_pages" not in data:
            break

        if page >= data["total_pages"]:
            break

        page += 1

        # Potentially running into rate limiting issues with this endpoint
        # Sleep for a second to avoid this
        time.sleep(1)

    return all_assets


@Decorators.check_env_vars
def search_for_asset(search_term: str) -> list[dict]:
    """
    Search for an asset.
    The equivalent of the search bar in the EZOfficeInventory UI.
    May not return all assets that match the search term. Better to use
    get_filtered_assets if you want to return all assets that match a filter.
    https://ezo.io/ezofficeinventory/developers/#api-search-name
    """

    url = os.environ["EZO_BASE_URL"] + "search.api"

    page = 1
    all_assets = []

    while True:
        data = {
            "page": page,
            "search": search_term,
            "facet": "FixedAsset",
            "include_custom_fields": "true",
            "show_document_urls": "true",
            "show_image_urls": "true",
            "show_document_details": "true",
            "show_services_details": "true",
        }

        try:
            response = _fetch_page(
                url,
                headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
                data=data,
            )
        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"Error, could not get search results: {e.response.status_code} - {e.response.content}"
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error, could not get search results: {e}")

        data = response.json()

        if "assets" not in data:
            raise Exception(f"Error, could not get search results: {response.content}")

        all_assets.extend(data["assets"])

        if "total_pages" not in data:
            break

        if page >= data["total_pages"]:
            break

        page += 1

    return all_assets


@Decorators.check_env_vars
def create_asset(asset: dict) -> dict:
    """
    Create an asset
    https://ezo.io/ezofficeinventory/developers/#api-create-asset
    """

    # Required fields
    if "fixed_asset[name]" not in asset:
        raise ValueError("asset must have 'fixed_asset[name]' key")
    if "fixed_asset[group_id]" not in asset:
        raise ValueError("asset must have 'fixed_asset[group_id]' key")
    if "fixed_asset[purchased_on]" not in asset:
        raise ValueError("asset must have 'fixed_asset[purchased_on]' key")
        # Also check that the date is in the correct format mm/dd/yyyy
        try:
            datetime.strptime(asset["fixed_asset[purchased_on]"], "%m/%d/%Y")
        except ValueError:
            raise ValueError(
                "asset['fixed_asset[purchased_on]'] must be in the format mm/dd/yyyy"
            )

    # Remove any keys that are not valid
    valid_keys = [
        "fixed_asset[name]",
        "fixed_asset[description]",
        "fixed_asset[product_model_number]",
        "fixed_asset[manufacturer]",
        "fixed_asset[group_id]",
        "fixed_asset[sub_group_id]",
        "fixed_asset[purchased_on]",
        "fixed_asset[price]",
        "fixed_asset[location_id]",
        "fixed_asset[image_url]",
        "fixed_asset[document_urls][]",
        "fixed_asset[identifier]",
    ]

    asset = {
        k: v for k, v in asset.items() if k in valid_keys or k.startswith("cust_attr")
    }

    url = os.environ["EZO_BASE_URL"] + "assets.api"

    try:
        response = requests.post(
            url,
            headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
            data=asset,
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"Error, could not create asset: {e.response.status_code} - {e.response.content}"
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error, could not create asset: {e}")

    return response.json()


@Decorators.check_env_vars
def update_asset(asset_id: int, asset: dict) -> dict:
    """
    Update an asset's details
    https://ezo.io/ezofficeinventory/developers/#api-update-asset
    """

    # Remove any keys that are not valid
    valid_keys = [
        "fixed_asset[name]",
        "fixed_asset[description]",
        "fixed_asset[product_model_number]",
        "fixed_asset[manufacturer]",
        "fixed_asset[group_id]",
        "fixed_asset[sub_group_id]",
        "fixed_asset[identifier]",
        "fixed_asset[purchased_on]",
        "fixed_asset[price]",
        "fixed_asset[location_id]",
        "fixed_asset[image_url]",
        "fixed_asset[document_urls][]",
    ]

    asset = {
        k: v for k, v in asset.items() if k in valid_keys or k.startswith("cust_attr")
    }

    url = os.environ["EZO_BASE_URL"] + "assets/" + str(asset_id) + ".api"

    try:
        response = requests.put(
            url,
            headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
            data=asset,
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"Error, could not update asset: {e.response.status_code} - {e.response.content}"
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error, could not update asset: {str(e)}")

    return response.json()


@_basic_retry
@Decorators.check_env_vars
def delete_asset(asset_id: int) -> dict:
    """
    Delete an asset
    https://ezo.io/ezofficeinventory/developers/#api-delete-asset
    """

    url = os.environ["EZO_BASE_URL"] + "assets/" + str(asset_id) + ".api"

    try:
        response = requests.delete(
            url,
            headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"Error, could not delete asset: {e.response.status_code} - {e.response.content}"
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error, could not delete asset: {e}")

    return response.json()


@_basic_retry
@Decorators.check_env_vars
def checkin_asset(asset_id: int, checkin: dict) -> dict:
    """
    Check in an asset to a location
    https://ezo.io/ezofficeinventory/developers/#api-checkin-asset
    """

    # Required fields
    if "checkin_values[location_id]" not in checkin:
        raise ValueError("checkin must have 'checkin[location_id]' key")

    # Remove any keys that are not valid
    valid_keys = [
        "checkin_values[location_id]",
        "checkin_values[comments]",
    ]

    checkin = {
        k: v
        for k, v in checkin.items()
        if k in valid_keys or k.startswith("checkin_values[c_attr_vals]")
    }

    url = os.environ["EZO_BASE_URL"] + "assets/" + str(asset_id) + "/checkin.api"

    try:
        response = requests.put(
            url,
            headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
            data=checkin,
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"Error, could not check asset in: {e.response.status_code} - {e.response.content}"
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error, could not check asset in: {e}")

    return response.json()


@_basic_retry
@Decorators.check_env_vars
def checkout_asset(asset_id: int, user_id: int, checkout: dict) -> dict:
    """
    Check out an asset to a member
    https://ezo.io/ezofficeinventory/developers/#api-checkout-asset

    Note: If user is inactive, checkout will return a 200 status code but the
    asset will not be checked out. Response will contain a message.
    """

    # Remove any keys that are not valid
    valid_keys = [
        "checkout_values[location_id]",
        "checkout_values[comments]",
        "till",
        "till_time",
        "checkout_values[override_conflicting_reservations]",
        "checkout_values[override_my_conflicting_reservations]",
    ]

    checkout = {
        k: v
        for k, v in checkout.items()
        if k in valid_keys or k.startswith("checkout_values[c_attr_vals]")
    }

    url = os.environ["EZO_BASE_URL"] + "assets/" + str(asset_id) + "/checkout.api"

    try:
        response = requests.put(
            url,
            headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
            params={"user_id": user_id},
            data=checkout,
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"Error, could not check asset out: {e.response.status_code} - {e.response.content}"
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error, could not check asset out: {e}")

    return response.json()


@_basic_retry
@Decorators.check_env_vars
def retire_asset(asset_id: int, retire: dict) -> dict:
    """
    Retires an asset. Asset needs to be in an available state to retire.
    https://ezo.io/ezofficeinventory/developers/#api-retire-asset

    :param asset_id: The asset ID to retire
    :param retire: A dictionary containing the retirement details. Must contain the keys fixed_asset[retire_reason_id] and fixed_asset[retired_on]
    """

    # Required fields
    if "fixed_asset[retire_reason_id]" not in retire:
        raise ValueError("retire must have 'fixed_asset[retire_reason_id]' key")
    if "fixed_asset[retired_on]" not in retire:
        raise ValueError("retire must have 'fixed_asset[retired_on]' key")
        # Also check that the date is in the correct format mm/dd/yyyy
        try:
            datetime.strptime(retire["fixed_asset[retired_on]"], "%m/%d/%Y")
        except ValueError:
            raise ValueError(
                "retire['fixed_asset[retired_on]'] must be in the format mm/dd/yyyy"
            )

    # Remove any keys that are not valid
    valid_keys = [
        "fixed_asset[retire_reason_id]",
        "fixed_asset[retired_on]",
        "fixed_asset[salvage_value]",
    ]

    retire = {k: v for k, v in retire.items() if k in valid_keys}

    url = os.environ["EZO_BASE_URL"] + "assets/" + str(asset_id) + "/retire.api"

    try:
        response = requests.put(
            url,
            headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
            data=retire,
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"Error, could not retire asset: {e.response.status_code} - {e.response.content}"
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error, could not retire asset: {e}")

    return response.json()


@_basic_retry
@Decorators.check_env_vars
def reactivate_asset(asset_id: int, reactivate: dict) -> dict:
    """
    Reactivates a retired asset.
    https://ezo.io/ezofficeinventory/developers/#api-activate-asset

    :param asset_id: The asset ID to reactivate
    :param reactivate: A dictionary containing the reactivation details. Currently that's only the key fixed_asset[location_id]. Whether it's required or not varies depending on company settings.
    """

    url = os.environ["EZO_BASE_URL"] + "assets/" + str(asset_id) + "/activate.api"

    # Remove any keys that are not valid
    valid_keys = ["fixed_asset[location_id]"]

    reactivate = {k: v for k, v in reactivate.items() if k in valid_keys}

    try:
        response = requests.put(
            url,
            headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
            data=reactivate,
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"Error, could not reactivate asset: {e.response.status_code} - {e.response.content}"
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error, could not reactivate asset: {e}")

    return response.json()


@Decorators.check_env_vars
def get_asset_history(asset_id: int) -> list[dict]:
    """
    Get asset history
    https://ezo.io/ezofficeinventory/developers/#api-checkin-out-history
    """

    url = (
        os.environ["EZO_BASE_URL"] + "assets/" + str(asset_id) + "/history_paginate.api"
    )

    page = 1
    all_history = []

    while True:
        try:
            response = _fetch_page(
                url,
                headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
                params={"page": page},
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"Error, could not get asset history: {e.response.status_code} - {e.response.content}"
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error getting asset history: {e}")

        data = response.json()

        if "history" not in data:
            raise Exception(f"Error, could not get asset history: {response.content}")

        all_history.extend(data["history"])

        if "total_pages" not in data:
            break

        if page >= data["total_pages"]:
            break

        page += 1

    return all_history


@_basic_retry
@Decorators.check_env_vars
def get_items_for_token_input(q: str) -> list[dict]:
    """
    This isn't an official endpoint in the EZOfficeInventory API. It's used to populate
    the token input dropdowns in the EZOfficeInventory UI. However, still works if called
    and is needed if wanting to use the get_work_orders item filter. Which doesn't yet
    support the asset ID as a filter. But does support the ID that comes from this endpoint.
    Found this via the network tab in the browser. Not sure what the official name is
    so I'm just going off of what the URL is.

    Note: If you use "#{Asset Sequence Num}" as the q search parameter, it should
    only return one result. If you use a more general search term. like searching
    for the name, you may get multiple.
    """

    url = os.environ["EZO_BASE_URL"] + "assets/items_for_token_input.json"

    try:
        response = requests.get(
            url,
            headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
            params={"include_id": "true", "q": q},
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"Error, could not get item token: {e.response.status_code} - {e.response.content}"
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error getting item token: {e}")

    return response.json()
