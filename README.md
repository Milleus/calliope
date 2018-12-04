# Scylla

Scylla retrieves a list of mobile application information from App Store and Google Play for further analysis. Information from App Store is through use of App Store search API, information from Google Play is from web crawler. Current functionality "searches" both stores based on keywords provided and stores results as in json files.

## Use Case

Scylla was created with the goal of retrieving information of all Singapore government owned mobile applications - without mobile application owners filling in any information, everything should be automagical. So the question is how do we capture new or existing mobile applications without the agency informing us? At the same time, how do we get an accurate list of all Singapore government owned mobile applications? To do this, we need to adopt a strategy.

## Strategy

This may be a simplistic strategy but it will serve our purpose - no need for real time information, developer ids do not change often, new Singapore government owned mobile applications released on stores is not common.

First, we adopt a brute force search on the app store and play store based on a list of keywords such as `sg.gov`, `gov.sg`, `singapore government`, `<insert ministry name>`, `<insert stat board name>`, and so on. What we want here is the developer id of the applications. We combine the results together and filter out duplicates. Next, we go through the list to "verify" the developer ids that we know belong to the Singapore government and put them on a white list. At the same time, we put the ones that do not belong to the Singapore government on a black list.

With a white list of developer ids, we can now find all the mobile applications belonging to it, essentially finding all Singapore government owned mobile applications. And because we have both white and black list, every X duration (weekly, fornightly or monthly), we can run an automated job to search both app store and play store again. This automated job will also check if there are new developer ids - ids that do not belong in the white or black list - and flag them out for verification.

## Installation Steps

1. Install python 2.7 and pip.
2. Install scrapy with `pip install scrapy`.

## Commands

- `python app_store/find_all_dev_ids.py`

  Calls App Store API with all keywords in keywords.data and returns a list of developer ids. Results are stored in app_store/all_dev_ids.json. This can be modified to return other information app related information.

- `python app_store/find_new_dev_ids.py`

  Calls App Store API with all keywords in keywords.data and returns a list of new developer ids (not in whitelist or blacklist). Results are stored in app_store/unverified.json.

- `python app_store/find_apps_by_whitelist.py`

  Calls App Store API with developer/app ids in whitelist and returns a list of mobile application data. Results are stored in data/app_store_results.json.

- `scrapy crawl find_apps_by_keyword`

  Calls Google Play search with keyword (currently hardcoded), extract app urls, crawl each app url, and return a list of mobile application data. Results are stored in data/google_play_results.json.

## Resources

- App Store Search API - https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
- Scrapy - https://scrapy.org/
