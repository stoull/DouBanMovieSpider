# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class Movie(scrapy.Item):
    m_id = scrapy.Field()
    name = scrapy.Field()
    directors = scrapy.Field()
    scenarists = scrapy.Field()
    actors = scrapy.Field()
    style = scrapy.Field()
    year = scrapy.Field()
    release_date = scrapy.Field()
    area = scrapy.Field()
    language = scrapy.Field()
    length = scrapy.Field()
    other_names = scrapy.Field()
    score = scrapy.Field()
    rating_number = scrapy.Field()
    synopsis = Field(serializer=str)
    imdb = scrapy.Field()
    poster_name = scrapy.Field()


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
    living_time = scrapy.Field()
    birthday = scrapy.Field(serializer=str)
    left_day = scrapy.Field(serializer=str)
    birthplace = scrapy.Field()
    occupation = scrapy.Field()
    is_director = scrapy.Field()
    is_scenarist = scrapy.Field()
    is_actor = scrapy.Field()
    names_cn = scrapy.Field()
    names_en = scrapy.Field()
    family = scrapy.Field()
    imdb = scrapy.Field()
    intro = scrapy.Field()
    portrait_name = scrapy.Field()


class MovieBriefItem(scrapy.Item):
    d_id = scrapy.Field()
    name = scrapy.Field(serializer=str)
    score = scrapy.Field()
    year = scrapy.Field()
    poster_name = scrapy.Field()

    # custom properties 用来区分存储事项
    location_type = scrapy.Field()  # 区分是来自电影页的'喜欢这部电影的人也喜欢 值为 movie' 还是来自人物页的'最受好评的5部作品 值为 celebrity'
    celebrity_id = scrapy.Field()  # 来自人物页的'最受好评的5部作品' 时有值
    movie_id = scrapy.Field()  # 当来自电影页的'喜欢这部电影的人也喜欢' 时有值


class HotComment(scrapy.Item):
    d_id = scrapy.Field()
    movie_id = scrapy.Field()
    content = scrapy.Field(serializer=str)
    reviewer_name = scrapy.Field(serializer=str)
    reviewer_id = scrapy.Field()


class Review(scrapy.Item):
    d_id = scrapy.Field()
    movie_id = scrapy.Field()
    title = scrapy.Field(serializer=str)
    content_short = scrapy.Field(serializer=str)
    content = scrapy.Field(serializer=str)
    reviewer_name = scrapy.Field(serializer=str)
    reviewer_id = scrapy.Field()


class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()

class Doubantop250Item(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    pass
