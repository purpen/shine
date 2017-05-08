# -*- coding: utf-8 -*-
import pymongo
from scrapy import Request
from scrapy.exceptions import DropItem


class MongoPipeline(object):
    """
    Mongo DB 存储爬取结果数据
    """
    def __init__(self, mongo_uri, mongo_db, mongo_coll):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_coll = mongo_coll


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'),
            mongo_coll=crawler.settings.get('MONGO_COLL', 'stuffs')
        )


    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        spider.log('Start to run mongo pipeline!')

        # 验证url spider 直接跳过
        if isinstance(item, Request):
            spider.log('This is request and not store mongodb!!!')
            return item

        # 产品或内容执行存储
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('Missing {0}!'.format(data))
        if valid:
            self.db[self.mongo_coll].insert(dict(item))

        return item