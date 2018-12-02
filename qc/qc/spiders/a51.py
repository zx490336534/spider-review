# -*- coding: utf-8 -*-
import scrapy
from qc.items import QcItem


class A51Spider(scrapy.Spider):
    name = 'a51'
    allowed_domains = ['51job.com']
    offset = 1
    base_url = 'https://search.51job.com/list/080200,000000,0000,00,9,99,python,2,'
    start_urls = [base_url + '1.html']

    def parse(self, response):
        node_list = response.xpath('//div[@class="el"]')
        for node in node_list:
            item = QcItem()
            item['work_name'] = node.xpath('./p/span/a/@title').extract_first()
            item['company'] = node.xpath('./span/a/@title').extract_first()
            item['work_position'] = node.xpath('./span[@class="t3"]/text()').extract_first()
            item['salary'] = node.xpath('./span[@class="t4"]/text()').extract_first()
            item['publishtime'] = node.xpath('./span[@class="t5"]/text()').extract_first()
            detail_href = node.xpath('./p/span/a/@href').extract_first()
            if not detail_href:
                continue
            yield scrapy.Request(detail_href, callback=self.detail, meta={"item": item})
        if not node_list:
            return
        self.offset += 1
        url = self.base_url + str(self.offset) + '.html'
        yield scrapy.Request(url, callback=self.parse)

    def detail(self, response):
        item = response.meta['item']
        content1 = response.xpath('//div[@class="bmsg job_msg inbox"]/*/*/text()').extract()
        content2 = response.xpath('//div[@class="bmsg job_msg inbox"]/*/text()').extract()
        if len(content1) > len(content2):
            item['content'] = "".join(content1)
        else:
            item['content'] = "".join(content2)
        item['content'] = item['content'].strip()

        item['contace'] = "".join(response.xpath('//div[@class="bmsg inbox"]/p/text()').extract()).strip()
        yield item
