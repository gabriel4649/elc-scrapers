from research_scrapers.spiders.spider_helpers.SpiderUtils import safe_list_get, make_url_absolute
from research_scrapers.spiders.spider_helpers.helper_base import HelperBase

class FanArtHelper(HelperBase):

    def __init__(self):
        HelperBase.__init__(self)
        # 'Dec 14, 2008 12:04 am'
        self.time_string = "%b %d, %Y %I:%M %p"

    def get_posts(self):
        body = self.hxs.select("//table[@class='forumline']")
        posts = body.select(".//tr[td[@class='row1' or @class='row2']]")
        #posts = body.select(".//td[@class='row1']/table/../..")
        return posts[::2]

    def load_first_page(self, ft):
        ft['title'] = self.hxs.select("//a[@class='maintitle']/text()").extract()[0]

        p = self.get_posts()[0]

        ft['author'] = p.select("..//a/text()").extract()[0]
        ft['url'] = self.response.url
        forum_name = self.hxs.select("//td[@valign='middle']/span[@class='nav']/a[@class='nav']/descendant-or-self::*/text()").extract()
        forum_name = ' '.join(forum_name)
        forum_name = forum_name.split("Back to top")[0]
        ft['forum_name'] = forum_name
        ft['responses'] = []

    def populate_post_data(self, p):
        fp = {}

        fp['body'] = ' '.join(p.select(".//tr/td[@colspan='2']/descendant-or-self::*/text()").extract())
        fp['author'] = p.select(".//a/text()").extract()[0]

        possible_dates = p.select(".//span[@class='postdetails']/text()").extract()
        for pd in possible_dates:
            if 'Posted' in pd:
                date = pd

        fp['date'] = date[12:]

        return fp

    def prepare_for_processing(self, responses):
        pass

    def get_next_page(self):
        next_page_url_relative = self.hxs.select("//span[@class='gensmall']/b/b/following-sibling::a/@href").extract()
        next_page_url_relative = safe_list_get(next_page_url_relative, 0)

        if next_page_url_relative:
            return make_url_absolute(self.response, next_page_url_relative)

        return next_page_url_relative
