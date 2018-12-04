import json
import logging
import os.path
import requests
import time

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
keywords_filename = os.path.abspath('./keywords.data')
blacklist_filename = os.path.abspath('./app_store/blacklist.json')
unverified_filename = os.path.abspath('./app_store/unverified.json')
whitelist_filename = os.path.abspath('./app_store/whitelist.json')

app_store = {
    'results': {},
    'resultCount': 0
}

with open(blacklist_filename, 'r') as f:
    blacklist = json.load(f)

with open(whitelist_filename, 'r') as f:
    whitelist = json.load(f)


def main():
    origin = 'https://itunes.apple.com'

    for l in open(keywords_filename, 'r'):
        p = get_params(l)
        r = requests.get(origin + '/search', params=p)

        for o in r.json()['results']:
            parse(o)

        # throttle API calls, search API limited to approximately 20 calls per minute
        time.sleep(3)

    closed()


def get_params(keyword):
    return {
        'country': 'SG',
        'term': keyword,
        'media': 'software',
        # 'limit': '200'
    }


def parse(o):
    dev_id = str(o['artistId'])

    if dev_id not in whitelist and dev_id not in blacklist and dev_id not in app_store['results']:
        try:
            app_store['results'][dev_id] = o['artistViewUrl']
            app_store['resultCount'] += 1
            logging.info('Developer id not found %s' % dev_id)
        except:
            logging.error('Error in record %s' % o)


def closed():
    with open(unverified_filename, 'w') as f:
        f.write(json.dumps(app_store))

        logging.info('Saved file %s' % unverified_filename)


if __name__ == '__main__':
    main()
