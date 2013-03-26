from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from spider_helpers.FanArtHelper import FanArtHelper

class FanArtSpider(CrawlSpider, FanArtHelper):
    name = 'fanart'
    allowed_domains = ['fanart-central.net']
    start_urls = ['http://forums.fanart-central.net/']

    rules = (
        Rule(SgmlLinkExtractor(allow='viewtopic.php', deny='start'), callback='parse_thread', follow=False),
        Rule(SgmlLinkExtractor(allow='viewforum.php\?f=\d+&sid=\w+')),
        Rule(SgmlLinkExtractor(allow='viewforum.php\?f=\d+&topicdays=\d+&start=\d+&sid=\w+')),
      )

    def __init__(self):
        CrawlSpider.__init__(self)
        FanArtHelper.__init__(self)
