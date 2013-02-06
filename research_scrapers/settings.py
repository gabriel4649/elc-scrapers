# Scrapy settings for deviant_art project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

SPIDER_MODULES = ['research_scrapers.spiders']
NEWSPIDER_MODULE = 'research_scrapers.spiders'

# Settings to avoid being banned
# http://doc.scrapy.org/en/latest/topics/practices.html
DOWNLOAD_DELAY = 0.25    # 250 ms of delay
COOKIES_ENABLED = False

ITEM_PIPELINES = [
     'research_scrapers.pipelines.NanoWrimoPipeline'
]
