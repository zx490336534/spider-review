# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TanzhouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 课程金额
    money = scrapy.Field()
    # 课程名字
    title = scrapy.Field()
