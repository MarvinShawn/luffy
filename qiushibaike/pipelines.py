# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from qiushibaike.items import QiushiItem,QiushiUser
import pymongo
from PIL import  Image
from io import BytesIO
import requests

# 这里是自己实现的获取图片宽高比 也可以 scrapy 提供的下载图片的ImagesPipeline
class ImgRatioPipeline(object):
    def process_item(self,item,spider):
        if isinstance(item, QiushiItem):
            if item['contentImg']:
                try:
                    res = requests.get(item['contentImg'])
                    tmpImg = BytesIO(res.content)
                    img = Image.open(tmpImg)
                    w, h = img.size
                    item['ratio'] = round(w / h, 4)
                except Exception:
                    raise DropItem("contentImg is invalid in %s" % item)
        elif isinstance(item, QiushiUser):
            pass
        return item



class MongoDBPipeline(object):


    def send_email(self,SMTP_host, from_account, from_passwd, to_account, subject, content):
        from email.header import Header
        from email.mime.text import MIMEText
        import smtplib
        print("开始发送邮件")
        email_client = smtplib.SMTP(SMTP_host,25)
        email_client.login(from_account, from_passwd)
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = from_account
        msg['To'] = to_account
        email_client.set_debuglevel(1)
        email_client.sendmail(from_account, to_account, msg.as_string())
        email_client.quit()
        print("发送邮件完成")

    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):

        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):

        if spider.name == "qiushiu":
            items_count = self.db["qiushiitems"].find({}).count()
            dic = spider.crawler.stats.get_stats()
            send_content = "qiushi_item_total_count -----> %d\n"%items_count
            for k, v in dic.items():
                send_content = send_content + k + " -----> " + str(v) + "\n"

            self.send_email("smtp.2980.com",
                            "marvinshawn@2980.com",
                            "123456qqq",
                            "511457709@qq.com",
                            "Scrapy Report",
                            send_content
                            )
        self.client.close()



    def process_item(self, item, spider):
        #需要去重
        name = item.__class__.__name__.lower() + 's'
        if isinstance(item, QiushiItem):
            self.db[name].update({'tag':item['tag']},{'$set':item},True)
        elif isinstance(item, QiushiUser):
            self.db[name].update({'userId': item['userId']}, {'$set': item}, True)
        return item
