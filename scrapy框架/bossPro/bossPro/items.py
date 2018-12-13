# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BossproItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    company = scrapy.Field()
    position = scrapy.Field()
    salary = scrapy.Field()
    workPlace = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()


