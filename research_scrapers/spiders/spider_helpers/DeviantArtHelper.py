
from research_scrapers.spiders.spider_helpers.SpiderUtils import safe_list_get, make_url_absolute
from research_scrapers.spiders.spider_helpers.helper_base import HelperBase

class DeviantArtHelper(HelperBase):

    def __init__(self):
        HelperBase.__init__(self)
        # 'Mar 21, 2013, 6:42:57 PM'
        self.time_string = '%b %d, %Y, %I:%M:%S %p'

    def get_posts(self):
        return self.hxs.select("//div[@class='ctext ch']")

    def load_first_page(self, ft):
        # TODO: Not always catching the title
        ft['title'] =  safe_list_get(self.hxs.select("//div[@class='forum-header']/h1/text()").extract(),0)

        p = self.get_posts()[0]
        ft['author'] = p.select(".//a[@class='u']/text()").extract()[0]

        ft['url'] = self.response.url
        ft['forum_name'] = '/'.join(self.hxs.select("//div[@class='catpath']/a/text()").extract())
        ft['responses'] = []

    def populate_post_data(self, p):
        fp = {}
        fp['body'] =  ''.join(p.select(".//div[@class='text text-ii']/descendant-or-self::*/text()").extract())
        fp['author'] = p.select(".//a[@class='u']/text()").extract()[0]
        date = p.select(".//span[@class='cc-time']/a/@title").extract()[0]

        if 'ago' in date:
            time = date.split('at ')[1][:-1]
            date = p.select(".//span[@class='cc-time']/a/text()").extract()[0] + ', ' + time

        fp['date'] = date

        return fp

    def prepare_for_processing(self, responses):
        pass

    def get_next_page(self):
        next_page_url_relative = self.hxs.select("//li[@class='next']/a[@class='away']/@href").extract()
        next_page_url_relative = safe_list_get(next_page_url_relative, 0)

        if next_page_url_relative:
            return make_url_absolute(self.response, next_page_url_relative)

        return next_page_url_relative
