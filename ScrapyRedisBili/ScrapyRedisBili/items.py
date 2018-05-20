# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyredisbiliItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    home_url = scrapy.Field()
    mid = scrapy.Field()
    name = scrapy.Field()
    face_img = scrapy.Field()
    curr_level = scrapy.Field()
    sex = scrapy.Field()
    regtime = scrapy.Field()
    follower = scrapy.Field()
    following = scrapy.Field()
