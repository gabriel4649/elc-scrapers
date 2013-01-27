# Scrapy settings for deviant_art project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'research_scrapers'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['research_scrapers.spiders']
NEWSPIDER_MODULE = 'research_scrapers.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
DOWNLOAD_DELAY = 0.25    # 250 ms of delay

ITEM_PIPELINES = [
     'research_scrapers.pipelines.NanoWrimoPipeline'
]
