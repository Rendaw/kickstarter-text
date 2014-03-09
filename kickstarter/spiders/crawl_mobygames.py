from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.utils.url import urljoin_rfc
import scrapy
import json
import os
import errno

import common
from kickstarter.items import MobyItem

class MobySpider(Spider):
    name = 'mobygames'
    allowed_domains = ['mobygames.com']
    delay = 30
    start_urls = ['http://www.mobygames.com/browse/games/offset,0/so,0a/list-games/']

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.settings = settings
        super(MobySpider, self).__init__()

    def parse(self, response):
        common.dump_response(self.settings, response)
        sel = Selector(response)

        for game_title in sel.xpath('//table[@id="mof_object_list"]//a[contains(@href, "/game/")]/text()'):
            item = MobyItem()
            item['value'] = game_title.extract()
            yield item

        for pagination_links in sel.xpath('//div[@class="mobFooter"]'):
            for link in pagination_links.xpath('.//a/@href'):
                yield scrapy.http.Request(urljoin_rfc(response.url, link.extract()), callback = self.parse)
                pass
            break

