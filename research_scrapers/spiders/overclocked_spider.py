from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule


from spider_helpers import OverclockedHelper

class OverclockedSpider(CrawlSpider):
    name = 'overclocked'
    allowed_domains = ['http://ocremix.org']
    start_urls = ['http://ocremix.org/forums/']

    rules = (
        Rule(SgmlLinkExtractor(allow='forumdisplay.php?f=\d+')),
        Rule(SgmlLinkExtractor(allow='forumdisplay.php?f=\d+&order=desc&page=\d+')),
        Rule(SgmlLinkExtractor(allow='showthread.php?t=\d+'), callback='parse_thread', follow=True)
      )

    def parse_thread(self, response):
        overcloked = OverclockedHelper(HtmlXPathSelector(response))

        # data_key was ft
        if overclocked.data_key in response.meta:
            data = response.meta[overclocked.data_key]
        else:
            data = overclocked.new_item()
            overclocked.load_first_page(data)

        for p in get_posts:
            data['responses'].append(overclocked.populate_post_data(p))

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
            responses = data['responses']
            first_post, last_post = responses[0], responses[-1]
            get_time_obj = overcloked.time_function()
            time_delta_obj = get_time_obj(last_post['date']) - get_time_obj(first_post['date'])
            time_delta = str(self.days_hours_minutes(time_delta_obj))
            number_of_comments = str(len(responses))
            data['time_delta'] = time_delta
            data['number_of_comments'] = number_of_comments


            return data
