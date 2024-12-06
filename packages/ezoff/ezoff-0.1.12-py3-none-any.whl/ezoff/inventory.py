"""
Covers everything related to inventory assets.
"""

import os
import time

import requests

from ezoff._auth import Decorators
from ezoff._helpers import _basic_retry, _fetch_page


@Decorators.check_env_vars
def get_all_inventories() -> list[dict]:
    """
    Gets all inventory assets. Recommended to use the filtered endpoint instead
    as this one will take a long time to run.
    https://ezo.io/ezofficeinventory/developers/#api-retrieve-inventories
    """

    url = os.environ["EZO_BASE_URL"] + "inventory.api"

    page = 1
    all_inventories = []

    while True:
        params = {"page": page}

        try:
            response = _fetch_page(
                url,
                headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
                params=params,
                data={
                    "include_custom_fields": "true",
                    "show_document_urls": "true",
                    "show_image_urls": "true",
                    "show_document_details": "true",
                },
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"Error, could not get inventory details: {e.response.status_code} - {e.response.content}"
            )
        except requests.exceptions.RequestException as e:
            raise Exception("Error getting inventories: ", e)

        data = response.json()

        if "assets" not in data:
            break

        all_inventories.extend(data["assets"])

        if "total_pages" not in data:
            break

        if page >= data["total_pages"]:
            break

        page += 1

        # Potentially running into rate limiting issues with this endpoint
        # Sleep for a second to avoid this
        time.sleep(1)

    return all_inventories


# @Decorators.check_env_vars
# def get_filtered_inventories(filter: dict):
#     """
#     Gets inventory assets that match the given filters
#     https://ezo.io/ezofficeinventory/developers/#api-volatile-asset-filters
#     """

#     url = os.environ["EZO_BASE_URL"] + "inventory/filter.api"


@_basic_retry
@Decorators.check_env_vars
def get_inventory_details(inv_asset_num: int) -> dict:
    """
    Get details for an inventory asset (sometimes referred to in API as a volatile asset)
    https://ezo.io/ezofficeinventory/developers/#api-volatile-details
    """

    url = os.environ["EZO_BASE_URL"] + f"inventory/{inv_asset_num}.api"

    try:
        response = requests.get(
            url,
            headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
            data={
                "include_custom_fields": "true",
                "show_document_urls": "true",
                "show_image_urls": "true",
                "show_document_details": "true",
            },
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"Error, could not get inventory details: {e.response.status_code} - {e.response.content}"
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error getting inventory details: {e}")

    return response.json()


@Decorators.check_env_vars
def create_inventory_order(inv_asset_num: int, order: dict) -> dict:
    """
    Creates an inventory order (i.e. Add Stock or New Sale)
    """
    url = os.environ["EZO_BASE_URL"] + f"inventory/{inv_asset_num}/order.api"

    # Check required fields
    if "line_item[quantity]" not in order:
        raise Exception("Quantity is required for an order")
    if "line_item[price]" not in order:
        raise Exception("Price is required for an order")
    if "order_type" not in order:
        raise Exception("Order type is required for an order")

    # Remove any keys that are not valid
    valid_keys = ["line_item[quantity]", "line_item[price]", "order_type"]

    order = {
        k: v
        for k, v in order.items()
        if k in valid_keys
        or k.startswith("add_stock_values[c_attr_vals]")
        or k.startswith("remove_stock_values[c_attr_vals]")
    }

    try:
        response = requests.post(
            url,
            headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
            data=order,
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error creating inventory order: {e}")

    return response.json()


# @Decorators.check_env_vars
# def transfer_inventory(inv_asset_num: int, transfer: dict) -> dict:
#     """
#     Transfers inventory asset amount from one location to another.
#     Called "transfer stock" in the documentation, I'm just calling it
#     transfer inventory for consistency.
#     https://ezo.io/ezofficeinventory/developers/#api-transfer-stock
#     """

#     url = os.environ["EZO_BASE_URL"] + f"inventory/{inv_asset_num}/transfer_stock.api"


@Decorators.check_env_vars
def get_inventory_history(inv_asset_num: int) -> list[dict]:
    """
    Gets history of an inventory asset
    https://ezo.io/ezofficeinventory/developers/#api-inventory-history
    """

    url = os.environ["EZO_BASE_URL"] + f"inventory/{inv_asset_num}/history.api"

    page = 1
    all_history = []

    while True:
        params = {"page": page}

        try:
            response = requests.get(
                url,
                headers={"Authorization": "Bearer " + os.environ["EZO_TOKEN"]},
                params=params,
                timeout=30,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"Error, could not get inventory history: {e.response.status_code} - {e.response.content}"
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error getting inventory history: {e}")

        data = response.json()

        if "history" not in data:
            break

        all_history.extend(data["history"])

        if "total_pages" not in data:
            break

        if page >= data["total_pages"]:
            break

        page += 1

        # Potentially running into rate limiting issues with this endpoint
        # Sleep for a second to avoid this
        time.sleep(1)

    return all_history


# TODO Create Inventory Asset
# TODO Update Inventory Asset
# TODO Delete Inventory Asset
# TODO Get Location Based Thresholds
