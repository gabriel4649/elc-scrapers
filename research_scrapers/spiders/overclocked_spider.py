from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from research_scrapers.spiders.spider_helpers.OverclockedHelper import OverclockedHelper
from overclocked_urls import urls

class OverclockedSpider(CrawlSpider, OverclockedHelper):
    name = 'overclocked'
    allowed_domains = ['ocremix.org']
    #start_urls = ['http://ocremix.org/forums/index.php']
    start_urls = urls

    rules = (
        Rule(SgmlLinkExtractor(allow=r'forums/showthread\.php\?[tp]=\d+', \
                               deny=r'.*page=\d+.*'), callback='parse_thread', follow=False),
        #Rule(SgmlLinkExtractor(allow=r'forums/forumdisplay.php\?f=\d+&order=desc&page=\d+')),
        #Rule(SgmlLinkExtractor(allow=r'forums/forumdisplay.php\?f=\d+')),
      )

    def __init__(self):
        CrawlSpider.__init__(self)
        OverclockedHelper.__init__(self)
