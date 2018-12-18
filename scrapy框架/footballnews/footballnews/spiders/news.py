# -*- coding: utf-8 -*-
import json
import scrapy

from footballnews.items import FootballnewsItem


class NewsSpider(scrapy.Spider):
    name = 'news'
    pageNum = 1
    # allowed_domains = ['www.xxx.com']
    base_url = "http://www.dongqiudi.com/archives/56?page={}"
    start_urls = ['http://www.dongqiudi.com/archives/56?page=1']

    def parse(self, response):
        news_info_list = json.loads(response.text).get("data")

        item = FootballnewsItem()

        for info in news_info_list:
            article_type = info["type"]
            item["type"] = article_type
            if article_type != "article":
                continue
            item["title"] = info.get("title")
            item["display_time"] = info.get("display_time")
            next_url = info.get("web_url")
            item["web_url"] = next_url

            yield scrapy.Request(url=next_url, callback=self.content_parse, meta={"item": item})

        if self.pageNum < 20:
            self.pageNum += 1
            req_url = self.base_url.format(str(self.pageNum))
            yield scrapy.Request(url=req_url, callback=self.parse)

    def content_parse(self, response):
        item = response.meta["item"]
        content = "".join(response.xpath("//div[@class='detail']/div[1]//text()").extract())
        item["content"] = content

        yield item
