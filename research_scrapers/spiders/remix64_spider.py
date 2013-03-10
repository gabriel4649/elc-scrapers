from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from spider_helpers.Remix64Helper import Remix64Helper

class Remix64Spider(CrawlSpider, Remix64Helper):
    name = 'remix64'
    allowed_domains = ['remix64.com']
    start_urls = ['http://www.remix64.com/board/index.php']

    rules = (
        Rule(SgmlLinkExtractor(allow='viewtopic.php\?f=\d+&t=\d+'), callback='parse_thread', follow=False),
        Rule(SgmlLinkExtractor(allow='viewforum.php\?f=\d+')),
        Rule(SgmlLinkExtractor(allow='viewforum.php\?f=\d+&start=\d+')),
      )

    def __init__(self):
        CrawlSpider.__init__(self)
        Remix64Helper.__init__(self)
