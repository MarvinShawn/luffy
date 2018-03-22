# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import  Item,Field

# 内容Item
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
    type = Field()


class QiushiUser(Item):

    #用户id
    userId = Field()
    #性别
    gender = Field()
    #年龄
    age = Field()
    #用户昵称
    nickname = Field()
    #婚姻状态
    marriage = Field()
    #星座
    constellation = Field()
    #职业
    job = Field()
    #故乡
    hometown = Field()
    #糗龄
    qiushiage = Field()
    #用户图像
    avatar = Field()
    #粉丝数
    fens = Field()
    #关注数
    focus = Field()
    #发表的糗事数
    works = Field()
    #评论数
    comments = Field()
    #收到的笑脸数
    smilefaces = Field()
    #入选糗事精选
    handpicks = Field()
    #是否开启糗百个人动态
    isOpenTimeline = Field()

