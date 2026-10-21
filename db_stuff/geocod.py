import requests
import json

GEOCODIO_API_KEY = "2603aa336723a23240635622634ff823f204623"

def lookup_address(address):
    url = "https://api.geocod.io/v1.7/geocode"
    params = {
        "q": address,
        "fields": "cd,stateleg",
        "api_key": GEOCODIO_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if not data.get("results"):
        print("No results found for that address.")
        return None

    result = data["results"][0]
    fields = result.get("fields", {})

    output = {
        "formatted_address": result.get("formatted_address"),
        "state": result["address_components"].get("state"),
        "county": result["address_components"].get("county").removesuffix(' County'),
        "city": result["address_components"].get("city"),
        "congressional_district": None,
        "state_senate_district": None,
        "state_house_district": None,
        "school_district_elementary": None,
        "school_district_secondary": None,
        "school_district_unified": None,
    }

    # Congressional district
    cd = fields.get("congressional_districts", [])
    if cd:
        output["congressional_district"] = cd[0].get("district_number")

    # State legislative districts
    stateleg = fields.get("state_legislative_districts", {})

    senate = stateleg.get("senate", [])
    if senate:
        output["state_senate_district"] = senate[0].get("district_number")

    house = stateleg.get("house", [])
    if house:
        output["state_house_district"] = house[0].get("district_number")

    # School districts
    return output
if __name__ == "__main__":
    address = '48 thames bllvd, bergenfield, nj 07621'
    result = lookup_address(address)
    if result:
        for key, value in result.items():
            print(f"{key}: {value}")