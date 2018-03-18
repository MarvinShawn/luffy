# -*- coding: utf-8 -*-
from scrapy import Spider,Request
import re
from qiushibaike.items import  QiushiUser


class QiushiuserSpider(Spider):
    name = 'qiushiuser'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['http://www.qiushibaike.com/','https://www.qiushibaike.com/hot/','https://www.qiushibaike.com/imgrank/','https://www.qiushibaike.com/text/']

    def parse(self, response):
        for item in response.xpath('//div[@id="content-left"]/div[contains(@class,"article block untagged mb15")]'):

            user = QiushiUser(userId=None,
                              gender=True,
                              age = 0,
                              nickname=None,
                              marriage=None,
                              constellation=None,
                              job=None,
                              hometown=None,
                              qiushiage=None,
                              avatar=None,
                              fens=0,
                              focus=0,
                              works=0,
                              comments=0,
                              smilefaces=0,
                              handpicks=0,
                              isOpenTimeline=False
                              )

            # 头像
            icon = item.xpath('./div[@class="author clearfix"]/a[1]/img/@src').extract_first()
            if icon:
                user['avatar'] = "https:" + icon

            # 昵称
            nickname = item.xpath('./div[@class="author clearfix"]/a[2]/h2/text()').extract_first()
            if nickname:
                user['nickname'] = nickname.strip()

            # 年龄
            age = item.xpath('./div[@class="author clearfix"]/div/text()').extract_first()
            if age:
                user['age'] = int(age)

            # 性别
            gender = item.xpath('./div[@class="author clearfix"]/div[@class="articleGender womenIcon"]')
            if gender:
                user['gender'] = False
            else:
                user['gender'] = True
            user_url = item.xpath('./div[@class="author clearfix"]/a[1]/@href').extract_first()
            if user_url:
                user['userId'] =  re.findall(r"/users/(.+?)/", user_url)[0]
                t_url = response.urljoin(user_url)
                yield Request(url=t_url,callback=self.parse_user,meta=user)



    def parse_user(self,response):
        user = response.meta
        user_main = response.xpath('//div[@class="user-main clearfix"]')
        if user_main:
            user["isOpenTimeline"] = True
            user_statis1 = user_main.xpath('./div[@class="user-col-left"]/div[@class="user-statis user-block"][1]')

            fens_num = user_statis1.xpath('./ul/li[1]/text()').extract_first()
            if fens_num:
                user["fens"] = int(fens_num)

            focus_num = user_statis1.xpath('./ul/li[2]/text()').extract_first()
            if fens_num:
                user["focus"] = int(focus_num)

            works_num = user_statis1.xpath('./ul/li[3]/text()').extract_first()
            if works_num:
                user["works"] = int(works_num)

            comment_num = user_statis1.xpath('./ul/li[4]/text()').extract_first()
            if comment_num:
                user["comments"] = int(comment_num)

            smilefaces_num = user_statis1.xpath('./ul/li[5]/text()').extract_first()
            if smilefaces_num:
                user["smilefaces"] = int(smilefaces_num)

            handpicks_num = user_statis1.xpath('./ul/li[6]/text()').extract_first()
            if handpicks_num:
                user["handpicks"] = int(handpicks_num)

            user_statis2 = user_main.xpath('./div[@class="user-col-left"]/div[@class="user-statis user-block"][2]')

            marital_status = user_statis2.xpath('./ul/li[1]/text()').extract_first()
            if marital_status:
                user["marriage"] = marital_status

            constellation = user_statis2.xpath('./ul/li[2]/text()').extract_first()
            if constellation:
                user["constellation"] = constellation

            job = user_statis2.xpath('./ul/li[3]/text()').extract_first()
            if job:
                user["job"] = job

            hometown = user_statis2.xpath('./ul/li[4]/text()').extract_first()
            if hometown:
                user["hometown"] = hometown

            qiushiage = user_statis2.xpath('./ul/li[5]/text()').extract_first()
            if qiushiage:
                user["qiushiage"] =   int(qiushiage.replace("天",""))

        yield user


