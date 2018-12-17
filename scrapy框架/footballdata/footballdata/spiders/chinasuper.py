# -*- coding: utf-8 -*-
import re
import datetime
import scrapy


class ChinasuperSpider(scrapy.Spider):
    name = 'chinasuper'
    # allowed_domains = ['www.xxx.com']
    detail_url = "http://zq.win007.com/jsData/teamInfo/teamDetail/tdl{}.js?version={}"
    start_url = 'http://zq.win007.com/cn/League/60.html'

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, meta={"useselenium": True})

    def parse(self, response):
        all_team_url = response.xpath("//tbody/tr/td[2]/a/@href").extract()

        # 匹配出url中的数字
        pattern = re.compile(r"\d+")
        # 获取当前时间
        current_time = datetime.datetime.now().strftime("%Y%m%d")
        for team_url in all_team_url:
            team_id = re.search(pattern, str(team_url)).group()
            next_url = self.detail_url.format(team_id, current_time + "19")
            yield scrapy.Request(url=next_url, callback=self.detail_parse, meta={"useselenium": True})
            break

    def detail_parse(self, response):
        # print(response.text)
        print(response)

