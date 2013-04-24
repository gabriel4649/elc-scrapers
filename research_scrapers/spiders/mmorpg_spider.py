from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from spider_helpers.MMORPGHelper import MMORPGHelper

class MMORPGSpider(CrawlSpider, MMORPGHelper):
    name = 'mmorpg'
    allowed_domains = ['mmorpgforum.com']
    start_urls = ['http://www.mmorpgforum.com/']

    rules = (
        Rule(SgmlLinkExtractor(allow='t=[0-9]*', deny=('do=whoposted', 'member', 'order', 'find')), callback='parse_thread', follow=False),
        Rule(SgmlLinkExtractor(allow='f=[0-9]*')),
        Rule(SgmlLinkExtractor(allow='f=[0-9]*&order=desc&page=[0-9]')),
      )

    def __init__(self):
        CrawlSpider.__init__(self)
        MMORPGHelper.__init__(self)
