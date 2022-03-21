# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import hashlib
from os.path import splitext

from DouBanMovieSpider.items import Moive, Celebrity
from DouBanMovieSpider.database import DBManager

class DoubanmoviespiderPipeline:

    def __init__(self):
        self.db = DBManager()
        self.db_path = self.db.db_file

    def open_spider(self, spider):
        # self.file = open('items.json', 'w')
        pass

    def close_spider(self, spider):
        # self.file.close()
        pass

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        # self.file.write(line)

        # set default values
        for field in item.fields:
            item.setdefault(field, None)

        if isinstance(item, Moive):
            self.db.insertMoiveItem(item)
        elif isinstance(item, Celebrity):
            self.db.insertCelerbrityItem(item)
        return item

class DoubanImagesPipeline(ImagesPipeline):

    # Custom images name
    def file_path(self, request, response=None, info=None, *, item=None):
        image_name = request.url.split('/')[-1]
        return image_name

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        adapter['image_paths'] = image_paths
        return item