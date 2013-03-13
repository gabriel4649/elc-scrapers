import abc

from SpiderUtils import safe_list_get, make_url_absolute
from helper_base import HelperBase

class FanArtHelper(HelperBase):

    def __init__(self):
        HelperBase.__init__(self)
        # 'Dec 14, 2008 12:04 am'
        self.time_string = "%b %d, %Y %I:%M %p"

    def get_posts(self):
        body = self.hxs.select("//table[@class='forumline']")
        return body.select(".//td[@class='row1']/table/../..")

    def load_first_page(self, ft):
        ft['title'] = self.hxs.select("//a[@class='maintitle']/text()").extract()[0]

        p = self.get_posts()[0]

        ft['author'] = p.select(".//span[@class='name']/b/a/text()").extract()[0]
        ft['url'] = self.response.url
        forum_name = hxs.select("//td[@valign='middle'']/span[@class='nav']/a[@class='nav']/descendant-or-self::*/text()").extract()
        forum_name = ' '.join(forum_name)
        forum_name = forum_name.split("Back to top")[0]
        ft['forum_name'] = forum_name
        ft['responses'] = []

    def populate_post_data(self, p):
        fp = {}

        fp['body'] = ' '.join()
        fp['author'] = p.select(".//span[@class='name']/b/a/text()").extract()[0]
        fp['date'] = p.select(".//td[@width='100%']/span[@class='postdetails']/text()").extract()[0][12:]

        return fp

    def prepare_for_processing(self, responses):
        pass

    def get_next_page(self):
        next_page_url_relative = self.hxs.select("//span[@class='gensmall']/b/b/following-sibling::a/@href").extract()[0]
        next_page_url_relative = safe_list_get(next_page_url_relative, 0)

        if next_page_url_relative:
            return make_url_absolute(self.response, next_page_url_relative)

        return next_page_url_relative
