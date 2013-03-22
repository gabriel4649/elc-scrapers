from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from research_scrapers.spiders.spider_helpers.OverclockedHelper import OverclockedHelper

class OverclockedSpider(CrawlSpider, OverclockedHelper):
    name = 'overclocked'
    allowed_domains = ['ocremix.org']
    start_urls = ['http://ocremix.org/forums/index.php']

    rules = (
        Rule(SgmlLinkExtractor(allow='forums/showthread.php\?t=\d+',
                               deny='.*page=\d+.*'), callback='parse_thread', follow=False),
        Rule(SgmlLinkExtractor(allow='forums/forumdisplay.php\?f=\d+&order=desc&page=\d+')),
        Rule(SgmlLinkExtractor(allow='forums/forumdisplay.php\?f=\d+')),
      )

    def __init__(self):
        CrawlSpider.__init__(self)
        OverclockedHelper.__init__(self)
