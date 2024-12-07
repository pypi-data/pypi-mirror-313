# SPDX-FileCopyrightText: 2024 Jonathan Sejdija
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import pgeocode
from .nuts_data import nuts_dict
import re
import argparse

# Initialize the pgeocode library for Germany
nomi = pgeocode.Nominatim('de')

def replace_german_umlauts(text: str) -> str:
    """
    Replace German umlauts in a string with their ASCII equivalents.
    
    Args:
        text (str): The input string containing German umlauts.
    
    Returns:
        str: The string with German umlauts replaced.
    """
    # Define a mapping of umlauts to their replacements
    umlaut_mapping = {
        'ä': 'ae',
        'ö': 'oe',
        'ü': 'ue',
        'Ä': 'Ae',
        'Ö': 'Oe',
        'Ü': 'Ue',
        'ß': 'ss'
    }
    
    # Create a regular expression pattern to match all umlauts
    pattern = re.compile('|'.join(re.escape(key) for key in umlaut_mapping.keys()))
    
    # Replace each matched umlaut with its corresponding replacement
    return pattern.sub(lambda match: umlaut_mapping[match.group(0)], text)

def get_region_by_prefix(prefix) -> dict:
    """
    Finds the region based on the first digits of a postal code (prefix).
    Returns the place name and community name corresponding to the prefix.

    Args:
        prefix (str): The first digits of the postal code (e.g., '10').

    Returns:
        dict: A dictionary with 'place_name' and 'community_name'.
              If no matching postal codes are found, returns an empty dictionary.
    """
    # Filter all postal codes that start with the given prefix
    matching_postcodes = nomi._data_frame[nomi._data_frame['postal_code'].str.startswith(prefix)]
    
    # If no matching postal codes are found, return an empty dictionary
    if matching_postcodes.empty:
        return {}

    # Sort postal codes by postal_code
    sorted_postcodes = matching_postcodes.sort_values(by='postal_code')
    
    # Extract place_name and community_name
    place_name = sorted_postcodes.iloc[0]['place_name']
    community_name = sorted_postcodes.iloc[0]['community_name']

    # Take only the first part of community_name before a comma (if present)
    if ',' in community_name:
        community_name = community_name.split(',')[0].strip()

    return {
        'place_name': place_name,
        'community_name': community_name,
    }

def get_nuts(region_dict: dict) -> str:
    """
    Finds the NUTS ID based on a dictionary containing place and community names.
    
    First, it checks if the place name or part of it exists in `nuts_dict`.
    If nothing is found, it tries to find a match for the community name.

    Args:
        region_dict (dict): A dictionary with 'place_name' and 'community_name',
                            typically returned by `get_region_by_prefix`.

    Returns:
        str: The found NUTS ID. If no match is found, returns 'Not Found'.
    """
    # Extract place_name and community_name from the input dictionary
    place_name = region_dict.get('place_name', '')
    community_name = region_dict.get('community_name', '')
    
    if "Kreisfreie Stadt" in community_name:
        # make it NAME, Kreisfreie Stadt
        community_name = community_name.replace("Kreisfreie Stadt", "").strip()
        community_name = community_name+", Kreisfreie Stadt"

    if "Landkreis" in community_name:
        # make it NAME, Landkreis
        community_name = community_name.replace("Landkreis", "")
        community_name = community_name+", Landkreis"
    
    # replace umlaute with normal letters
    place_name = replace_german_umlauts(place_name)
    community_name = replace_german_umlauts(community_name)
    print(community_name)

    # Check if place_name or part of it exists in nuts_dict
    for key, value in nuts_dict.items():
        if place_name.lower() in key.lower():
            return value

    # If no match was found, check community_name
    for key, value in nuts_dict.items():
        if community_name.lower() in key.lower():
            return value

    # If no match is found, return "Not Found"
    return "Not Found"

def plz2nuts_cli():
    """
    Command-line interface to convert German postal codes to NUTS IDs.
    """
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Convert German postal code to NUTS ID.')
    parser.add_argument('postal_code', type=str, help='Postal code or prefix to lookup NUTS ID')

    # Parse the arguments
    args = parser.parse_args()

    # Get the postal code from the arguments
    postal_code = args.postal_code

    # Get the region dictionary using the postal code
    region = get_region_by_prefix(postal_code)

    if not region:
        print("No region found for the given postal code.")
        return

    # Get the NUTS ID using the region dictionary
    nuts_id = get_nuts(region)

    if nuts_id == "Not Found":
        print("No NUTS ID found for the given postal code.")
    else:
        print(nuts_id)

if __name__ == "__main__":
    plz2nuts_cli()
