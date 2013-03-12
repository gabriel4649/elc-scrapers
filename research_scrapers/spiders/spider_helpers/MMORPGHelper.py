import abc

from SpiderUtils import safe_list_get, make_url_absolute
from helper_base import HelperBase

class MMORPGHelper(HelperBase):

    def __init__(self):
        HelperBase.__init__(self)
        # '11-02-2006, 12:19 PM'
        self.time_string = "%m-%d-%Y, %I:%M %p"

    def get_posts(self):
        return self.hxs.select("//div[@id='posts']/div/div/div/div")

    def load_first_page(self, ft):
        ft['title'] = self.hxs.select("//td[@class='navbar']/strong/text()").extract()[0]

        p = self.get_posts()[0]

        ft['author'] = p.select(".//a[@style='text-decoration:none; color:white;']/text()").extract()[0]
        ft['url'] = self.response.url
        ft['forum_name'] = '/'.join(self.hxs.select("//span[@class='navbar']/a/text()").extract())
        ft['responses'] = []

    def populate_post_data(self, p):
        fp = {}

        fp['body'] = ' '.join(p.select(".//div[starts-with(@id,'post_message_')]/descendant-or-self::*/text()").extract())
        fp['author'] = p.select(".//a[@style='text-decoration:none; color:white;']/text()").extract()[0]
        fp['date'] = p.select(".//td[@style='font-weight:normal']/text()").extract()[2][5:-10]

        return fp

    def prepare_for_processing(self, responses):
        pass

    def get_next_page(self):
        nav = self.hxs.select("//div[@class='pagenav']/table")
        next_page_url_relative = safe_list_get(nav.select(".//td[@class='alt2']/following-sibling::td/a/@href").extract(), 0)

        if next_page_url_relative:
            return make_url_absolute(self.response, next_page_url_relative)

        return next_page_url_relative
