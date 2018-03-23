# -*- coding: utf-8 -*-
from scrapy import Spider,Request,log
import  re

from qiushibaike.items import QiushiItem


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
    #穿越
    pass_url = 'https://www.qiushibaike.com/history/'
    #糗图
    qiutu_url = 'https://www.qiushibaike.com/pic/'
    #新鲜
    fresh_url = 'https://www.qiushibaike.com/textnew/'



    def start_requests(self):
        yield Request(self.hot_url,callback=self.parse_item,meta={"type":0})
        yield Request(self.tf_url,callback=self.parse_item,meta={"type":1})
        yield Request(self.hotImg_url,callback=self.parse_item,meta={"type":2})
        yield Request(self.word_url,callback=self.parse_item,meta={"type":3})
        yield Request(self.pass_url,callback=self.parse_item,meta={"type":4})
        yield Request(self.qiutu_url,callback=self.parse_item,meta={"type":5})
        yield Request(self.fresh_url,callback=self.parse_item,meta={"type":6})




    def parse_detail(self,response):
        item = response.xpath('//div[@class="content"]').extract_first()
         # 使用正则替换
        reg = re.compile('(<div class="content">|</div>|<span>|</span>)')
        content_text = reg.sub("",item).replace("<br>","\n")
        if content_text:
            qs = response.meta['item']
            qs['contentText'] = content_text.strip()
            yield qs



    def parse_item(self,response):

        for item in response.xpath('//div[contains(@class,"article block untagged mb15")]'):
            qiubai = QiushiItem(comments=0,
                                likes=0,
                                contentText=None,
                                nickname=None,
                                avatar=None,
                                age=0,
                                gender=True,
                                contentImg=None,
                                ratio=0,
                                tag=None,
                                type=response.meta['type']
                                )

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

            # 内容
            content = item.xpath('./a/div[@class="content"]/span').extract()
            if content:
                if len(content) > 1:  # 包含了查看全部
                    detail_url = item.xpath('./a/@href').extract_first()
                    url = response.urljoin(detail_url)
                    yield Request(url=url, callback=self.parse_detail, meta={"item": qiubai})
                else:
                    creg = re.compile('(<span>|</span>)')
                    result = creg.sub("", content[0]).replace("<br>", "\n")
                    # result = content[0].replace("<span>", "").replace("</span>", "").replace("<br>", "\n")
                    if result:
                        qiubai['contentText'] = result.strip()

            yield qiubai

        #下一页 更多除外
        next_page = response.xpath('//div[@id="content-left"]/ul[@class="pagination"]/li[last()]/a/@href').extract_first()
        has_more = response.xpath('//div[@id="content-left"]/ul[@class="pagination"]/li[last()]/a/span/text()').extract_first()

        if has_more and '更多' in has_more:
            pass
        elif next_page:
            url = response.urljoin(next_page)
            yield  Request(url=url,callback=self.parse_item,meta={"type":response.meta["type"]})




