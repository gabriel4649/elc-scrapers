from scrapy.selector import HtmlXPathSelector
from research_scrapers.items import ForumThread, Profile
from SpiderUtils import check_url


class HPFanFicHelper(object):

    def __init__(self, response):
        self.time_string = '%Y-%m-%dT%H:%M:%S+00:00'
        self.hxs = HtmlXPathSelector(response)
        self.response = response

    def get_posts(self):
        return self.hxs.select("//div[@id='ips_Posts']/div")

    def load_first_page(self, ft):
        ft['title'] = self.hxs.select("//h1[@class='ipsType_pagetitle']/text()").extract()[0]
        ft['author'] = self.hxs.select("//span[@itemprop='creator']/text()").extract()[0]
        ft['url'] = self.hxs.response.url
        ft['responses'] = []

    def populate_post_data(self, p):
        fp = {}

        comment_body_list = p.select(".//div[@class='post entry-content ']/descendant-or-self::*/text()").extract()

        comment_body = "\n Comment: \n"
        for part in comment_body_list:
            comment_body += ''.join(part)

        fp['body'] = comment_body
        fp['author'] = p.select(".//span[@class='author vcard']/text()").extract()[0]
        fp['date'] = p.select(".//abbr[@class='published']/@title").extract()[0]

        return fp

    def new_item(self):
        return ForumThread()

    def next_page(self):
        next_page_urls = self.hxs.select('//a[@rel="next"]/@href').extract()

        if len(next_page_urls) > 0:
            return True

        return False

    def prepare_for_processing(self, responses):
        pass

    def get_next_page(self):
        self.hxs.select('//a[@rel="next"]/@href').extract()[0]
