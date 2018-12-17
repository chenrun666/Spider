# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CrawltestSpider(CrawlSpider):
    name = 'crawlTest'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.qiushibaike.com/pic/']
    # 连接器提取对象： 去页面中提取符合要求的连接
    link = LinkExtractor(allow=r"/pic/page/\d+\?")
    link1 = LinkExtractor(allow=r"/pic/$")

    rules = (
        Rule(link, callback='parse_item', follow=True),
        Rule(link1, callback="parse_item", follow=True),
    )

    def parse_item(self, response):
        print(response)
