from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from research_scrapers.spiders.spider_helpers.EtsyHelper import EtsyHelper

class EtsySpider(CrawlSpider, EtsyHelper):
    # Here goes the crawler name
    name = 'etsy'
    # Domains for which the crawler is constrained too
    allowed_domains = ['etsy.com']
    # URLs where the crawler should start scraping
    start_urls = ["http://www.etsy.com/teams/7720/bugs/discuss/",
                  "http://www.etsy.com/teams/7714/ideas/discuss/",
                  "http://www.etsy.com/teams/7722/business-topics/discuss/",
                  "http://www.etsy.com/teams/7718/site-help/discuss/",
                  "http://www.etsy.com/teams/7716/announcements/discuss/"]

    # Rules on what the scraper should do with the links it finds
    rules = (
        # Thread links should be given to the parse_thread method from the Helper
        Rule(SgmlLinkExtractor(allow=r'discuss/\d+', deny='page'), callback='parse_thread', follow=False),
        # Follow sub-forums

        #Rule(SgmlLinkExtractor(allow=r'teams\/\d+\/.*\/discuss\/')),
        # Follow all the sub-forum pages

        Rule(SgmlLinkExtractor(allow=r'discuss/page/\d+')),
      )

    # Let's initialize the classes we are inheriting from.
    def __init__(self):
        CrawlSpider.__init__(self)
        EtsyHelper.__init__(self)
