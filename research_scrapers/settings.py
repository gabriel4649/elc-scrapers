# Scrapy settings for elc-scrapers project
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
DOWNLOAD_DELAY = 0.5    # 500 ms of delay

COOKIES_ENABLED = False

COOKIES_DEBUG = False

ITEM_PIPELINES = [
     'research_scrapers.pipelines.TextFileExportPipeline'
]

BOT_NAME = "Googlebot/2.X (+http://www.googlebot.com/bot.html)"
