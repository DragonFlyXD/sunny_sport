# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class StudentItem(Item):
    """
    name 姓名
    student_num 学号
    total_mileage 总里程
    total_avg_speed 总平均速度
    valid_cnt 有效次数
    """

    name = Field()
    student_num = Field()
    total_mileage = Field()
    total_avg_speed = Field()
    valid_cnt = Field()


class SportItem(Item):
    """
    cnt 长跑次数
    date 长跑日期
    time 长跑时段
    mileage 长跑里程
    avg_speed 长跑平均速度
    is_valid 长跑是否有效 (1有效 0无效)
    """
    cnt = Field()
    date = Field()
    time = Field()
    mileage = Field()
    avg_speed = Field()
    is_valid = Field()
