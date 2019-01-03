import json
import logging
import os.path
import requests
import time

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
kw_file = os.path.abspath('./keywords.data')
op_file = os.path.abspath('./app_store/data/all_dev_ids.json')

app_store = {
    'data': {},
    'totalCount': 0
}


def main():
    origin = 'https://itunes.apple.com'

    for l in open(kw_file, 'r'):
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


def parse(obj):
    dev_id = str(obj['artistId'])

    if dev_id not in app_store['data']:
        app_store['data'][dev_id] = obj['artistViewUrl']
        app_store['totalCount'] += 1


def closed():
    with open(op_file, 'w') as f:
        f.write(json.dumps(app_store))

        logging.info('Saved file %s' % op_file)


if __name__ == '__main__':
    main()
