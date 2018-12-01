# -*- coding: utf-8 -*-
import scrapy
from TenCent.items import TencentItem,DetailItem


class TcSpider(scrapy.Spider):
    name = 'tc'
    allowed_domains = ['hr.tencent.com']
    base_url = "https://hr.tencent.com/"
    start_urls = ['https://hr.tencent.com/position.php']

    def parse(self, response):
        node_list = response.xpath("//tr[@class='even']|//tr[@class='odd']")
        next_page = response.xpath('//a[@id="next"]/@href').extract_first()

        for node in node_list:
            item = TencentItem()
            item['position_name'] = node.xpath("./td[1]/a/text()").extract_first()
            item['position_link'] = node.xpath("./td[1]/a/@href").extract_first()
            item['position_type'] = node.xpath("./td[2]/text()").extract_first()
            item['people_number'] = node.xpath("./td[3]/text()").extract_first()
            item['work_location'] = node.xpath("./td[4]/text()").extract_first()
            item['publish_times'] = node.xpath("./td[5]/text()").extract_first()
            yield item
            yield scrapy.Request(url=self.base_url+item['position_link'],callback=self.parse_detail)
        yield scrapy.Request(url=self.base_url+next_page,callback=self.parse)

    def parse_detail(self,response):
        item = DetailItem()
        item['position_zhize'] = "".join(response.xpath('//ul[@class="squareli"]')[0].xpath("./li/text()").extract())
        item['position_yaoqiu'] = "".join(response.xpath('//ul[@class="squareli"]')[1].xpath("./li/text()").extract())
        yield item