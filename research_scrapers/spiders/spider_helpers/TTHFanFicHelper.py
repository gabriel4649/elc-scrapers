import abc

from SpiderUtils import safe_list_get
from helper_base import HelperBase

class TTHFanFicHelper(HelperBase):

    def __init__(self):
        HelperBase.__init__(self)
        # 'Fri, 02 Dec 11 17:38:12'
        self.time_string = "%a, %d %b %y %H:%M:%S"

    def get_posts(self):
        return self.hxs.select("//td[@class='tth-post tth-post-even' or @class='tth-post tth-post-odd']")

    def load_first_page(self, ft):
        ft['title'] = self.hxs.select("//td[@id='top_subject']/text()").extract()[0]

        p = self.get_posts()[0]

        #ft['author'] = p.select(".//a[starts-with(@title,'View the profile of')]/text()").extract()[0]
        ft['author'] = p.select(".//td[@width='16%']/b/descendant-or-self::*/text()").extract()[0]
        ft['url'] = self.response.url
        ft['forum_name'] = '/'.join(self.hxs.select("//div[@class='nav']/descendant-or-self::*/text()").extract()[0:-3:2])
        ft['responses'] = []

    def populate_post_data(self, p):
        fp = {}

        fp['body'] = ' '.join(p.select(".//div[@class='post']/descendant-or-self::*/text()").extract())
        fp['author'] = p.select(".//td[@width='16%']/b/descendant-or-self::*/text()").extract()[0]
        fp['date'] = p.select(".//div[@class='smalltext']/text()").extract()[-1].replace(u' \xbb', '')[1:-1]

        return fp

    def prepare_for_processing(self, responses):
        pass

    def get_next_page(self):
        next_page_url = safe_list_get(self.hxs.select(".//td[@class='middletext']/b[1]/following-sibling::a/@href").extract(), 0)

        return next_page_url
