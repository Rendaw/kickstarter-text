# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class MobyItem(Item):
    db_table_name = 'rawnames'
    value = Field()

class KickstarterItem(Item):
    db_table_name = 'projects'
    title = Field()
    goal = Field()
    currency = Field()
    date = Field()
    rawtext = Field()
    web = Field()

