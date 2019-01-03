import json
import logging
import os.path
import requests
import time

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
bl_file = os.path.abspath('./app_store/data/blacklist.json')
kw_file = os.path.abspath('./keywords.data')
op_file = os.path.abspath('./app_store/data/new_dev_ids.json')
wl_file = os.path.abspath('./app_store/data/whitelist.json')

app_store = {
    'data': {},
    'totalCount': 0
}

with open(bl_file, 'r') as f:
    blacklist = json.load(f)

with open(wl_file, 'r') as f:
    whitelist = json.load(f)


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

    if dev_id not in whitelist and dev_id not in blacklist and dev_id not in app_store['data']:
        try:
            app_store['data'][dev_id] = obj['artistViewUrl']
            app_store['totalCount'] += 1
            logging.info('New developer id found %s' % dev_id)
        except:
            logging.error('Error occurred %s' % obj)


def closed():
    with open(op_file, 'w') as f:
        f.write(json.dumps(app_store))

        logging.info('Saved file %s' % op_file)


if __name__ == '__main__':
    main()
