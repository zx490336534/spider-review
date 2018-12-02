# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QcItem(scrapy.Item):
    # 数据源
    source = scrapy.Field()
    # 抓取时间
    utc_time = scrapy.Field()
    # 职位名称
    work_name = scrapy.Field()
    # 公司名称
    company = scrapy.Field()
    # 工作地点
    work_position = scrapy.Field()
    # 薪资范围
    salary = scrapy.Field()
    # 发布时间
    publishtime = scrapy.Field()
    # 详情页内容
    content = scrapy.Field()
    # 联系方式
    contace = scrapy.Field()

