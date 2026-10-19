#%%
import httpx
import json
import os
import datetime as dt
from azure.storage.blob import BlobServiceClient

#%%
# Bysykkel Endpoints
URL_SYSTEM       = "https://gbfs.urbansharing.com/oslobysykkel.no/system_information.json"
URL_STATIONS     = "https://gbfs.urbansharing.com/oslobysykkel.no/station_information.json"
URL_AVAILABILITY = "https://gbfs.urbansharing.com/oslobysykkel.no/station_status.json"

# Bysykkel API identifier and header
IDENTIFIER = "personal-bysykkel-project"
headers = {
    "Client-Identifier": IDENTIFIER,
}

# Blob storage configuration
USE_BLOB_STORAGE = True
CONNECT_STR = "UseDevelopmentStorage=true"
CONTAINER_NAME = "bysykkel"

# Path for when USE_BLOB_STORAGE is False
OUTPUT_PATH = "data"


def fetch_data(url):
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data

def save_data(data, output_path, filename):
    with open(f"{output_path}/{filename}", "w") as f:
        json.dump(data, f, indent=4)


def save_data_to_blob(data, container, filename):
    blob = container.get_blob_client(filename)
    blob.upload_blob(json.dumps(data))


def capture_to_blob():
    client = BlobServiceClient.from_connection_string(CONNECT_STR)
    container = client.get_container_client(CONTAINER_NAME)
    if not container.exists():
        container.create_container()

    data_stations     = fetch_data(URL_STATIONS)
    data_system       = fetch_data(URL_SYSTEM)
    data_availability = fetch_data(URL_AVAILABILITY)

    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

    save_data_to_blob(data_stations,     container, f"stations/station_information_{timestamp}.json")
    save_data_to_blob(data_system,       container, f"system/system_information_{timestamp}.json")
    save_data_to_blob(data_availability, container, f"availability/station_status_{timestamp}.json")

    # Write print statment of generated files
    print(f"Generated files in Azure Blob Storage:")
    print(f" - stations/station_information_{timestamp}.json")
    print(f" - system/system_information_{timestamp}.json")
    print(f" - availability/station_status_{timestamp}.json")


def capture_to_local():
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
     




if __name__ == "__main__":
    if USE_BLOB_STORAGE:
        capture_to_blob()
    else:
        capture_to_local()


