# -*- coding: utf-8 -*-
import json
import scrapy
from Douyu.items import DouyuItem


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['douyucdn.cn']
    offset = 0
    base_url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset='
    start_urls = [base_url + str(offset)]

    def parse(self, response):
        node_list = json.loads(response.body.decode())['data']
        if not node_list:
            return
        for node in node_list:
            item = DouyuItem()
            item['image_link'] = node['vertical_src']
            item['nick_name'] = node['nickname']
            item['room_id'] = node['room_id']
            item['city'] = node['anchor_city']
            yield item
        self.offset += 20
        yield scrapy.Request(self.base_url + str(self.offset), callback=self.parse)
