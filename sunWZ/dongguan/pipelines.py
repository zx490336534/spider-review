# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json

class JsonWriterPipeline(object):
    def open_spider(self, spider):
        # 创建一个只写文件，指定文本编码格式为utf-8
        self.filename = open('sunwz.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.filename.write(content)
        return item

    def spider_closed(self, spider):
        self.filename.close()