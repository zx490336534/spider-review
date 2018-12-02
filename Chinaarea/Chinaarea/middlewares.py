# -*- coding: utf-8 -*-
import os
import random
import time
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Chinaarea.settings import USER_AGENT as ua_list


class UserAgentMiddleware(object):
    """
        给每一个请求随机切换一个User-Agent
    """

    def process_request(self, request, spider):
        user_agent = random.choice(ua_list)
        request.headers['User-Agent'] = user_agent
        # request.meta['proxy'] = '' #切换代理
        # print(request.headers['User-Agent'])


class SeleniumMiddleware(object):
    """
        使用浏览器访问
    """

    def process_request(self, request, spider):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chromedriver = "/home/zx/chrome_driver/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        if request.url != 'https://www.aqistudy.cn/historydata/':
            self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromedriver)
            self.driver.get(request.url)
            time.sleep(2)
            html = self.driver.page_source
            self.driver.quit()
            return scrapy.http.HtmlResponse(url=request.url, body=html, encoding='utf-8', request=request)
