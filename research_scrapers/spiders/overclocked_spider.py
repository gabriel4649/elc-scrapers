from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from research_scrapers.items import ForumThread, Profile

#from overcloked_module.py import Overclocked

class OverclockedSpider(CrawlSpider):
    name = 'overcloked'
    allowed_domains = ['http://ocremix.org']
    start_urls = ['http://ocremix.org/forums/']

    rules = (
        Rule(SgmlLinkExtractor(allow='forumdisplay.php?f=[0-9]+')),
        Rule(SgmlLinkExtractor(allow='forumdisplay.php?f=[0-9]+&order=desc&page=[0-9]+')),
        Rule(SgmlLinkExtractor(allow='showthread.php?t=[0-9]+'), callback='parse_thread', follow=True)
      )

    def parse_thread(self, response):
        overcloked = Overclocked(HtmlXPathSelector(response))

        # data_key was ft
        if overclocked.data_key in response.meta:
            data = response.meta[overclocked.data_key]
        else:
            data = overclocked.get_newitem()
            overclocked.load_first_page(data)

        for p in get_posts:
            fp = {}
            ft['responses'].append(overclocked.populate_post_data(p))

        # Get links to next page in thread if there is a next page
        next_page = overclocked.links_to_next_page()

        # Check if there is another page
        if overclocked.next_page():
            # There is another page
            next_page_url = overclocked.get_next_page()
            request = Request(next_page_url,
                      callback=self.parse_posts)
            request.meta[overclocked.data_key] = data
            return request
        # There is no other page, return forum post items
        else:
            overclocked.populate_last_page(data)

            return data
