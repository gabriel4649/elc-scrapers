import abc

from SpiderUtils import safe_list_get, make_url_absolute
from helper_base import HelperBase

class Remix64Helper(HelperBase):

    def __init__(self):
        HelperBase.__init__(self)
        self.time_string = '%d/%m/%Y - %H:%M'

    def get_posts(self):
        return self.hxs.select("//div[@class='postbody']")

    def load_first_page(self, ft):
        ft['title'] = self.hxs.select("//div[@id='page-body']/h2/a/text()").extract()[0]

        p = self.get_posts()[0]

        ft['author'] = p.select(".//p[@class='author']/strong/descendant-or-self::*/text()").extract()[0]
        ft['url'] = self.response.url
        ft['responses'] = []

    def populate_post_data(self, p):
        fp = {}

        comment_body_list = p.select(".//div[@class='content']/descendant-or-self::*/text()").extract()

        comment_body = ""
        for part in comment_body_list:
            comment_body += ''.join(part)

        fp['body'] = comment_body
        fp['author'] = p.select(".//p[@class='author']/strong/descendant-or-self::*/text()").extract()[0]
        fp['date'] = p.select(".//span[@class='hotdate']/text()").extract()[0]

        return fp

    def prepare_for_processing(self, responses):
        pass

    def get_next_page(self):
        next_page_url_relative = safe_list_get(self.hxs.select("//a[@class='right-box right']/@href").extract(), 0)

        if next_page_url_relative:
            return make_url_absolute(self.response, next_page_url_relative)

        return next_page_url_relative
