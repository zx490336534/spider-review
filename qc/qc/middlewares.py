# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import redis
import hashlib
from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from qc.settings import USER_AGENT as ua_list


class QcSpiderMiddleware(object):
    """
        给每一个请求随机切换一个User-Agent
    """

    def process_request(self, request, spider):
        user_agent = random.choice(ua_list)
        request.headers['User-Agent'] = user_agent


class QcRedisMiddleware(object):
    """
        把每一个URL放到redis.set中，防止重复爬取
    """

    def __init__(self):
        self.sr = redis.StrictRedis(host='localhost', port=6379, db=1)

    def process_request(self, request, spider):
        if request.url.startswith('https://jobs.51job.com/'):
            # MD5压缩详情页链接(必须是bytes类型数据)
            url_md5 = hashlib.md5(request.url.encode()).hexdigest()
            result = self.sr.sadd('qc_url', url_md5)
            if not result:
                raise IgnoreRequest
