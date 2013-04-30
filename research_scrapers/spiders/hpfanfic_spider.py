from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from spider_helpers.HPFanFicHelper import HPFanFicHelper

class HPFanFicSpider(CrawlSpider, HPFanFicHelper):
    name = 'hpfanfic'
    allowed_domains = ['hpfanfictionforums.com']

    # All the forums and sub-forums in:
    # http://www.hpfanfictionforums.com/index.php?act=idx
    start_urls = \
       ["http://www.hpfanfictionforums.com/index.php?showforum=2",
        "http://www.hpfanfictionforums.com/index.php?showforum=10",
        "http://www.hpfanfictionforums.com/index.php?showforum=115",
        "http://www.hpfanfictionforums.com/index.php?showforum=281",
        "http://www.hpfanfictionforums.com/index.php?showforum=160",
        "http://www.hpfanfictionforums.com/index.php?showforum=14",
        "http://www.hpfanfictionforums.com/index.php?showforum=135",
        "http://www.hpfanfictionforums.com/index.php?showforum=169",
        "http://www.hpfanfictionforums.com/index.php?showforum=360",
        "http://www.hpfanfictionforums.com/index.php?showforum=7",
        "http://www.hpfanfictionforums.com/index.php?showforum=1",
        "http://www.hpfanfictionforums.com/index.php?showforum=3",
        "http://www.hpfanfictionforums.com/index.php?showforum=6",
        "http://www.hpfanfictionforums.com/index.php?showforum=44",
        "http://www.hpfanfictionforums.com/index.php?showforum=43",
        "http://www.hpfanfictionforums.com/index.php?showforum=45",
        "http://www.hpfanfictionforums.com/index.php?showforum=273",
        "http://www.hpfanfictionforums.com/index.php?showforum=138",
        "http://www.hpfanfictionforums.com/index.php?showforum=4",
        "http://www.hpfanfictionforums.com/index.php?showforum=119",
        "http://www.hpfanfictionforums.com/index.php?showforum=19",
        "http://www.hpfanfictionforums.com/index.php?showforum=193",
        "http://www.hpfanfictionforums.com/index.php?showforum=206",
        "http://www.hpfanfictionforums.com/index.php?showforum=267",
        "http://www.hpfanfictionforums.com/index.php?showforum=9",
        "http://www.hpfanfictionforums.com/index.php?showforum=112",
        "http://www.hpfanfictionforums.com/index.php?showforum=30",
        "http://www.hpfanfictionforums.com/index.php?showforum=29",
        "http://www.hpfanfictionforums.com/index.php?showforum=165",
        "http://www.hpfanfictionforums.com/index.php?showforum=385",
        "http://www.hpfanfictionforums.com/index.php?showforum=166",
        "http://www.hpfanfictionforums.com/index.php?showforum=147",
        "http://www.hpfanfictionforums.com/index.php?showforum=148",
        "http://www.hpfanfictionforums.com/index.php?showforum=149",
        "http://www.hpfanfictionforums.com/index.php?showforum=150",
        "http://www.hpfanfictionforums.com/index.php?showforum=152",
        "http://www.hpfanfictionforums.com/index.php?showforum=142"]

    rules = (
        Rule(SgmlLinkExtractor(allow='.*topic.*'), \
             callback=r'parse_thread', follow=False),
        Rule(SgmlLinkExtractor( \
                                allow=r'showforum=\d+&prune_day=100&sort_by=Z-A&sort_key=last_post&topicfilter=all&page=\d+', deny=('setlanguage', 'cal_id', 'views', 'posts', 'start_data', 'st=&'))),
        #Rule(SgmlLinkExtractor(allow=r'showforum=\d+', deny=('sort'))),
    )

    def __init__(self):
        CrawlSpider.__init__(self)
        HPFanFicHelper.__init__(self)
