from scrapy.selector import HtmlXPathSelector
from SpiderUtils import safe_list_get
from helper_base import HelperBase

class EbaumsworldHelper(HelperBase):

    def __init__(self):
        HelperBase.__init__(self)
        self.time_string = '%Y-%m-%dT%H:%M:%S+00:00'

    def get_posts(self):
        return self.hxs.select("//div[@id='ips_Posts']/div")

    def load_first_page(self, ft):
        ft['title'] = self.hxs.select("//h1[@class='ipsType_pagetitle']/text()").extract()[0]
        ft['author'] = self.hxs.select("//span[@itemprop='creator']/text()").extract()[0]
        ft['forum_name'] = ' '.join(self.hxs.select("//ol[@class='breadcrumb top ipsList_inline left']/li/a/span/text()").extract())
        ft['url'] = self.response.url
        ft['responses'] = []

    def populate_post_data(self, p):
        fp = {}

        comment_body_list = p.select(".//div[@class='post entry-content ']/descendant-or-self::*/text()").extract()

        comment_body = ''.join(comment_body_list)

        fp['body'] = comment_body
        #fp['author'] = p.select(".//span[@class='author vcard']/text()").extract()[0]
        fp['author'] = p.select(".//span[@itemprop='name']/text()").extract()[0]
        fp['date'] = p.select(".//abbr[@class='published']/@title").extract()[0]

        return fp

    def prepare_for_processing(self, responses):
        pass

    def get_next_page(self):
        return safe_list_get(self.hxs.select('//a[@rel="next"]/@href').extract(), 0)
