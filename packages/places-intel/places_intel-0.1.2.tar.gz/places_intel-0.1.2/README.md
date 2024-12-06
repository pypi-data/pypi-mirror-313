# Place Intel

`places-intel` is a Python library for fetching and processing place data with polygons using Outscraper and Overpass APIs.


## Installation

```bash
pip install places-intel


## Usage

## Fetching Information for Multiple Places and ccreating a kml file

from places_intel import multiple_place_intel, create_kml

api_key = "your-api-key"
places, polygons = multiple_place_intel(api_key, "museums", "New York", result_amount=5, radius=10)
print(places)
create_kml(polygons, "output.kml")

## Fetching Information for a Single Place

from places-intel import single_place_intel, create_kml

api_key = "your-api-key"
place, polygons = single_place_intel(api_key, "Empire State Building", radius=10)
print(place)
create_kml(polygons, "output.kml")

