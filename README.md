# Scylla

Scylla retrieves mobile app information from play store and app store.

## Use Case

Scylla was created to retrieve mobile app information of government agency applications.

## Installation Steps

1. Install python 2.7 and pip.
2. Install scrapy with `pip install scrapy`.

## Commands

- `python app_store_search.py`

  Calls app store API with search parameters (currently hardcoded). Data is stored a json object in `/data/app_store_search.json`. This command will overwrite existing data file.

- `scrapy crawl google_play_search`

Calls googleplay search with search params (currently hardcoded), extract app urls, and crawl each app url. Data is stored as a json object in `/data/google_play_search.json`. This command will overwrite existing data file.

## Resources

- App Store Search API - https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
- Scrapy - https://scrapy.org/
