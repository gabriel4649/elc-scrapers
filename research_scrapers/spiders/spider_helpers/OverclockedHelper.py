from research_scrapers.items import ForumThread, Profile
from datetime import datetime

class OverclockedHelper(object):

    def __init__(self, hxs):
        self.data_key = 'ft'
        self.hxs = hxs

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
        links = self.hxs.select("//a[@rel='next']/@href").extract()

        return len(links) > 0

    def get_next_page_relative(self):
        return self.hxs.select("//a[@rel='next']/@href").extract()[0]

    def time_function(self):
        return lambda x: datetime.strptime(x, '%m-%d-%Y,%I:%M%p')

    def prepare_for_processing(self, responses):
        responses.reverse()
