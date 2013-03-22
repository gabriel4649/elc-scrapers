from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from spider_helpers.DeviantArtHelper import DeviantArtHelper

class DeviantSpider(CrawlSpider, DeviantArtHelper):
    name = "deviantart"
    allowed_domains = ["deviantart.com"]
    start_urls = ["https://forum.deviantart.com/"]

    rules = (
    Rule(SgmlLinkExtractor(allow='\w+/\w+/\d+'), callback='parse_thread', follow=False),
    Rule(SgmlLinkExtractor(allow='\w+/w\+')),
    Rule(SgmlLinkExtractor(allow='\w+/w\+/\?offset=\d+')),
  )

    def __init__(self):
        CrawlSpider.__init__(self)
        DeviantArtHelper.__init__(self)
