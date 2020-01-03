# Calliope

Calliope crawls and retrieves Singapore Government mobile applications data from both App Store and Play Store. Written in Python, this is a quick prototype on data consolidation.

## Use Case

Every X period, agencies/ministries have to report their app numbers for assessment. This crawler automates that process (at least for information that is publicly available).

Hopefully, with a smoother process to get high level timely information on all apps, certain change could be triggered.

1. Allow higher management to determine which apps should be improved, which apps should be removed.
2. Allow agencies/ministries to compare each other's apps, with hopes of triggering further actions such as knowledge sharing or consolidation of apps which provide similar services.

Ultimately, I really do hope that this could trigger some kind of change that will improve the digital service offerings that the government provides to its citizens.

## Strategy

Keep in mind that this is a prototype, this strategy is not ideal.

1. Brute force search based on keywords to retrieve a list of developer ids. (keywords file)
2. Manually "verify" the list of developer ids to determine which belongs to / does not belong to the Singapore government (thus the whitelist and blacklist file).
3. Crawl for information of apps that belong to verified developer ids.

## Installation Steps

1. Install python and pip.
2. Install scrapy with `pip install scrapy`.

## Commands

### App Store

- `python app_store/get_new_dev_ids.py`

  Calls App Store API with all keywords in keywords.data and returns a list of new developer ids (not in whitelist or blacklist). Results are stored in app_store/data/new_dev_ids.json.

- `python app_store/get_apps_data.py`

  Calls App Store API with developer/app ids in whitelist and returns a collection of mobile application data. Results are stored in app_store/data/apps_data.json.

### Play Store

- `python app_store/get_new_dev_ids.py`

  Calls Play Store search with all keywords in keywords.data and returns a list of new developer ids (not in whitelist or blacklist). Results are stored in play_store/data/new_dev_ids.json.

- `scrapy crawl get_apps_data`

  Crawl Play Store developer/app pages with developer/app ids in whitelist and returns a collection of mobile application data. Results are stored in play_store/data/apps_data.json.

### Merging Data

- `python merge_apps_data.py`

  Combine apps_data.json from app store and play store, and return a merged collection of mobile application data. Mobile applications are merged based on app name. Results are stored in merged_apps_data.json.

## Resources

- App Store Search API - https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
- Scrapy - https://scrapy.org/
