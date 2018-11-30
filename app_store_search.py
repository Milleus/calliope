import json
import logging
import os.path
import requests

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
filename = os.path.abspath('./data/app_store_search.json')
app_store_search = {
    'results': [],
    'resultCount': 0
}


def main():
    origin = 'https://itunes.apple.com'
    payload = {
        'country': 'SG',
        'term': 'singapore government',
        'media': 'software',
        'limit': '50'
    }

    r = requests.get(origin + '/search', params=payload)
    app_store_search['resultCount'] = r.json()['resultCount']

    for o in r.json()['results']:
        parse(o)

    closed()


def parse(o):
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

    app_store_search['results'].append(item)


def set_v(key, row, string_type=True):
    value = None if string_type == True else 0
    if key in row:
        value = row[key]

    return value


def closed():
    with open(filename, 'w') as f:
        f.write(json.dumps(app_store_search))

        logging.info('Saved file %s' % filename)


if __name__ == '__main__':
    main()
