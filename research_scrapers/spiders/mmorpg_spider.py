from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from spider_helpers.HPFanFicHelper import MMORPGHelper

class MMORPGSpider(CrawlSpider, MMORPGHelper):
    name = 'mmorpg'
    allowed_domains = ['mmorpgforum.com']
    start_urls = ['http://www.mmorpgforum.com/']

    rules = (
        Rule(SgmlLinkExtractor(allow='showtopic=\d+', deny='page=\d+'), callback='parse_thread', follow=False),
        Rule(SgmlLinkExtractor(allow='showforum=\d+&prune_day=100&sort_by=Z-A&sort_key=last_post&topicfilter=all&page=\d+')),
        Rule(SgmlLinkExtractor(allow='showforum=\d+')),
      )

    def __init__(self):
        CrawlSpider.__init__(self)
        MMORPGHelper.__init__(self)
