import json
import logging
import os.path
import re
import requests

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
op_file = os.path.abspath('./merged_results.json')
as_file = os.path.abspath('./app_store/data/app_store_results.json')
ps_file = os.path.abspath('./play_store/data/play_store_results.json')
am_file = os.path.abspath('./agency_map.json')

merged = {
    'results': [],
    'resultCount': 0
}

merged_dict = {}

with open(am_file, 'r') as f:
    agency_map = json.load(f)


def main():
    parse_app_store_results()
    parse_play_store_results()

    merged['results'] = merged_dict
    merged['resultCount'] = len(merged_dict)

    closed()


def parse_app_store_results():
    with open(as_file, 'r') as f:
        app_store = json.load(f)

    for obj in app_store['results']:
        app_name = obj['appName']

        item = {
            'agencyFullName': find_agency_full_name(obj),
            'appStore': {
                'appViewUrl': obj['appViewUrl'],
                'developerViewUrl': obj['developerViewUrl'],
                'averageUserRating': obj['averageUserRating'],
                'userRatingCount': obj['userRatingCount']
            }
        }

        merged_dict[app_name] = item


def parse_play_store_results():
    with open(ps_file, 'r') as f:
        play_store = json.load(f)

    for obj in play_store['results']:
        app_name = obj['appName']

        item = {
            'playStore': {
                'appViewUrl': obj['appViewUrl'],
                'developerViewUrl': obj['developerViewUrl'],
                'averageUserRating': obj['averageUserRating'],
                'userRatingCount': obj['userRatingCount']
            }
        }

        if app_name in merged_dict:
            merged_dict[app_name].update(item)
        else:
            item['agencyFullName'] = find_agency_full_name(obj)
            merged_dict[app_name] = item


def find_agency_full_name(obj):
    dev_url = obj['developerViewUrl']
    app_url = obj['appViewUrl']

    if 'itunes' in dev_url:
        dev_id = re.findall(r'id(\d+)[?]', dev_url)[0]
        app_id = re.findall(r'id(\d+)[?]', app_url)[0]
    else:
        dev_id = dev_url.split('id=')[1].replace(
            '%28', '(').replace('%29', ')')
        app_id = app_url.split('id=')[1].replace(
            '%28', '(').replace('%29', ')')

    for k, v in agency_map.iteritems():
        ids = v.keys()
        if dev_id in ids or app_id in ids:
            return k


def closed():
    with open(op_file, 'w') as f:
        f.write(json.dumps(merged))

        logging.info('Saved file %s' % op_file)


if __name__ == '__main__':
    main()
