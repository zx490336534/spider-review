# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from TenCent.items import TencentItem, DetailItem


class TencentPipeline(object):
    def open_spider(self, spider):
        self.file = open('Tencent.json', 'w', encoding='utf8')

    def process_item(self, item, spider):
        if isinstance(item, TencentItem):
            content = json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()


class DetailPipeline(object):
    def open_spider(self, spider):
        self.file = open('detail.json', 'w', encoding='utf8')

    def process_item(self, item, spider):
        if isinstance(item, DetailItem):
            content = json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()
