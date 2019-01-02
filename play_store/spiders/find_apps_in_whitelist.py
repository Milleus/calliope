from lxml import html
import json
import os.path
import requests
import scrapy


class FindAppsByWhitelist(scrapy.Spider):
    name = 'find_apps_in_whitelist'
    op_file = os.path.abspath('./play_store/data/play_store_results.json')
    wl_file = os.path.abspath('./play_store/data/whitelist.json')

    play_store = {
        'results': [],
        'resultCount': 0
    }

    with open(wl_file, 'r') as f:
        whitelist = json.load(f)

    def start_requests(self):
        app_obj = self.whitelist.pop('whitelistedApps', None)
        app_urls = app_obj.values() if app_obj is not None else []
        dev_urls = self.whitelist.values()

        for u in dev_urls:
            yield scrapy.Request(url=u, callback=self.parse_apps_by_dev)

        for u in app_urls:
            yield scrapy.Request(url=u, callback=self.parse)

    def parse_apps_by_dev(self, response):
        origin = 'https://play.google.com'
        paths = response.css(
            'div.Q9MA7b a[href^="/store/apps/details"]::attr(href)').extract()

        for p in paths:
            yield scrapy.Request(url=origin + p, callback=self.parse)

    def parse(self, response):
        aur = response.css('.BHMmbe::text').extract_first()
        aur = float(aur.replace(',', '')) if aur is not None else 0

        urc = response.css('.EymY4b span:nth-child(2)::text').extract_first()
        urc = int(urc.replace(',', '')) if urc is not None else 0

        item = {
            'appName': response.css('h1[itemprop="name"] span::text').extract_first(),
            'appViewUrl': response.url,

            'developerName': response.css('.T32cc.UAO9ie:nth-child(1) a::text').extract_first(),
            'developerViewUrl': response.css('.T32cc.UAO9ie:nth-child(1) a::attr(href)').extract_first(),

            'bundleId': response.url.split('id=')[1],
            'description': response.css('meta[itemprop="description"]::attr(content)').extract_first(),
            'contentAdvisoryRating': response.css('.hAyfc:nth-child(6) span div::text').extract_first(),
            'releaseNotes': ' '.join(response.css('[jsrenderer="FzdkFd"] div[jsname="bN97Pc"] content::text').extract()),
            'size': response.css('.hAyfc:nth-child(2) span div span::text').extract_first(),

            'currentVersionReleaseDate': response.css('.hAyfc:nth-child(1) span div span::text').extract_first(),
            'minimumOsVersion': response.css('.hAyfc:nth-child(5) span div span::text').extract_first(),
            'version': response.css('.hAyfc:nth-child(4) span div span::text').extract_first(),

            'averageUserRating': aur,
            'userRatingCount': urc,
            'downloads': response.css('.hAyfc:nth-child(3) span div span::text').extract_first(),
        }

        self.play_store['results'].append(item)
        self.play_store['resultCount'] += 1

    def closed(self, reason):
        with open(self.op_file, 'w') as f:
            f.write(json.dumps(self.play_store))

        self.logger.info('Saved file %s' % self.op_file)
