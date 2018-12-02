# -*- coding: utf-8 -*-
import json
import scrapy
from csm_huan.items import CsmHuanItem


class CsmSpider(scrapy.Spider):
    name = 'csm'
    allowed_domains = ['csm-huan.com']
    base_url = 'http://www.csm-huan.com/'
    start_urls = ['http://www.csm-huan.com/index.html']
    history_compare = 'http://www.csm-huan.com/history_compare'

    def parse(self, response):
        channel_list = response.xpath('//*[@id="tbodys"]/tr/td[1]/a/text()').extract()
        program_list = response.xpath('//*[@id="tbodys"]/tr/td[2]/a/text()').extract()
        rating_list = response.xpath('//*[@id="tbodys"]/tr/td[3]/a/span/text()').extract()
        channel_code_list = response.xpath('//*[@id="tbodys"]/tr/td[1]/a/@href').extract()
        for channel, program, rating, channel_code in zip(channel_list, program_list, rating_list, channel_code_list):
            item = CsmHuanItem()
            item['channel'] = channel
            item['program'] = program
            item['audience_rating'] = rating
            code = channel_code.split('=')[-1]
            print(channel_code)
            print(type(channel_code))
            data = {
                'channel_codes': code,
                'flag': 'hour',
                'queryType': 'all',
            }
            print(data)
            yield scrapy.FormRequest(
                url=self.history_compare,
                formdata=data,
                callback=self.history_compare_parse,
                meta={'item': item}
            )

    def history_compare_parse(self, response):
        item = response.meta['item']
        info = response.body.decode()
        info = json.loads(info)
        item['time_xAxis'] = info.get('option').get('xAxis')[0].get('data')
        item['series'] = info.get('option').get('series')[0].get('data')
        yield item
