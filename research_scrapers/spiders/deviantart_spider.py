from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.http.request import Request
from scrapy import log

# from research_scrapers.items import ForumPost, Profile

import re
from datetime import datetime

# TODO Remove unused imports

class DeviantSpider(CrawlSpider):
    name = "deviantart"
    allowed_domains = ["deviantart.com"]
    start_urls = [
        "https://forum.deviantart.com/"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        forums = hxs.select("//td[@class='f bl']/strong/a/@href").extract()
        posts = []
        for forum in forums:
            print forum
            f = HtmlXPathSelector(Request(forum))
            print f
            f.select("//td[@class='d-topic f v np']/a/@href").extract()
            posts.append(f.select("//td[@class='d-topic f v np']/a/@href").extract())

        items = []
        for post in posts:
            p = HtmlXPathSelector(Request(post))
            fp = ForumPost()
            fp['title'] = p.select('//h1/text()').extract()[2]
            fp['author']  = p.select('/html/body/div[2]/div/div[2]/div/div/div/div/div/span[2]/a/text()').extract()
            fp['link'] = p.select('a/@href').extract()

            items.append(fp)


        return fp
