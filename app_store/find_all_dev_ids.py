import json
import logging
import os.path
import requests
import time

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
keywords_filename = os.path.abspath('./keywords.data')
all_dev_ids_filename = os.path.abspath('./app_store/all_dev_ids.json')

app_store = {
    'results': {},
    'resultCount': 0
}


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

    if dev_id not in app_store['results']:
        app_store['results'][dev_id] = o['artistViewUrl']
        app_store['resultCount'] += 1


def closed():
    with open(all_dev_ids_filename, 'w') as f:
        f.write(json.dumps(app_store))

        logging.info('Saved file %s' % all_dev_ids_filename)


if __name__ == '__main__':
    main()
