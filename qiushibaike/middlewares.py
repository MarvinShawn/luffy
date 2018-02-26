# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import  webdriver
from selenium.webdriver.support.ui import WebDriverWait
from scrapy.http import  HtmlResponse


class JSMiddleware(object):

    def process_request(self,request,spider):
        print("PhantomJS is starting")
        configure = ['--load-images=false','--disk-cache=true']
        driver = webdriver.PhantomJS(service_args=configure)
        wait = WebDriverWait(driver,10)
        driver.set_window_size(1400,900)
        driver.get(request.url)
        body = driver.page_source
        return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)


