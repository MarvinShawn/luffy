# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import  Item,Field


class QiushiItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    comments = Field()
    likes = Field()
    contentText = Field()
    nickname = Field()
    avatar = Field()
    age = Field()
    gender = Field()
    contentImg = Field()
    ratio = Field()
    tag = Field()

# 热门
class HotItem(QiushiItem):
    pass

# 24小时
class NewItem(QiushiItem):
    pass

# 热图
class ImageItem(QiushiItem):
    pass

# 文字
class TextItem(QiushiItem):
    pass

