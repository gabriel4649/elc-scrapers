from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from spider_helpers.FanArtHelper import FanArtHelper

from fanart_urls import urls

class FanArtSpider(CrawlSpider, FanArtHelper):
    name = 'fanart'
    allowed_domains = ['forums.fanart-central.net']
    start_urls = urls

    rules = (
        Rule(SgmlLinkExtractor(allow='viewtopic'), \
             callback='parse_thread', follow=False),
        #Rule(SgmlLinkExtractor(allow=r'viewforum\.php\?f=\d+&sid=\w+')),
        #Rule(SgmlLinkExtractor(allow= \
        #                       r'viewforum\.php\?f=\d+&topicdays=\d+&start=\d+&sid=\w+')),
      )

    def __init__(self):
        CrawlSpider.__init__(self)
        FanArtHelper.__init__(self)
