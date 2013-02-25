from scrapy.contrib.spiders.init import InitSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.http import FormRequest
from scrapy.http.request import Request

from spider_helpers.SpiderUtils import make_url_absolute, days_hours_minutes
from spider_helpers.OverclockedHelper import OverclockedHelper

class OverclockedSpider(InitSpider):
    name = 'overclocked'
    allowed_domains = ['ocremix.org']
    login_page = 'http://ocremix.org/forums/index.php'
    start_urls = ['http://ocremix.org/forums/search.php']


    rules = (
        Rule(SgmlLinkExtractor(allow='forums/search.php?searchid=\d+')),
        Rule(SgmlLinkExtractor(allow='forums/search.php?searchid=\d+&pp=\d+&page=\d+')),
        Rule(SgmlLinkExtractor(allow='forums/showthread.php\?t=\d+'), callback='parse_thread'),
        Rule(SgmlLinkExtractor(allow='forums/forumdisplay.php\?f=\d+&order=desc&page=\d+')),
        Rule(SgmlLinkExtractor(allow='forums/forumdisplay.php\?f=\d+')),
      )

    def init_request(self):
        """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        """Generate a login request."""
        return FormRequest.from_response(response,
                clickdata={'value':'Log in'},
                formdata={'vb_login_username': 'cwarrior', 'vb_login_password':  'BoeN\NHY'},
                callback=self.check_login_response)

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        # check login succeed before going on
        if "You have entered an invalid username or password." in response.body:
            self.log("Login failed", level=log.ERROR)
            return
        else:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin..
            self.initialized()
            return Request(url="http://ocremix.org/forums/search.php",
                      callback=self.search_keywords)

    def search_keywords(self, response):
        keywords = ('copyright', 'legal', 'illegal', 'permission', 'trademark',
                    'stealing', 'steal', 'stole', 'license', 'rights', 'attorney',
                    'infringement', 'copy', 'copying', 'plagiarism')

        for keyword in keywords:
            yield FormRequest.from_response(response,
                    clickdata={'name':'dosearch'},
                    formdata={'query': keyword})

    def parse_thread(self, response):
        overclocked = OverclockedHelper(HtmlXPathSelector(response))

        # data_key was ft
        if overclocked.data_key in response.meta:
            data = response.meta[overclocked.data_key]
        else:
            data = overclocked.new_item()
            overclocked.load_first_page(data)

        for p in overclocked.get_posts():
            fp = overclocked.populate_post_data(p)
            if len(fp) < 1:
                pass
            else:
                data['responses'].append(fp)

        # Check if there is another page
        if overclocked.next_page():
            # There is another page
            next_page_url_relative = overclocked.get_next_page_relative()

            next_page_url = make_url_absolute(response, next_page_url_relative)

            # Make recursive call
            request = Request(next_page_url,
                      callback=self.parse_thread)
            request.meta[overclocked.data_key] = data
            return request
        # There is no other page, return forum post items
        else:
            responses = data['responses']
            first_post, last_post = overclocked.get_first_and_last_posts(responses)
            get_time_obj = overclocked.time_function()
            time_delta_obj = get_time_obj(last_post['date']) - get_time_obj(first_post['date'])
            time_delta = str(days_hours_minutes(time_delta_obj))
            number_of_comments = str(len(responses))
            data['time_delta'] = time_delta
            data['number_of_comments'] = number_of_comments

            return data
