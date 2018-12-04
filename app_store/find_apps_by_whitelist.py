import json
import logging
import os.path
import requests

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
apps_data_filename = os.path.abspath('./data/app_store_results.json')
whitelist_filename = os.path.abspath('./app_store/whitelist.json')

app_store = {
    'results': [],
    'resultCount': 0
}

with open(whitelist_filename, 'r') as f:
    whitelist = json.load(f)


def main():
    origin = 'https://itunes.apple.com'
    wl_arr = whitelist.keys()
    identifiers = ','.join(wl_arr)
    payload_str = 'id=%s&country=SG&entity=software' % identifiers

    r = requests.get(origin + '/lookup', params=payload_str)

    for o in r.json()['results']:
        parse(o)

    closed()


def parse(o):
    if 'trackName' not in o:
        return

    item = {
        'appName': o['trackName'],
        'appViewUrl': o['trackViewUrl'],

        'developerName': o['artistName'],
        'developerViewUrl': o['artistViewUrl'],

        'bundleId': o['bundleId'],
        'description': o['description'],
        'contentAdvisoryRating': o['contentAdvisoryRating'],
        'releaseNotes': set_v('releaseNotes', o),
        'size': o['fileSizeBytes'],

        'currentVersionReleaseDate': o['currentVersionReleaseDate'],
        'minimumOsVersion': o['minimumOsVersion'],
        'version': o['version'],

        'averageUserRating': set_v('averageUserRating', o, False),
        'userRatingCount': set_v('userRatingCount', o, False),
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
    with open(apps_data_filename, 'w') as f:
        f.write(json.dumps(app_store))

        logging.info('Saved file %s' % apps_data_filename)


if __name__ == '__main__':
    main()
