from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from research_scrapers.spiders.spider_helpers.EbaumsworldHelper import EbaumsworldHelper

class EbaumsworldSpider(CrawlSpider, EbaumsworldHelper):
    name = 'ebaums'
    allowed_domains = ['ebaumsworld.com']
    start_urls = ["http://forum.ebaumsworld.com/"]
    rules = (
        Rule(SgmlLinkExtractor(allow='showthread.php\?[0-9a-zA-Z\-]+',
                               deny='.*page\d+.*'), callback='parse_thread', follow=False),
        Rule(SgmlLinkExtractor(allow='forumdisplay.php\?[0-9]+-\w+')),
        Rule(SgmlLinkExtractor(allow='forumdisplay.php\?/[0-9]+-\w+/page\d+&order=desc')),
      )

    def __init__(self):
        CrawlSpider.__init__(self)
        EbaumsworldHelper.__init__(self)
