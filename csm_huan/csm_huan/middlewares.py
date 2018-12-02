# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os
import time
import scrapy
from selenium import webdriver

from scrapy import signals


class SeleniumMiddleware(object):
    """
        使用浏览器访问
    """

    def process_request(self, request, spider):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chromedriver = "/home/zx/chrome_driver/chromedriver"
        # chromedriver = "././chromedriver"

        os.environ["webdriver.chrome.driver"] = chromedriver
        if request.url == 'http://www.csm-huan.com/index.html':
            # self.driver = webdriver.Chrome(executable_path=chromedriver)
            self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromedriver)
            self.driver.get(request.url)
            self.driver.implicitly_wait(8)
            self.driver.find_element_by_xpath('/html/body/div[2]/div/span').click()
            self.driver.find_element_by_id('zh_CN_btn').click()
            time.sleep(5)
            html = self.driver.page_source
            self.driver.quit()
            return scrapy.http.HtmlResponse(url=request.url, body=html, encoding='utf-8', request=request)
