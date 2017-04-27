# -*- coding: utf-8 -*-

from scrapy.http import Request, FormRequest
from scrapy.spiders import CrawlSpider
from sunny_sport.items import StudentItem, SportItem


class SunnysportSpider(CrawlSpider):
    name = "sunnysport"
    allowed_domains = ["hzaspt.sunnysport.org.cn"]
    start_url = 'http://hzaspt.sunnysport.org.cn/runner/index.html'

    def start_requests(self):
        """
        模拟表单登录
        """
        return [FormRequest(
            url='http://hzaspt.sunnysport.org.cn/login/',
            formdata={
                'username': '2015002507',
                'password': '2015002507'
            },
            # meta={'cookiejar': 1},
            callback=self.after_login
        )]

    def after_login(self, response):
        """
        登录后，爬取基本信息页面和长跑信息页面
        """
        return [Request(
            url=self.start_url,
            # meta={'cookiejar': response.meta['cookiejar']},
            cookies={'sessionid': 'clyid4a5s1c81hpygz2a26iqovla78jz'},
            dont_filter=True,
            callback=self.parse_main_page
        )]

    def parse_main_page(self, response):
        """
        解析个人信息页面
        """
        name = response.xpath('//div[@class="col-md-3"][1]/div[1]/div[2]/label/text()').extract_first()
        student_num = response.xpath('//div[@class="col-md-3"][1]/div[1]/div[3]/label/text()').extract_first()
        total_mileage = response.xpath('//div[@class="col-md-3"][2]/div[1]/div[2]//tr[1]/td[2]/text()').extract_first()
        total_avg_speed = response.xpath(
            '//div[@class="col-md-3"][2]/div[1]/div[2]//tr[2]/td[2]/text()').extract_first()
        valid_cnt = response.xpath('//div[@class="col-md-3"][2]/div[1]/div[2]//tr[3]/td[2]/text()').extract_first()
        yield StudentItem(
            name=name,
            student_num=student_num,
            total_mileage=total_mileage,
            total_avg_speed=total_avg_speed,
            valid_cnt=valid_cnt
        )

        yield Request(
            url='http://hzaspt.sunnysport.org.cn/runner/achievements.html',
            # meta={'cookiejar': response.meta['cookiejar']},
            cookies={'sessionid': 'clyid4a5s1c81hpygz2a26iqovla78jz'},
            callback=self.parse_sport_page
        )

    def parse_sport_page(self, response):
        """
        解析长跑信息
        """
        trs = response.xpath('//div[@class="col-md-8"]//tbody/tr')
        for tr in trs:
            cnt = tr.xpath('.//td[1]/text()').extract_first()
            date = tr.xpath('.//td[2]/text()').extract_first()
            time = tr.xpath('.//td[3]/text()').extract_first()
            mileage = tr.xpath('.//td[4]/text()').extract_first()
            avg_speed = tr.xpath('.//td[5]/text()').extract_first()
            is_valid = tr.xpath('.//td[6]/span[contains(@class,"glyphicon-ok")]').extract_first() and 1 or 0
            yield SportItem(
                cnt=cnt,
                date=date,
                time=time,
                mileage=mileage,
                avg_speed=avg_speed,
                is_valid=is_valid
            )
