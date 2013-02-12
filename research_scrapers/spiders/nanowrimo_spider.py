from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from scrapy import log

from research_scrapers.items import ForumThread, Profile

from spider_helpers.SpiderUtils import days_hours_minutes, make_url_absolute, safe_list_get

import re
from datetime import datetime

class NanoWrimoSpider(CrawlSpider):
    name = "nanowrimo"
    allowed_domains = ["nanowrimo.org"]
    rules = [Rule(SgmlLinkExtractor(allow=('threads/[0-9]+')), callback='parse_posts'),
             Rule(SgmlLinkExtractor(allow=('forums/[A-Za-z0-9-]+'))),
             Rule(SgmlLinkExtractor(allow=('forums/[A-Za-z0-9-]+\?page=\d+'))),
             #Rule(SgmlLinkExtractor(allow=('threads/[0-9]+\?page=[0-9]+')), callback='parse_posts'),
             Rule(SgmlLinkExtractor(allow=('participants/\w+')), callback='parse_profile')]
    start_urls = [
        "http://www.nanowrimo.org/en/forums"
    ]

    def parse_posts(self, response):
        hxs = HtmlXPathSelector(response)

        if 'ft' in response.meta:
            ft = response.meta['ft']
        else:
            ft = ForumThread()
            # TODO Add forum titile
            ft['title'] = hxs.select("//h1/text()").extract()[0]
            ft['url'] = response.url
            ft['responses'] = []

        posts = hxs.select("//div[@class='forum_thread_comment']")
        for p in posts:
            fp = {}
            body_list = p.select(".//div[@class='forum_thread_comment_body']/p/text()").extract()
            body_string = ''
            for body in body_list:
                body_string += body + '\n'

            fp['body'] = body_string
            fp['author'] = p.select(".//a[@class='forum_thread_comment_author']/text()").extract()[0]
            fp['date'] = p.select(".//span[@class='created_time_ago']/@title").extract()[0]
            ft['responses'].append(fp)

        # Get links to next page in thread if there is a next page
        next_page = hxs.select("//a[@class='next_page']/@href").extract()

        # Check if there is another page
        if len(next_page) > 0:
            # There is another page
            next_page_url_relative = next_page[0]
            next_page_url = self.make_url_absolute(response, next_page_url_relative)
            request = Request(next_page_url,
                      callback=self.parse_posts)
            request.meta['ft'] = ft
            return request
        # There is no other page, return forum post items
        else:
            responses = ft['responses']
            first_post, last_post = responses[0], responses[-1]
            get_time_obj = lambda x: datetime.strptime(x, '%B %d, %Y %H:%M')
            time_delta_obj = get_time_obj(last_post['date']) - get_time_obj(first_post['date'])
            time_delta = str(self.days_hours_minutes(time_delta_obj))

            number_of_comments = str(len(responses))

            ft['time_delta'] = time_delta
            ft['number_of_comments'] = number_of_comments

            return ft

    def parse_profile(self, response):
        hxs = HtmlXPathSelector(response)

        profile_box = hxs.select("//div[@id='profile_fact_sheet']")

        p = Profile()
        p['author'] = self.safe_list_get(hxs.select("//h1[@id='profile_name']/text()").extract(), 0).replace('\n','')
        p['age'] = self.safe_list_get(profile_box.select(".//dt[text()='Age:']/following::dd[1]/text()").extract(), 0)
        p['location'] = self.safe_list_get(profile_box.select(".//dt[text()='Location:']/following::dd[1]/text()").extract(), 0)
        p['occupation'] = self.safe_list_get(profile_box.select(".//dt[text()='Occupation:']/following::dd[1]/text()").extract(), 0)

        profile_bling = hxs.select("//div[@id='profile_bling']")
        years = profile_bling.select(".//div[@class='year']")

        participation = ''
        for y in years:
            participation += self.safe_list_get(y.select(".//img/@title").extract(), 0) + ', '

        p['participation'] = participation
        p['url'] = response.url

        return p

