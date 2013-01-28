from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule


class FanFicSpider(CrawlSpider):
    name = 'fanfic'
    allowed_domains = ['fanfiction.net']
    start_urls = ['http://www.fanfiction.net/forums/']

    rules = (
        Rule(SgmlLinkExtractor(allow='Items/'), callback='parse_item', follow=True),
        Rule(SgmlLinkExtractor(allow=('forums/\w+'))),
        Rule(SgmlLinkExtractor(allow=('forums/\w+/\w+'))),
        Rule(SgmlLinkExtractor(allow=('forums/\w+/\w+/\d+'))),
        Rule(SgmlLinkExtractor(allow=('topic/\d+/\d+/\d+/\w+')), callback='parse_thread'),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

    def parse_thread(self, response):
        print "HERE"
