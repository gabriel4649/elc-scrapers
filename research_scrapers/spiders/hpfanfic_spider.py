from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import FormRequest
from scrapy.http.request import Request

from spider_helpers.SpiderUtils import make_url_absolute, days_hours_minutes, ThreadParser
from spider_helpers.HPFanFicHelper import HPFanFicHelper

class HPFanFicSpider(CrawlSpider, ThreadParser):
    name = 'hpfanfic'
    allowed_domains = ['hpfanfictionforums.com']
    start_urls = ['http://www.hpfanfictionforums.com/index.php?act=idx']

    rules = (
        Rule(SgmlLinkExtractor(allow='index.php?showforum=\d+')),
        Rule(SgmlLinkExtractor(allow='index.php?showforum=\d+&prune_day=100&sort_by=Z-A&sort_key=last_post&topicfilter=all&page=\d+')),
        Rule(SgmlLinkExtractor(allow='index.php?showtopic=\d+'), callback='parse_thread'),
      )

    def __init__(self):
        CrawlSpider.__init__(self)
        ThreadParser.__init__(self, HPFanFicHelper)
