# -*- coding: utf-8 -*-
import scrapy


class RenrenSpider(scrapy.Spider):
    name = 'renren'

    def start_requests(self):
        url = "http://www.renren.com/PLogin.do"

        yield scrapy.FormRequest(
            url=url,
            formdata={'email':'15168230644','password':'zx660644'},
            callback=self.parse
        )
        print('*'*30)

    def parse(self, response):
        print(response.body.decode('utf8'))
        name = response.xpath('//p[@class="status"]/text()').extract_first()
        friend = response.xpath('//div[@class="userhead"]/span/text()').extract_first()
        with open('renren.txt') as f:
            f.write(name)
            f.write(friend)

