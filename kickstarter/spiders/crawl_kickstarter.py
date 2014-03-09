from scrapy.spider import Spider
from scrapy.selector import Selector
import scrapy
import json
import os
import errno

import inspect # Debug

import common
from kickstarter.items import KickstarterItem

class KickstarterSpider(Spider):
    name = 'kickstarter'
    allowed_domains = ['kickstarter.com']
    delay = 30
    settings = None
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.settings = settings
        super(KickstarterSpider, self).__init__()

    def generate_search_request(self, index):
        return scrapy.http.Request(
            'https://www.kickstarter.com/discover/advanced?page={0}&category_id=35&raised=2&sort=end_date&seed='.format(index),
            headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json, text/javascript, */*; q=0.01'
            },
            callback = self.parse_search,
            meta = {'index': index}
        )

    def start_requests(self):
        return [self.generate_search_request(0)]

    def parse_search(self, response):
        common.dump_response(self.settings, response)
        body = response.body_as_unicode()
        jsonresponse = json.loads(body)
        for project in jsonresponse['projects']:
            yield scrapy.http.Request(
                project['urls']['web']['project'],
                callback = self.parse_project,
                meta = {'json': project}
            )
        yield self.generate_search_request(response.meta['index'] + 1)           

    def parse_project(self, response):
        common.dump_response(self.settings, response)
        json = response.meta['json']
        sel = Selector(response)
        item = KickstarterItem()
        item['title'] = json['name']
        item['currency'] = json['currency']
        item['goal'] = float(json['goal'])
        item['date'] = int(json['deadline'])

        # Remove html tags from description here since we're in the scrapy context and thus have relevant utilities
        item['rawtext'] = ' '.join(map(
            lambda sel: sel.extract(),
            sel.xpath('//div[@class="full-description"]//text()')
        )) + ' ' + ' '.join(map(
            lambda sel: sel.extract(),
            sel.xpath('//div[@class="short_blurb"]//text()')
        ))

        item['web'] = response.url

        return [item]

