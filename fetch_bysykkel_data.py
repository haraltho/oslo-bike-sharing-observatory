#%%
import httpx
import json
import os
import datetime as dt

#%%
# Endpoints
URL_SYSTEM       = "https://gbfs.urbansharing.com/oslobysykkel.no/system_information.json"
URL_STATIONS     = "https://gbfs.urbansharing.com/oslobysykkel.no/station_information.json"
URL_AVAILABILITY = "https://gbfs.urbansharing.com/oslobysykkel.no/station_status.json"

OUTPUT_PATH = "data"


IDENTIFIER = "personal-bysykkel-project"

headers = {
    "Client-Identifier": IDENTIFIER,
}

def fetch_data(url):
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data

def save_data(data, output_path, filename):
    with open(f"{output_path}/{filename}", "w") as f:
        json.dump(data, f, indent=4)



if __name__ == "__main__":
    os.makedirs(os.path.join(OUTPUT_PATH, "stations"),     exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_PATH, "system"),       exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_PATH, "availability"), exist_ok=True)

    data_stations     = fetch_data(URL_STATIONS)
    data_system       = fetch_data(URL_SYSTEM)
    data_availability = fetch_data(URL_AVAILABILITY)

    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

    save_data(data_stations,     os.path.join(OUTPUT_PATH, "stations"),     f"station_information_{timestamp}.json")
    save_data(data_system,       os.path.join(OUTPUT_PATH, "system"),       f"system_information_{timestamp}.json")
    save_data(data_availability, os.path.join(OUTPUT_PATH, "availability"), f"station_status_{timestamp}.json")

    # Write print statment of generated files
    print(f"Generated files:")
    print(f" - {os.path.join(OUTPUT_PATH, 'stations',     f'station_information_{timestamp}.json')}")
    print(f" - {os.path.join(OUTPUT_PATH, 'system',       f'system_information_{timestamp}.json')}")
    print(f" - {os.path.join(OUTPUT_PATH, 'availability', f'station_status_{timestamp}.json')}")
