# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyuItem(scrapy.Item):
    image_link = scrapy.Field()
    image_path = scrapy.Field()
    nick_name = scrapy.Field()
    room_id = scrapy.Field()
    city = scrapy.Field()
    source = scrapy.Field()
