#%%
import httpx

#%%
# Endpoints
url_system       = "https://gbfs.urbansharing.com/oslobysykkel.no/system_information.json"
url_stations     = "https://gbfs.urbansharing.com/oslobysykkel.no/station_information.json"
url_availability = "https://gbfs.urbansharing.com/oslobysykkel.no/station_status.json"

IDENTIFIER = "personal-bysykkel-project"

headers = {
    "Client-Identifier": IDENTIFIER,
}

response_stations = httpx.get(url_stations, headers=headers)
response_system = httpx.get(url_system, headers=headers)
response_availability = httpx.get(url_availability, headers=headers)

#%%
station_data = response_stations.json()
system_data = response_system.json()
availability_data = response_availability.json()

print("test")