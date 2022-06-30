from lxml import html
import copy
import json
import os.path
import requests
import scrapy


class FindAppsByWhitelist(scrapy.Spider):
    name = 'get_apps_data'
    op_file = os.path.abspath('./play_store/data/apps_data.json')
    wl_file = os.path.abspath('./play_store/data/whitelist.json')

    play_store = {
        'data': [],
        'totalCount': 0
    }

    with open(wl_file, 'r') as f:
        whitelist = json.load(f)

    def start_requests(self):
        wl_copy = copy.deepcopy(self.whitelist)
        wl_apps = wl_copy.pop('whitelistedApps', None)
        app_obj = wl_apps.values() if wl_apps is not None else []
        dev_obj = wl_copy.values()

        for d in dev_obj:
            yield scrapy.Request(url=d['url'], callback=self.parse_apps_by_dev)

        for a in app_obj:
            yield scrapy.Request(url=a['url'], callback=self.parse)

    def parse_apps_by_dev(self, response):
        origin = 'https://play.google.com'
        paths = response.css('div.TAQqTe a[href^="/store/apps/details"]::attr(href)').extract()

        for p in paths:
            yield scrapy.Request(url=origin + p, callback=self.parse)

    def parse(self, response):
        aur = response.css('div.TT9eCd::text').extract_first()
        # aur = float(aur.replace(',', '')) if aur is not None else 0

        urc = response.css('.g1rdde::text').extract_first().split(' ')[0]
        # urc = int(urc.replace(',', '')) if urc is not None else 0

        item = {
            'agencyFullName': self.find_agency_full_name(response),
            'appName': response.css('h1[itemprop="name"] span::text').extract_first(),
            'appViewUrl': response.url,

            'developerName': response.css('.Vbfug.auoIOc span::text').extract_first(),
            'developerViewUrl': response.css('.Vbfug.auoIOc a::attr(href)').extract_first(),

            'bundleId': response.url.split('id=')[1],
            'description': response.css('meta[itemprop="description"]::attr(content)').extract_first(),
            'contentAdvisoryRating': response.css('span[itemprop="contentRating"] span::text').extract_first(),
            # 'releaseNotes': ' '.join(response.css('[jsrenderer="FzdkFd"] div[jsname="bN97Pc"] content::text').extract()),
            # 'size': response.css('.hAyfc:nth-child(2) span div span::text').extract_first(),

            # 'currentVersionReleaseDate': response.css('.hAyfc:nth-child(1) span div span::text').extract_first(),
            # 'minimumOsVersion': response.css('.hAyfc:nth-child(5) span div span::text').extract_first(),
            # 'version': response.css('.hAyfc:nth-child(4) span div span::text').extract_first(),

            'averageUserRating': aur,
            'userRatingCount': urc,
            'downloads': response.css('.wVqUob div.ClM7O::text').extract_first(),
        }

        self.play_store['data'].append(item)
        self.play_store['totalCount'] += 1

    def find_agency_full_name(self, response):
        dev_url = response.css('.Vbfug.auoIOc a::attr(href)').extract_first()
        app_url = response.url

        dev_id = dev_url.split('id=')[1].replace('%28', '(').replace('%29', ')')
        app_id = app_url.split('id=')[1].replace('%28', '(').replace('%29', ')')

        agency_full_name = None

        if dev_id in self.whitelist:
            agency_full_name = self.whitelist[dev_id]['agencyFullName']

        if app_id in self.whitelist['whitelistedApps']:
            agency_full_name = self.whitelist['whitelistedApps'][app_id]['agencyFullName']

        return agency_full_name

    def closed(self, reason):
        with open(self.op_file, 'w') as f:
            f.write(json.dumps(self.play_store))

        self.logger.info('Saved file %s' % self.op_file)
