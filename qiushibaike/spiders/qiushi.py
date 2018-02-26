# -*- coding: utf-8 -*-
import scrapy

from qiushibaike.items import QiushiItem


class QiushiSpider(scrapy.Spider):
    name = 'qiushi'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com']

    def parse(self, response):
        for item in response.xpath('//div[@id="content-left"]/div[contains(@class,"article block untagged mb15")]'):
            qiubai = QiushiItem()

            # 糗事tagId
            tag = item.xpath('@id').extract_first()
            if tag:
                qiubai['tag'] = tag

            # 头像
            icon = item.xpath('./div[@class="author clearfix"]/a[1]/img/@src').extract()
            if icon:
                qiubai['avatar'] =  "https:" + icon[0]
            else:
                qiubai['avatar'] = None

            #昵称
            nickname = item.xpath('./div[@class="author clearfix"]/a[2]/h2/text()').extract()
            if nickname:
                qiubai['nickname'] = nickname[0].strip()
            else:
                qiubai['nickname'] = None

            #年龄
            age = item.xpath('./div[@class="author clearfix"]/div/text()').extract()
            if age:
                qiubai['age'] = int(age[0])
            else:
                qiubai['age'] = None

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
            else:
                qiubai['contentText'] = None

            #内容图片
            content_img = item.xpath('./div[@class="thumb"]/a/img/@src').extract()
            if content_img:
                qiubai['contentImg'] = "https:" + content_img[0]
            else:
                qiubai['contentImg'] = None
                qiubai['ratio'] = 0

            #喜欢数
            like = item.xpath('./div[@class="stats"]/span[@class="stats-vote"]/i/text()').extract()
            if like:
                qiubai['likes'] = int(like[0])
            else:
                qiubai['likes'] = 0

            #评论数
            comment = item.xpath('./div[@class="stats"]/span[@class="stats-comments"]/a/i/text()').extract()
            if comment:
                qiubai['comments'] = int(comment[0])
            else:
                qiubai['comments'] = 0
            yield qiubai

        #下一页
        next_page = response.xpath('//div[@id="content-left"]/ul[@class="pagination"]/li[last()]/a/@href').extract_first()
        url = response.urljoin(next_page)
        yield scrapy.Request(url=url, callback=self.parse)

