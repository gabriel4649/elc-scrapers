from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from spider_helpers.SpiderUtils import ThreadParser
from spider_helpers.HPFanFicHelper import HPFanFicHelper

class HPFanFicSpider(CrawlSpider, ThreadParser):
    name = 'hpfanfic'
    allowed_domains = ['hpfanfictionforums.com']
    start_urls = ['http://www.hpfanfictionforums.com/index.php']

    rules = (
        Rule(SgmlLinkExtractor(allow='showtopic=\d+', deny='page=\d+'), callback='parse_thread', follow=False),
        Rule(SgmlLinkExtractor(allow='showforum=\d+&prune_day=100&sort_by=Z-A&sort_key=last_post&topicfilter=all&page=\d+')),
        Rule(SgmlLinkExtractor(allow='showforum=\d+')),
      )

    def __init__(self):
        CrawlSpider.__init__(self)
        ThreadParser.__init__(self, HPFanFicHelper)
