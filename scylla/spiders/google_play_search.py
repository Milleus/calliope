from lxml import html
import json
import os.path
import requests
import scrapy


class GooglePlaySearch(scrapy.Spider):
    name = 'google_play_search'
    filename = os.path.abspath('./data/google_play_search.json')
    google_play_search = {
        'results': [],
        'resultCount': 0
    }

    def start_requests(self):
        origin = 'https://play.google.com'
        payload = {'q': '.gov.sg', 'c': 'apps'}

        r = requests.get(origin + '/store/search', params=payload)
        w = html.fromstring(r.content)

        app_xpath = '//a[contains(@href,"store/apps/details?id=") and @class="title"]/@href'
        pnames = w.xpath(app_xpath)

        for pname in pnames:
            yield scrapy.Request(url=origin + pname, callback=self.parse)

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

        self.google_play_search['results'].append(item)
        self.google_play_search['resultCount'] += 1

    def closed(self, reason):
        with open(self.filename, 'w') as f:
            f.write(json.dumps(self.google_play_search))

        self.logger.info('Saved file %s' % self.filename)
