from research_scrapers.spiders.spider_helpers.helper_base import HelperBase

from research_scrapers.spiders.spider_helpers.SpiderUtils \
    import safe_list_get, make_url_absolute

import code

class EtsyHelper(HelperBase):

    def __init__(self):
        HelperBase.__init__(self)
        # 4:05 pm Apr 25, 2013 EDT
        # 11:48 am May 10, 2013 EDT
        self.time_string = "%I:%M %p %b %d, %Y"

    def get_posts(self):
        replies = self.hxs.select("//div[@id='original-post']/div")
        replies.extend(self.hxs.select("//div[@id='replies']/div[contains(@class, 'post')]"))
        #code.interact(local=locals())
        return replies


    def load_first_page(self, ft):
        ft['title'] = self.hxs.select("//h2[@class='thread-title title ff-medium']/text()").extract()[0]


        ft['author'] =  self.hxs.select("//div[@class='meta-info']/span[@class='author']/a/text()").extract()[0]
        ft['url'] = self.response.url
        ft['forum_name'] = self.hxs.select("//h1/text()").extract()[0]
        ft['responses'] = []

    def populate_post_data(self, p):
        fp = {}

        fp['body'] = ''.join(p.select(".//div[@class='post-body']/descendant-or-self::*/text()").extract())
        fp['author'] = p.select( \
            ".//span[@class='author']/a[contains(@href,'people')]/text()").extract()[0]
        fp['date'] = p.select(".//a[@class='create_date']/text()").extract()[0].strip()[0:-4]

        return fp

    def prepare_for_processing(self, responses):
        pass

    def get_next_page(self):
        next_page_url_relative = safe_list_get( \
            self.hxs.select(".//a[@class='next']/@href").extract(),0)

        if next_page_url_relative:
            return make_url_absolute(self.response, next_page_url_relative)

        return next_page_url_relative
