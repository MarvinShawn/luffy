# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import pymongo
from PIL import  Image
from io import BytesIO
import requests


class ImgRatioPipeline(object):
    def process_item(self,item,spider):
        if item['contentImg']:
            try:
                res = requests.get(item['contentImg'])
                tmpImg = BytesIO(res.content)
                img = Image.open(tmpImg)
                w, h = img.size
                item['ratio'] = round(w / h, 4)
            except Exception:
                raise DropItem("contentImg is invalid in %s" % item)
        return item



class MongoDBPipeline(object):

    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        #需要去重
        name = item.__class__.__name__
        self.db[name].update({'tag':item['tag']},{'$set':item},True)
        return item
