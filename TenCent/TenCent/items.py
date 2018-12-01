# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
    #职位名称
    position_name = scrapy.Field()
    #详情链接
    position_link = scrapy.Field()
    #职位类别
    position_type = scrapy.Field()
    #招聘人数
    people_number = scrapy.Field()
    #工作地点
    work_location = scrapy.Field()
    #招聘时间
    publish_times = scrapy.Field()

class DetailItem(scrapy.Item):
    #工作职责
    position_zhize = scrapy.Field()
    #工作要求
    position_yaoqiu = scrapy.Field()
