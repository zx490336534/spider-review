# -*- coding: utf-8 -*-
import scrapy
from TenCent.items import TencentItem,DetailItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CrawlTencentSpider(CrawlSpider):
    name = 'crawl_tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    rules = (
        Rule(LinkExtractor(allow=r'start=\d+'), callback='parse_tencent', follow=True),
        Rule(LinkExtractor(allow=r'position_detail\.php\?id=\d+'),callback='parse_detail',follow=False)
    )

    def parse_tencent(self, response):
        node_list = response.xpath("//tr[@class='even']|//tr[@class='odd']")
        for node in node_list:
            item = TencentItem()
            item['position_name'] = node.xpath("./td[1]/a/text()").extract_first()
            item['position_link'] = node.xpath("./td[1]/a/@href").extract_first()
            item['position_type'] = node.xpath("./td[2]/text()").extract_first()
            item['people_number'] = node.xpath("./td[3]/text()").extract_first()
            item['work_location'] = node.xpath("./td[4]/text()").extract_first()
            item['publish_times'] = node.xpath("./td[5]/text()").extract_first()
            yield item
    def parse_detail(self,response):
        item = DetailItem()
        item['position_zhize'] = "".join(response.xpath('//ul[@class="squareli"]')[0].xpath("./li/text()").extract())
        item['position_yaoqiu'] = "".join(response.xpath('//ul[@class="squareli"]')[1].xpath("./li/text()").extract())
        yield item



