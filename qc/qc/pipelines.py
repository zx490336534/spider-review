# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
import pymysql
from datetime import datetime


class QcPipeline(object):
    def process_item(self, item, spider):
        item['source'] = spider.name
        item['utc_time'] = str(datetime.utcnow())
        return item


class QcJsonPipeline(object):
    def open_spider(self, spider):
        self.file = open('q51.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()


class QcMongoPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.collection = self.client['qc']['qc']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()


class QcMysqlPipeline(object):
    def open_spider(self, spider):
        self.con = pymysql.connect(host='localhost', port=3306, database='qiancheng', user='root', password='qwe123',
                                   charset="utf8")
        self.cur = self.con.cursor()

    def process_item(self, item, spider):
        sql = (
            "insert into qiancheng(source,utcTime,workName,company,workPosition,salary,publishtime,content,contact) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        list_item = [item['source'], item['utc_time'], item['work_name'], item['company'], item['work_position'],
                     item['salary'], item['publishtime'], item['content'], item['contace']]
        self.cur.execute(sql, list_item)
        self.con.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.con.close()


"""
mysql表格
create table qiancheng
(
    id INT unsigned PRIMARY KEY auto_increment NOT NULL,
    source VARCHAR(20) DEFAULT "",
    utcTime DATETIME DEFAULT "1111-11-11 11:11:11",
    workName VARCHAR(40) DEFAULT "",
    company VARCHAR(40) DEFAULT "",
    workPosition VARCHAR(40) DEFAULT "",
    salary VARCHAR(40) DEFAULT "",
    publishTime VARCHAR(20) DEFAULT "",
    content TEXT(1024),
    contact VARCHAR(40) DEFAULT ""
);
"""
