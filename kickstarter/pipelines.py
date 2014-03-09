# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from kickstarter.nonspider import common
from scrapy import log

class SQLitePipeline(object):
    def __init__(self):
        self.connection = common.connect_db()

    def close_spider(self, spider):
        self.connection.commit()
        self.connection.close()

    def process_item(self, item, spider):
        query = 'INSERT OR IGNORE INTO {0} ({1}) VALUES ({2})'.format(
            item.db_table_name,
            ', '.join(item.keys()),
            '?' + ', ?' * (len(item) - 1)
        ) 
        self.connection.execute(query, tuple(item.values()))
        return item

