# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
import os
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from items import Moive, Celebrity
from database import DBManager

class DoubanmoviespiderPipeline:

    def __init__(self):
        self.db = DBManager()
        self.db_path = self.db.db_file

    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        for field in item.fields:
            item.setdefault(field, None)

        if isinstance(item, Moive):
            self.db.insertMoiveItem(item)
        elif isinstance(item, Celebrity):
            self.db.insertCelerbrityItem(item)
        return item