# Scylla

Scylla retrieves a list of mobile application information from App Store and Play Store for further analysis. Information from App Store is through use of their search API, information from Play Store is crawling their website.

## Use Case

Scylla was created with the goal of retrieving information of all Singapore government owned mobile applications, without mobile application owners filling in any information - everything should be automagical. We want to capture a specific list of new and existing mobile applications.

## Strategy

We do a brute force search based on 100+ keywords to both stores (see keywords.data) to retrieve a list of developer ids. We combine query results and filter out duplicates. Then, we go through the list to "verify" the developer ids that we know belong to the Singapore government and put them on a whitelist, and the rest to a blacklist.

Based on the whitelist, we can now find all the mobile applications that belong to the Singapore government. We can run an automated job every X duration (weekly, fortnightly or monthly) to brute force search both stores again and flag out new developer ids found, and repeat the same process of putting them in the correct list.

## Installation Steps

1. Install python and pip.
2. Install scrapy with `pip install scrapy`.

## Commands

### App Store

- `python app_store/get_new_dev_ids.py`

  Calls App Store API with all keywords in keywords.data and returns a list of new developer ids (not in whitelist or blacklist). Results are stored in app_store/data/unverified.json.

- `python app_store/get_apps_data.py`

  Calls App Store API with developer/app ids in whitelist and returns a collection of mobile application data. Results are stored in app_store/data/apps_data.json.

### Play Store

- `python app_store/get_new_dev_ids.py`

  Calls Play Store search with all keywords in keywords.data and returns a list of new developer ids (not in whitelist or blacklist). Results are stored in play_store/data/unverified.json.

- `scrapy crawl get_apps_data`

  Crawl Play Store developer/app pages with developer/app ids in whitelist and returns a collection of mobile application data. Results are stored in play_store/data/apps_data.json.

### Merging Data

- `python merge.py`

  Combine apps_data.json from app store and play store, and return a merged collection of mobile application data. Results are stored in merged_apps_data.json.

## Resources

- App Store Search API - https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
- Scrapy - https://scrapy.org/
