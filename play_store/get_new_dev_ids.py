from lxml import html
import json
import logging
import os.path
import requests

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
bl_file = os.path.abspath('./play_store/data/blacklist.json')
kw_file = os.path.abspath('./keywords.data')
op_file = os.path.abspath('./play_store/data/new_dev_ids.json')
wl_file = os.path.abspath('./play_store/data/whitelist.json')

play_store = {
    'data': {},
    'totalCount': 0
}

with open(bl_file, 'r') as f:
    blacklist = json.load(f)

with open(wl_file, 'r') as f:
    whitelist = json.load(f)


def main():
    origin = 'https://play.google.com'

    for l in open(kw_file, 'r'):
        p = get_params(l)
        r = requests.get(origin + '/store/search', params=p)
        w = html.fromstring(r.content)

        dev_xpath = '//a[contains(@href,"store/apps/dev")]/@href'
        dev_paths = w.xpath(dev_xpath)

        for p in dev_paths:
            parse(origin, p)

    closed()


def get_params(keyword):
    return {
        'c': 'apps',
        'q': keyword
    }


def parse(origin, path):
    dev_id = path.split('id=')[1]

    if dev_id not in whitelist and dev_id not in blacklist and dev_id not in play_store['data']:
        try:
            play_store['data'][dev_id] = origin + path
            play_store['totalCount'] += 1
            logging.info('New developer id found %s' % dev_id)
        except:
            logging.error('Error occurred %s' % origin + path)


def closed():
    with open(op_file, 'w') as f:
        f.write(json.dumps(play_store))

        logging.info('Saved file %s' % op_file)


if __name__ == '__main__':
    main()
