# -*- coding: utf-8 -*-
import scrapy

from bossPro.items import BossproItem


class BossesSpider(scrapy.Spider):
    # 区分没个spider的名字
    name = 'bosses'
    # 允许的域名
    # allowed_domains = ['www.xxx.com']
    # url
    pageNum = 0
    index_url = "https://www.zhipin.com/c101010100-p100109/?page="
    # java_url = "https://www.zhipin.com/c101010100-p100101/?page="
    # 启动时候的url
    start_urls = ['https://www.zhipin.com/c101010100-p100109/?page=1']
    # start_urls = ['https://www.zhipin.com/c101010100-p100101/?page=1']

    # 默认调用start_urls里面的url的时候执行这个函数
    def parse(self, response):
        self.pageNum += 1
        li_list = response.xpath('//div[@class="job-list"]/ul/li')

        for li in li_list:
            item = BossproItem()

            item["company"] = li.xpath(".//div[@class='info-company']//a/text()")[0].extract()
            item["name"] = li.xpath(".//div[@class='info-primary']//div[@class='job-title']/text()")[0].extract()
            item["salary"] = li.xpath(".//div[@class='info-primary']//span[@class='red']//text()")[0].extract()
            item["position"], item["experience"], item["education"] = \
                li.xpath(".//div[@class='info-primary']/p/text()").extract()

            yield item

        if self.pageNum <= 5:
            next_url = self.index_url + str(self.pageNum)
            yield scrapy.Request(url=next_url, callback=self.parse)



