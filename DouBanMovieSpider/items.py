# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class DoubanmoviespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.scrapy.Field()
    pass

class Moive(scrapy.Item):
    m_id = scrapy.Field()
    name = scrapy.Field()
    directors = scrapy.Field()
    scenarists = scrapy.Field()
    actors = scrapy.Field()
    style = scrapy.Field()
    year = scrapy.Field()
    releaseDate = scrapy.Field()
    area = scrapy.Field()
    language = scrapy.Field()
    length = scrapy.Field()
    otherNames = scrapy.Field()
    score = scrapy.Field()
    synopsis = Field(serializer=str)
    imdb = scrapy.Field()
    doubanUrl = scrapy.Field()
    posterUrl = scrapy.Field()
    iconUrl = scrapy.Field()

class Director(scrapy.Item):
    d_id = scrapy.Field()
    name_cn = scrapy.Field()
    name_en = scrapy.Field()
    gender = scrapy.Field()
    birthday = scrapy.Field(serializer=str)
    leaveday = scrapy.Field(serializer=str)
    birthplace = scrapy.Field()
    imdb = scrapy.Field()
    intro = scrapy.Field()
    photoUrl = scrapy.Field()

class Scenarist(scrapy.Item):
    d_id = scrapy.Field()
    name_cn = scrapy.Field()
    name_en = scrapy.Field()
    gender = scrapy.Field()
    birthday = scrapy.Field(serializer=str)
    leaveday = scrapy.Field(serializer=str)
    birthplace = scrapy.Field()
    imdb = scrapy.Field()
    intro = scrapy.Field()
    photoUrl = scrapy.Field()

class Actor(scrapy.Item):
    d_id = scrapy.Field()
    name_cn = scrapy.Field()
    name_en = scrapy.Field()
    gender = scrapy.Field()
    birthday = scrapy.Field(serializer=str)
    leaveday = scrapy.Field(serializer=str)
    birthplace = scrapy.Field()
    imdb = scrapy.Field()
    intro = scrapy.Field()
    photoUrl = scrapy.Field()