# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from selenium import webdriver


class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    # allowed_domains = ['www.xxx.com']
    # start_urls = ['https://news.163.com/']
    # start_urls = ['https://news.163.com/']
    start_urls = ["https://news.163.com/"]

    def __init__(self):
        self.bro = webdriver.Chrome()

    def parse(self, response):
        # 解析出国内，国际，军事，航空对应url
        li_list = response.xpath('//div[@class="ns_area list"]/ul/li')
        index_list = [3, 4, 6, 7]
        news_list = []  # 存储的是四个板块对应的li标签
        for i in index_list:
            news_list.append(li_list[i])
        # 解析获取板块的url
        for li in news_list:
            url = li.xpath('./a/@href').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_news)

    def parse_news(self, response):
        print(response.xpath(
            '/html/body/div[1]/div[3]/div[4]/div[1]/div/div/ul/li/div/div[3]/div[1]/h3/a/text()').extract_first())

    def closed(self, spider):
        self.bro.quit()
