# -*- coding: utf-8 -*-
import scrapy

from scrapy_redis.spiders import RedisSpider
from redisSpiderPro.items import RedisspiderproItem
class RedisspidertestSpider(RedisSpider):
    name = 'redisSpiderTest'
    #allowed_domains = ['www.xxx,com']
    #start_urls = ['http://www.xxx,com/']
    redis_key = 'data' #调度器队列的名称
    url = 'http://db.pharmcube.com/database/cfda/detail/cfda_cn_instrument/'
    pageNum = 1
    def parse(self, response):
        num = response.xpath('/html/body/div/table/tbody/tr[1]/td[2]/text()').extract_first()
        name = response.xpath('/html/body/div/table/tbody/tr[2]/td[2]/text()').extract_first()

        item = RedisspiderproItem()
        item['num'] = num
        item['name'] = name

        yield item

        if self.pageNum <= 10000:
            self.pageNum += 1
            new_url = self.url + str(self.pageNum)
            yield scrapy.Request(url=new_url,callback=self.parse)
