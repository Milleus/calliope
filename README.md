# Scylla

Scylla retrieves a list of mobile application information from App Store and Google Play for further analysis. Information from App Store is through use of App Store search API, information from Google Play is from web crawler. Current functionality "searches" both stores based on keywords provided and stores results as in json files.

## Use Case

Scylla was created with the goal of retrieving information of all Singapore government owned mobile applications. Current search is not optimized as it may returns other mobile applications as well. Further work will be done to refine searching and crawling - perhaps to search and crawl based on a list of developer id.

## Installation Steps

1. Install python 2.7 and pip.
2. Install scrapy with `pip install scrapy`.

## Commands

- `python app_store_search.py`

  Calls App Store API with search parameters (currently hardcoded). Data is stored a json object in `/data/app_store_search.json`. This command will overwrite existing data file.

- `scrapy crawl google_play_search`

Calls Google Play search with search params (currently hardcoded), extract app urls, and crawl each app url. Data is stored as a json object in `/data/google_play_search.json`. This command will overwrite existing data file.

## Resources

- App Store Search API - https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
- Scrapy - https://scrapy.org/
