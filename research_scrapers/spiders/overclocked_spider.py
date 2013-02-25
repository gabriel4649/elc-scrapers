from scrapy.contrib.spiders.init import InitSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.http import FormRequest
from scrapy.http.request import Request

from spider_helpers.SpiderUtils import make_url_absolute, days_hours_minutes, ThreadParser
from spider_helpers.OverclockedHelper import OverclockedHelper

class OverclockedSpider(InitSpider, ThreadParser):
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

    def __init__(self):
        InitSpider.__init__(self)
        ThreadParser.__init__(self, OverclockedHelper)

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

