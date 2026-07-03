import requests
import json
import sqlite3

conn = sqlite3.connect("db.db")
cur = conn.cursor()
GEOCODIO_API_KEY = "2603aa336723a23240635622634ff823f204623"

def main():
    address = """input("Enter an address: ")"""'48 thames blvd, 07621'
    result = lookup_address(address)
    print(result)
    # if result:
    #     for i in result:
    #         print (result[i])
    cur.execute(f"SELECT * FROM politician WHERE position_id IN (SELECT id FROM position WHERE district_id = (SELECT id FROM legislative_district WHERE name = '{result["congressional_district"]}' AND type = 'congressional'));")
    for row in cur.fetchall():
        print(f"{row[1]}, {row[3]}")
        cur.execute(f"SELECT * FROM FACTS WHERE politician_id = {row[0]}")
        for i in cur.fetchall():
            print (i[1])
        print("m"*60)

def lookup_address(address):
    url = "https://api.geocod.io/v1.7/geocode"
    params = {
        "q": address,
        "fields": "cd,stateleg,county",
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
        "county": result["address_components"].get("county"),
        "city": result["address_components"].get("city"),
        "congressional_district": None,
        "state_senate_district": None,
        "state_house_district": None,
    }

    # Congressional district
    cd = fields.get("congressional_districts", [])
    if cd:
        output["congressional_district"] =  cd[0].get("district_number")

    # State legislative districts
    stateleg = fields.get("state_legislative_districts", {})

    senate = stateleg.get("senate", [])
    if senate:
        output["state_senate_district"] = senate[0].get("district_number"),

    house = stateleg.get("house", [])
    if house:
        output["state_house_district"] = house[0].get("district_number")

    return output


if __name__ == "__main__":
    main()