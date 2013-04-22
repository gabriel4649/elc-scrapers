from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from research_scrapers.spiders.spider_helpers.ExampleHelper import ExampleHelper

class ExampleSpider(CrawlSpider, ExampleHelper):
    # Here goes the crawler name
    name = 'example'
    # Domains for which the crawler is constrained too
    allowed_domains = ['exampledomain.com']
    # URLs where the crawler should start scraping
    start_urls = ['http://www.exampledomain.com/']

    # Rules on what the scraper should do with the links it finds
    rules = (
        # Thread links should be given to the parse_thread method from the Helper
        Rule(SgmlLinkExtractor(allow='showthread.php\?t=\d+'), callback='parse_thread', follow=False),
        # Follow sub-forums
        Rule(SgmlLinkExtractor(allow='forumdisplay.php\?f=\d+')),
        # Follow all the sub-forum pages
        Rule(SgmlLinkExtractor(allow='forumdisplay.php\?f=\d+&order=desc&page=\d+')),
      )

    # Let's initialize the classes we are inheriting from.
    def __init__(self):
        CrawlSpider.__init__(self)
        ExampleHelper.__init__(self)
