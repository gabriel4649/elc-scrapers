from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from spider_helpers.TTHFanFicHelper import TTHFanFicHelper

class TTHFanFicSpider(CrawlSpider, TTHFanFicHelper):
    name = 'tthfanfic'
    allowed_domains = ['tthfanfic.org']
    start_urls = ['http://forum.tthfanfic.org/']

    rules = (
        Rule(SgmlLinkExtractor(allow='index.php\?topic=\d+\.0'), callback='parse_thread', follow=False),
        Rule(SgmlLinkExtractor(allow='index.php\?board=\d+\.\d+')),
      )

    def __init__(self):
        CrawlSpider.__init__(self)
        TTHFanFicHelper.__init__(self)
