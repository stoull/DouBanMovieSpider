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

class Celebrity(scrapy.Item):
    # properties for scrapy object
    # indicate the types of object, have Director, Actor and Scenarist
    type = scrapy.Field()
    # the movie id which this object belongs to
    movie_id = scrapy.Field()

    # properties for database
    d_id = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()
    zodiac = scrapy.Field()
    livingTime = scrapy.Field()
    birthday = scrapy.Field(serializer=str)
    leaveday = scrapy.Field(serializer=str)
    birthplace = scrapy.Field()
    occupation = scrapy.Field()
    names_cn = scrapy.Field()
    names_en = scrapy.Field()
    family = scrapy.Field()
    imdb = scrapy.Field()
    intro = scrapy.Field()
    photoUrl = scrapy.Field()