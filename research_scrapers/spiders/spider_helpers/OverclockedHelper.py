from research_scrapers.spiders.spider_helpers.SpiderUtils import safe_list_get, make_url_absolute
from research_scrapers.spiders.spider_helpers.helper_base import HelperBase

from datetime import date, timedelta

class OverclockedHelper(HelperBase):

    def __init__(self):
        HelperBase.__init__(self)
        self.time_string = '%m-%d-%Y,%I:%M%p'

    def get_posts(self):
        return self.hxs.select("//div[@id='posts']/div")

    def load_first_page(self, ft):
        ft['title'] = self.hxs.select("//div[@class='smallfont']/strong/text()").extract()[0]

        p = self.get_posts()[0]
        ft['author']= p.select(".//a[@class='bigusername']/text()").extract()[0]
        
        ft['url'] = self.response.url
        ft['forum_name'] = '/'.join(self.hxs.select("//div[@id='breadcrumb']/a/text()").extract())
        ft['responses'] = []

    def populate_post_data(self, p):
        fp = {}

        comment_body_list = p.select('.//div[@class="forumpost"]/descendant-or-self::*/text()').extract()
        # Check if post is empty
        if len(comment_body_list) < 1:
            return fp

        fp['body'] = ''.join(comment_body_list)
        fp['author'] = p.select(".//a[@class='bigusername']/text()").extract()[0]

        post_date = ''.join(p.select(".//div[@class='normal']/text()").extract()[4].split())

        if  'Today' in post_date or 'Yesterday' in post_date:
            if 'Today' in post_date:
                day  = date.today()
            else:
                day = date.today() - timedelta(1)

            post_date = day.strftime('%m-%d-%Y,') + post_date.split(',')[1]

        fp['date'] = post_date

        return fp

    def prepare_for_processing(self, responses):
        #responses.reverse()
        pass

    def get_next_page(self):
        next_page_url_relative = self.hxs.select("//td[@class='alt2']/following-sibling::td/a/@href").extract()
        next_page_url_relative = safe_list_get(next_page_url_relative, 0)

        if next_page_url_relative:
            return make_url_absolute(self.response, next_page_url_relative)

        return next_page_url_relative
