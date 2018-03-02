# -*- coding: utf-8 -*-
from scrapy import Spider,Request,log

from qiushibaike.items import HotItem,NewItem,ImageItem,TextItem


class QiushiSpider(Spider):
    name = 'qiushi'
    allowed_domains = ['www.qiushibaike.com']

    # 热门
    hot_url = 'https://www.qiushibaike.com/'
    # 24小时
    tf_url = 'https://www.qiushibaike.com/hot/'
    #热图
    hotImg_url = 'https://www.qiushibaike.com/imgrank/'
    #文字
    word_url = 'https://www.qiushibaike.com/text/'


    def start_requests(self):
        yield Request(self.hot_url,callback=self.parse_hot)
        yield Request(self.tf_url,callback=self.parse_24hours)
        yield Request(self.hotImg_url,callback=self.parse_hotimg)
        yield Request(self.word_url,callback=self.parse_word)

    def parse_hot(self,response):
        return self.parse_item(response,HotItem)

    def parse_24hours(self,response):
        return self.parse_item(response, NewItem)

    def parse_hotimg(self,response):
        return self.parse_item(response, ImageItem)

    def parse_word(self,response):
        return self.parse_item(response, TextItem)


    def parse_item(self,response,cls):
        print('current Item = ',cls.__name__)
        for item in response.xpath('//div[@id="content-left"]/div[contains(@class,"article block untagged mb15")]'):
            qiubai = cls(comments=0,likes=0,contentText=None,nickname=None,avatar=None,age=0,gender=True,contentImg=None,ratio=0,tag=None)

            # 糗事tagId
            tag = item.xpath('@id').extract_first()
            if tag:
                qiubai['tag'] = tag

            # 头像
            icon = item.xpath('./div[@class="author clearfix"]/a[1]/img/@src').extract_first()
            if icon:
                qiubai['avatar'] =  "https:" + icon


            #昵称
            nickname = item.xpath('./div[@class="author clearfix"]/a[2]/h2/text()').extract_first()
            if nickname:
                qiubai['nickname'] = nickname.strip()


            #年龄
            age = item.xpath('./div[@class="author clearfix"]/div/text()').extract_first()
            if age:
                qiubai['age'] = int(age)


            #性别
            gender = item.xpath('./div[@class="author clearfix"]/div[@class="articleGender womenIcon"]')
            if gender:
                qiubai['gender'] = False
            else:
                qiubai['gender'] = True

            #内容
            content = item.xpath('./a/div[@class="content"]/span/text()').extract()
            if content:
                con = ''
                for str in content:
                    con += str
                qiubai['contentText'] = con.strip()


            #内容图片
            content_img = item.xpath('./div[@class="thumb"]/a/img/@src').extract_first()
            if content_img:
                qiubai['contentImg'] = "https:" + content_img


            #喜欢数
            like = item.xpath('./div[@class="stats"]/span[@class="stats-vote"]/i/text()').extract_first()
            if like:
                qiubai['likes'] = int(like)


            #评论数
            comment = item.xpath('./div[@class="stats"]/span[@class="stats-comments"]/a/i/text()').extract_first()
            if comment:
                qiubai['comments'] = int(comment)

            yield qiubai

        #下一页 更多除外
        next_page = response.xpath('//div[@id="content-left"]/ul[@class="pagination"]/li[last()]/a/@href').extract_first()
        has_more = response.xpath('//div[@id="content-left"]/ul[@class="pagination"]/li[last()]/a/span/text()').extract_first()

        if has_more and '更多' in has_more:
            pass
        elif next_page:
            url = response.urljoin(next_page)
            if cls is HotItem:
                yield Request(url=url, callback=self.parse_hot)
            elif cls is NewItem:
                yield Request(url=url, callback=self.parse_24hours)
            elif cls is ImageItem:
                yield Request(url=url, callback=self.parse_hotimg)
            elif cls is TextItem:
                yield Request(url=url, callback=self.parse_word)




