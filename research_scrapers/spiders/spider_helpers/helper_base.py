import abc
from datetime import datetime

from scrapy.http.request import Request
from scrapy.selector import HtmlXPathSelector

from research_scrapers.items import ForumThread
from SpiderUtils import days_hours_minutes

class HelperBase(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.data_key = 'ft'

    @abc.abstractmethod
    def get_posts(self):
        """Get posts divided by divs or other html."""
        return

    @abc.abstractmethod
    def load_first_page(self, ft):
        """Load thread data available in first page."""
        return

    @abc.abstractmethod
    def populate_post_data(self, p):
        """Populate data for a given post."""
        return

    @abc.abstractmethod
    def prepare_for_processing(self):
        """Make any final processing before finalizing."""
        return

    @abc.abstractmethod
    def get_next_page(self):
        """Gets the url for the next page if there is one, otherwise
        return empty string"""
        return

    def parse_thread(self, response):
        """Generic method to parse forum threads, returns a finished
        ForumThread item"""

        self.hxs = HtmlXPathSelector(response)
        self.response = response

        # data_key was ft
        if self.data_key in response.meta:
            data = response.meta[self.data_key]
        else:
            data = ForumThread()
            self.load_first_page(data)

        for p in self.get_posts():
            fp = self.populate_post_data(p)
            if len(fp) < 1:
                pass
            else:
                data['responses'].append(fp)

        # Check if there is another page
        next_page_url = self.get_next_page()
        if next_page_url:
            # There is another page

            # Make recursive call
            request = Request(next_page_url,
                      callback=self.parse_thread)
            request.meta[self.data_key] = data

            print
            print "RETURNING REQUEST!!!"
            print
            print next_page_url
            print
            print "RETURNING REQUEST!!!"
            print

            return request
        # There is no other page, return forum post items
        else:
            responses = data['responses']
            self.prepare_for_processing(responses)
            first_post, last_post = responses[0], responses[-1]
            get_time_obj = lambda x: datetime.strptime(x, self.time_string)
            time_delta_obj = get_time_obj(last_post['date']) - get_time_obj(first_post['date'])
            time_delta = str(days_hours_minutes(time_delta_obj))
            data['time_delta'] = time_delta
            data['number_of_comments'] = str(len(responses))

            return data
