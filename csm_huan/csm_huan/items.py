# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CsmHuanItem(scrapy.Item):
    # 频道
    channel = scrapy.Field()
    # 节目
    program = scrapy.Field()
    # 实时收视率
    audience_rating = scrapy.Field()
    # 收视率对应的时间
    time_xAxis = scrapy.Field()
    # 收视率
    series = scrapy.Field()
