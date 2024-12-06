# ezoff

Python package for interacting with the EZOffice API

## Installation

`pip install ezoff`

## Usage

Several environment variables are required for ezo to function.

| Required? | Env Variable | Description |
| --------- | ------------ | ----------- |
| EZO_BASE_URL | Yes | Should be https://{companyname}.ezofficeinventory.com/ |
| EZO_TOKEN | Yes | The access token used to authenticate requests |

## Project Structure

Project is split up into several files depending on what area of the EZOffice API is being dealt with. Purely for organizational purposes.

### Assets

Contains functions for the following:

- get all asssets
- get filtered assets
- search for an asset
- create an asset
- update an asset
- delete an asset
- check asset in
- check asset out
- get an asset's history

### Inventories

- get inventories
- get inventory details
- create inventory order
- get inventory history

### Groups

Contains functions for the following:

- get subgroups

### Locations

Contains functions for the following:

- get locations
- get location details
- get item quantities in location
- create a location
- activate a location
- deactivate a location
- update a location

### Members

Contains functions for the following:

- get members
- get a member's details
- create a member
- update a member
- deactivate a member
- activate a member
- get custom roles
- get teams

### Work Orders

Contains functions for the following:

- get work orders
- get work order details
- get work order types
- create a work order
- start a work order
- end a work order
- add work log to a work order
- add linked inventory to a work order
- get checklists

## Notes

The official EZOffice documentation is mistaken on custom fields (insofar as how to fill them out when creating an object or updating the custom field on an already existing object). It says to put underscores in place of spaces in the field name, but this is incorrect. After testing the API, it appears it wants the actual name of the field with the spaces, not underscores. At least on members.

Similarly, the documentation isn't exhaustive when it comes to listing the valid fields when creating or updating something. Frequently there are fields on the actual page that aren't mentioned in the EZOffice documentation. Throughout this program I check that keys provided are valid to prevent the API call from potentially erroring out. So there may be times where a key that would be valid if passed to the API is provided, but the function does not allow it. This is because the key wasn't documented. Just have to add to list of valid key whenever we run into one.

When wanting to clear a field out of its current value with an update function, generally the empty string ("") should be used.
