# -*- coding: utf-8 -*-
import time
import scrapy
from Tanzhou.items import TanzhouItem


class TzSpider(scrapy.Spider):
    name = 'tz'  # 爬虫名字
    allowed_domains = ['tanzhouedu.com']  # 限制爬虫范围
    start_urls = ['http://www.tanzhouedu.com/mall/course/initAllCourse']  # 请求url的第一个链接
    offset = 0

    def parse(self, response):
        item = TanzhouItem()
        node_list = response.xpath('//div[@id="newCourse"]/div/div/ul/li')
        for node in node_list:
            item['money'] = node.xpath('./div/span/text()').extract_first()
            item['title'] = node.xpath('./a/@title').extract_first()
            yield item
        if not node_list:
            return
        self.offset += 20
        yield scrapy.Request(url="http://www.tanzhouedu.com/mall/course/initAllCourse?params.offset=" + str(
            self.offset) + "&params.num=20&keyword=&_=" + str(int(time.time() * 1000)), callback=self.parse)
        # url会被传送给Scheduler【调度器】整理入列
