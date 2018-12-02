# -*- coding: utf-8 -*-
import re

import scrapy
from qc.items import QcItem
from urllib import parse


class A51Spider(scrapy.Spider):
    name = 'a51'
    allowed_domains = ['search.51job.com', 'jobs.51job.com']
    offset = 1
    keyword = ' '
    keyword_urlcode = parse.quote(parse.quote(keyword))
    base_url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,%s,2,' % keyword_urlcode
    start_urls = [base_url + '1.html']

    def parse(self, response):
        node_list = response.xpath('//div[@class="el"]')
        page_info = response.xpath('//*[@id="resultList"]/div/div/div/div/span/text()').extract_first()
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
        if self.offset <= int(re.findall(r'共(.*?)页', page_info)[0]):
            print('当前正在爬取%s岗位的第' % self.keyword, self.offset, '页...')
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
