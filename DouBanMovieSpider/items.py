# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class DoubanmoviespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Director(scrapy.Item):
    d_id = Field()
    name_cn = Field()
    name_en = Field()
    gender = Field()
    birthday = Field(serializer=str)
    leaveday = Field(serializer=str)
    birthplace = Field()
    imdb = Field()
    intro = Field()
    photoUrl = Field()