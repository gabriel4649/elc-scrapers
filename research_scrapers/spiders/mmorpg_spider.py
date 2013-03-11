from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from spider_helpers.MMORPGHelper import MMORPGHelper

class MMORPGSpider(CrawlSpider, MMORPGHelper):
    name = 'mmorpg'
    allowed_domains = ['mmorpgforum.com']
    start_urls = ['http://www.mmorpgforum.com/']

    rules = (
        Rule(SgmlLinkExtractor(allow='showthread.php\?t=\d+'), callback='parse_thread', follow=False),
        Rule(SgmlLinkExtractor(allow='forumdisplay.php\?f=\d+')),
        Rule(SgmlLinkExtractor(allow='forumdisplay.php\?f=\d+&order=desc&page=\d+')),
      )

    def __init__(self):
        CrawlSpider.__init__(self)
        MMORPGHelper.__init__(self)
