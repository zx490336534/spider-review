"""
Base class for Scrapy spiders

See documentation in docs/topics/spiders.rst
"""
import logging
import warnings

from scrapy import signals
from scrapy.http import Request
from scrapy.utils.trackref import object_ref
from scrapy.utils.url import url_is_from_spider
from scrapy.utils.deprecate import create_deprecated_class
from scrapy.exceptions import ScrapyDeprecationWarning
from scrapy.utils.deprecate import method_is_overridden


class Spider(object_ref):
    """Base class for scrapy spiders. All spiders must inherit from this
    class.
    所有爬虫的基类，用户定义的爬虫必须从这个类继承
    """

    #定义spider名字的字符串(string),spider的名字定义了Scrapy如何定位（并初始化）spider，所以必须是唯一的。
    #name是spider最重要的属性，而且是必须的
    #一般做法是以该网站(domain)(加或不加 后缀)来命名spider，例如如果spider爬取mywebsite.com，该spider通常会被命名为mywebsite
    name = None
    custom_settings = None

    #初始化，提取爬虫名字，start_urls
    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        #如果爬虫没有名字，中断后续操作且报错
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        # python 对象或类型通过内置成员__dict__来存储成员信息
        self.__dict__.update(kwargs)
        #URL列表，当没有指定的URL，spider将从该列表中开始进行爬取，因此，第一个被获取到的页面的URL将是该列表之一
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

    @property
    def logger(self):
        logger = logging.getLogger(self.name)
        return logging.LoggerAdapter(logger, {'spider': self})

    #打印Scrapy执行后的log信息
    def log(self, message, level=logging.DEBUG, **kw):
        """Log the given message at the given log level

        This helper wraps a log call to the logger within the spider, but you
        can use it directly (e.g. Spider.logger.info('msg')) or use any other
        Python logger too.
        """
        self.logger.log(level, message, **kw)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    # 判断对象object的属性是否存在，不存在做断言处理
    def set_crawler(self, crawler):
        warnings.warn("set_crawler is deprecated, instantiate and bound the "
                      "spider to this crawler with from_crawler method "
                      "instead.",
                      category=ScrapyDeprecationWarning, stacklevel=2)
        assert not hasattr(self, 'crawler'), "Spider already bounded to a " \
                                             "crawler"
        self._set_crawler(crawler)

    def _set_crawler(self, crawler):
        self.crawler = crawler
        self.settings = crawler.settings
        crawler.signals.connect(self.close, signals.spider_closed)

    #该方法将读取start_urls内的地址，并为每个地址生成一个Request对象，交给Scrapu下载并返回Response
    #该方法仅调用一次
    def start_requests(self):
        cls = self.__class__
        if method_is_overridden(cls, Spider, 'make_requests_from_url'):
            warnings.warn(
                "Spider.make_requests_from_url method is deprecated; it "
                "won't be called in future Scrapy releases. Please "
                "override Spider.start_requests method instead (see %s.%s)." % (
                    cls.__module__, cls.__name__
                ),
            )
            for url in self.start_urls:
                yield self.make_requests_from_url(url)
        else:
            for url in self.start_urls:
                yield Request(url, dont_filter=True)

    #start_requests()中调用，实际生成Request的函数
    #Request对象默认的回调函数为parse()，提交方式为get
    def make_requests_from_url(self, url):
        """ This method is deprecated. """
        return Request(url, dont_filter=True)

    #默认的Request对象回调函数，处理返回的response
    #生成Item或者Request对象，用户必须实现这个类
    def parse(self, response):
        raise NotImplementedError('{}.parse callback is not defined'.format(self.__class__.__name__))

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(cls.custom_settings or {}, priority='spider')

    @classmethod
    def handles_request(cls, request):
        return url_is_from_spider(request.url, cls)

    @staticmethod
    def close(spider, reason):
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)

    def __str__(self):
        return "<%s %r at 0x%0x>" % (type(self).__name__, self.name, id(self))

    __repr__ = __str__


BaseSpider = create_deprecated_class('BaseSpider', Spider)


class ObsoleteClass(object):
    def __init__(self, message):
        self.message = message

    def __getattr__(self, name):
        raise AttributeError(self.message)

spiders = ObsoleteClass(
    '"from scrapy.spider import spiders" no longer works - use '
    '"from scrapy.spiderloader import SpiderLoader" and instantiate '
    'it with your project settings"'
)

# Top-level imports
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.spiders.feed import XMLFeedSpider, CSVFeedSpider
from scrapy.spiders.sitemap import SitemapSpider
