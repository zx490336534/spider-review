# -*- coding: utf-8 -*-
import scrapy
from Chinaarea.items import ChinaareaItem


class AirSpider(scrapy.Spider):
    name = 'air'
    allowed_domains = ['aqistudy.cn']
    base_url = 'https://www.aqistudy.cn/historydata/'
    start_urls = [base_url]

    def parse(self, response):
        print('正在爬取城市信息...')
        url_list = response.xpath('//div[@class="all"]/div[@class="bottom"]//a/@href').extract()
        city_list = response.xpath('//div[@class="all"]/div[@class="bottom"]//a/text()').extract()
        for city, url in zip(city_list, url_list):
            link = self.base_url + url
            yield scrapy.Request(url=link, callback=self.parse_month, meta={'city': city})

    def parse_month(self, response):
        print('正在爬取城市月份...')
        url_list = response.xpath('//tr/td/a/@href').extract()
        for url in url_list:
            url = self.base_url + url
            yield scrapy.Request(url=url, meta={'city': response.meta['city']}, callback=self.parse_day)

    def parse_day(self, response):
        print('正在爬取最终数据...')
        node_list = response.xpath('//tr')
        node_list.pop(0)
        for node in node_list:
            item = ChinaareaItem()
            item['city'] = response.meta['city']
            item['data'] = node.xpath('./td[1]/text()').extract_first()
            item['aqi'] = node.xpath('./td[2]/text()').extract_first()
            item['lever'] = node.xpath('./td[3]//text()').extract_first()
            item['pm2_5'] = node.xpath('./td[4]/text()').extract_first()
            item['pm10'] = node.xpath('./td[5]/text()').extract_first()
            item['so2'] = node.xpath('./td[6]/text()').extract_first()
            item['co'] = node.xpath('./td[7]/text()').extract_first()
            item['no2'] = node.xpath('./td[8]/text()').extract_first()
            item['o3'] = node.xpath('./td[9]/text()').extract_first()
            yield item

