# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

import xlwt
from scrapy.exceptions import DropItem


class PositionPipeline(object):
    def __init__(self):
        self.education = "本科"

    def process_item(self, item, spider):
        if item["education"]:
            if item["education"] == self.education:
                return item
        else:
            return DropItem("Missing Position")


class ExcelPipeline(object):
    def __init__(self):
        self.num = 1
        # 实例化一个excel对象
        self.book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        self.sheet = self.book.add_sheet("sheet1", cell_overwrite_ok=True)

    def process_item(self, item, spider):
        x = 0
        for key, value in item.items():
            if self.num == 1:
                self.sheet.write(0, x, key)
            self.sheet.write(self.num, x, value)
            x += 1
        self.num += 1

        return item

    def close_spider(self, spider):
        self.book.save("./work.xls")


class MongoPipeline(object):
    def __init__(self):
        host = settings["MONGO_URI"]
        port = settings["MONGO_PORT"]
        dbname = settings["MONGO_DB"]

        client = pymongo.MongoClient(host=host, port=port)

        self.mydb = client[dbname]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.mydb[name].insert(dict(item))

        return item


class MongoPipeline1(object):
    def __int__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_DB=crawler.settings.get("MONGO_DB")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
