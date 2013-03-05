from scrapy.selector import HtmlXPathSelector
from research_scrapers.items import ForumThread, Profile
from SpiderUtils import check_url
from datetime import datetime

class OverclockedHelper(object):

    def __init__(self, response):
        self.data_key = 'ft'
        self.hxs = HtmlXPathSelector(response)
        self.response = response

    def get_posts(self):
        return self.hxs.select("//div[@id='posts']/div")

    def load_first_page(self, ft):
        ft['title'] = self.hxs.select("//div[@class='smallfont']/strong/text()").extract()[0]
        ft['url'] = self.hxs.response.url
        ft['responses'] = []

    def populate_post_data(self, p):
        fp = {}

        comment_body_list =  p.select('.//div[@class="forumpost"]/descendant-or-self::*/text()').extract()

        # Check if post is empty
        if len(comment_body_list) < 1:
            return fp

        comment_body = "\n Comment: \n"
        for part in comment_body_list:
            comment_body += ''.join(part)

        fp['body'] = comment_body
        fp['author'] = p.select(".//a[@class='bigusername']/text()").extract()[0]
        date_list = p.select(".//div[@class='normal']/text()").extract()[5].split()
        date = ''.join(date_list)
        fp['date'] = date

        return fp

    def new_item(self):
        return ForumThread()

    def next_page(self):
        prev_link = self.hxs.select('//a[@rel="next"]/@href').extract()

        if len(prev_link) > 0:
            return True

        return False

    def time_function(self):
        return lambda x: datetime.strptime(x, '%m-%d-%Y,%I:%M%p')

    def prepare_for_processing(self, responses):
        responses.reverse()

    def get_next_page(self):
        url, page_num = self.base_url_and_page_number(self.response.url)
        next_page = url + '&page=' + str(page_num + 1)

        return next_page

    def base_url_and_page_number(self, url):
        split = url.split('&')

        # Check if we are on the first page
        if len(split) < 2:
            return url, 1

        base_url, parameter = split
        page_num = int(parameter.split('=')[1])

        return base_url, page_num
