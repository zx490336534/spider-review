# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from Douyu.settings import IMAGES_STORE
import os


class ImageSource(object):
    def process_item(self, item, spider):
        item['source'] = spider.name
        return item


class DouyuPipeline(ImagesPipeline):
    # 发送图片链接请求
    def get_media_requests(self, item, info):
        # 获取item数据的图片链接
        image_link = item['image_link']
        # 发送图片请求，响应会保存在settings中的IMAGES_STORE
        yield scrapy.Request(url=image_link)

    def item_completed(self, results, item, info):
        # 每个resultes表示一个图片的信息，去除这个图片的原本路径
        image_path = [x['path'] for ok, x in results if ok]
        # 先保存当前图片的路径
        old_name = IMAGES_STORE + image_path[0]
        print('*'*300)
        print(old_name)
        print('*' * 300)
        # 新建的当前图片的路径
        new_name = IMAGES_STORE + item['nick_name'] + '.jpg'
        item['image_path'] = new_name
        try:
            # 将原本路径的图片名，修改为新建的图片名
            os.rename(old_name, new_name)
        except:
            print('[INOF]:图片已被修改')
        return item
