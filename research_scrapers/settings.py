# Scrapy settings for deviant_art project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'deviant_art'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['deviant_art.spiders']
NEWSPIDER_MODULE = 'deviant_art.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
DOWNLOAD_DELAY = 0.25    # 250 ms of delay

