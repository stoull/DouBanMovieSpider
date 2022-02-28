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

class Moive(scrapy.Item):
    m_id = Field()
    name = Field()
    directors = Field()
    style = Field()
    releaseDate = Field(serializer=str)
    language = Field()
    length = Field()
    otherNames = Field()
    score = Field()
    synopsis = Field(serializer=str)
    imdb = Field()
    doubanUrl = Field()


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

class Scenarist(scrapy.Item):
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

class Actor(scrapy.Item):
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