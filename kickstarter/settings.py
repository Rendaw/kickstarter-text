# Scrapy settings for kickstarter project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'kickstarter'

SPIDER_MODULES = ['kickstarter.spiders']
NEWSPIDER_MODULE = 'kickstarter.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = ''

DOWNLOAD_DELAY = 5

KICKSTARTER_DUMP_RESPONSE = True
KICKSTARTER_ENGLISH_WORD_FILE = '/usr/share/dict/cracklib-small'

ITEM_PIPELINES = {
    'kickstarter.pipelines.SQLitePipeline': 800,
}
