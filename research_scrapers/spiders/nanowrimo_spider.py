from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.http.request import Request
from scrapy import log

from deviant_art.items import ForumPost, Profile

import re
from datetime import datetime

class NanoWrimoSpider(CrawlSpider):
    name = "nanowrimo"
    allowed_domains = ["nanowrimo.org"]
    rules = [Rule(SgmlLinkExtractor(allow=('forums/fanfiction\?page=\d+'))),
             #Rule(SgmlLinkExtractor(allow=('threads/[0-9]+\?page=[0-9]+')), callback='parse_posts'),
             Rule(SgmlLinkExtractor(allow=('threads/\d+', )), callback='parse_posts'),
             Rule(SgmlLinkExtractor(allow=('participants/[a-zA-Z0-9]+', )), callback='parse_profile')]
    start_urls = [
        "http://www.nanowrimo.org/en/forums/fanfiction"
    ]

    def parse_posts(self, response):
        hxs = HtmlXPathSelector(response)

        if 'fps' in response.meta:
            fps = response.meta['fps']
        else:
            fps = []

        posts = hxs.select("//div[@class='forum_thread_comment']")
        for p in posts:
            fp = ForumPost()
            fp['body'] = p.select(".//div[@class='forum_thread_comment_body']/p/text()").extract()
            fp['author'] = p.select(".//a[@class='forum_thread_comment_author']/text()").extract()
            fp['date'] = p.select(".//span[@class='created_time_ago']/@title").extract()[0]
            fp['url'] = response.url
            fps.append(fp)

        # Get links to next page in thread if there is a next page
        next_page = hxs.select("//a[@class='next_page']/@href").extract()

        # Check if there is another page
        if len(next_page) > 0:
            # There is another page
            next_page_url_relative = next_page[0]
            base_url = get_base_url(response)
            next_page_url = urljoin_rfc(base_url, next_page_url_relative)
            request = Request(next_page_url,
                      callback=self.parse_posts)
            request.meta['fps'] = fps
            return request
        # There is no other page, return forum post items
        else:
            first_post, last_post = fps[0], fps[-1]
            get_time_obj = lambda x: datetime.strptime(x, '%B %d, %Y %H:%M')
            time_delta_obj = get_time_obj(last_post['date']) - get_time_obj(first_post['date'])
            time_delta = self.days_hours_minutes(time_delta_obj)

            number_of_comments = len(fps)

            for fp in fps:
                fp['time_delta'] = time_delta
                fp['number_of_comments'] = number_of_comments

            return fps

    def parse_profile(self, response):
        hxs = HtmlXPathSelector(response)

        profile_box = hxs.select("//div[@id='profile_fact_sheet']")

        p = Profile()
        p['author'] = hxs.select("//h1[@id='profile_name']/text()").extract()
        p['age'] = profile_box.select(".//dt[text()='Age:']/following::dd[1]/text()").extract()
        p['location'] = profile_box.select(".//dt[text()='Location:']/following::dd[1]/text()").extract()
        p['occupation'] =  profile_box.select(".//dt[text()='Occupation:']/following::dd[1]/text()").extract()

        profile_bling = hxs.select("//div[@id='profile_bling']")
        years = profile_bling.select(".//div[@class='year']")
        p['participation'] = [y.select(".//img/@title").extract()[0] for y in years]
        p['url'] = response.url

        return p

    def days_hours_minutes(self, td):
        return td.days, td.seconds//3600, (td.seconds//60)%60
