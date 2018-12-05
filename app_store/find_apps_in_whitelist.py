import json
import logging
import os.path
import requests

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
op_file = os.path.abspath('./app_store/data/app_store_results.json')
wl_file = os.path.abspath('./app_store/data/whitelist.json')

app_store = {
    'results': [],
    'resultCount': 0
}

with open(wl_file, 'r') as f:
    whitelist = json.load(f)


def main():
    origin = 'https://itunes.apple.com'

    app_obj = whitelist.pop('whitelistedApps', None)
    app_ids = app_obj.keys() if app_obj is not None else []
    dev_ids = whitelist.keys()

    ids = ','.join(dev_ids + app_ids)
    p = 'id=%s&country=SG&entity=software' % ids

    r = requests.get(origin + '/lookup', params=p)

    for o in r.json()['results']:
        parse(o)

    closed()


def parse(obj):
    if 'trackName' not in obj:
        return

    item = {
        'appName': obj['trackName'],
        'appViewUrl': obj['trackViewUrl'],

        'developerName': obj['artistName'],
        'developerViewUrl': obj['artistViewUrl'],

        'bundleId': obj['bundleId'],
        'description': obj['description'],
        'contentAdvisoryRating': obj['contentAdvisoryRating'],
        'releaseNotes': set_v('releaseNotes', obj),
        'size': obj['fileSizeBytes'],

        'currentVersionReleaseDate': obj['currentVersionReleaseDate'],
        'minimumOsVersion': obj['minimumOsVersion'],
        'version': obj['version'],

        'averageUserRating': set_v('averageUserRating', obj, False),
        'userRatingCount': set_v('userRatingCount', obj, False),
        # 'downloads':
    }

    app_store['results'].append(item)
    app_store['resultCount'] += 1


def set_v(key, row, string_type=True):
    value = None if string_type == True else 0
    if key in row:
        value = row[key]

    return value


def closed():
    with open(op_file, 'w') as f:
        f.write(json.dumps(app_store))

        logging.info('Saved file %s' % op_file)


if __name__ == '__main__':
    main()
