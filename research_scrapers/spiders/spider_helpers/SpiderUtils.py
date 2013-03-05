import httplib
import urlparse
from datetime import datetime

from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.http.request import Request

def get_server_status_code(url):
    """
    Download just the header of a URL and
    return the server's status code.
    """
    # http://stackoverflow.com/questions/1140661
    host, path = urlparse.urlparse(url)[1:3]    # elems [1] and [2]
    try:
        conn = httplib.HTTPConnection(host)
        conn.request('HEAD', path)
        return conn.getresponse().status
    except StandardError:
        return None

def check_url(url):
    """
    Check if a URL exists without downloading the whole file.
    We only check the URL header.
    """
    # see also http://stackoverflow.com/questions/2924422
    good_codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
    return get_server_status_code(url) in good_codes

def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60

def make_url_absolute(response, relative_url):
    base_url = get_base_url(response)
    return urljoin_rfc(base_url, relative_url)

def safe_list_get(l, idx, default=''):
    try:
        return l[idx]
    except IndexError:
        return default

class ThreadParser(object):
    def __init__(self, helper):
        self.helper = helper
        self.data_key = 'ft'

    def parse_thread(self, response):
        helper = self.helper(response)

        # data_key was ft
        if self.data_key in response.meta:
            data = response.meta[self.data_key]
        else:
            data = helper.new_item()
            helper.load_first_page(data)

        for p in helper.get_posts():
            fp = helper.populate_post_data(p)
            if len(fp) < 1:
                pass
            else:
                data['responses'].append(fp)

        # Check if there is another page
        if helper.next_page():
            # There is another page
            next_page_url = helper.get_next_page()

            # Make recursive call
            request = Request(next_page_url,
                      callback=self.parse_thread)
            request.meta[self.data_key] = data

            return request
        # There is no other page, return forum post items
        else:
            responses = data['responses']
            helper.prepare_for_processing(responses)
            first_post, last_post = responses[0], responses[-1]
            get_time_obj = lambda x: datetime.strptime(x, helper.time_string)
            time_delta_obj = get_time_obj(last_post['date']) - get_time_obj(first_post['date'])
            time_delta = str(days_hours_minutes(time_delta_obj))
            number_of_comments = str(len(responses))
            data['time_delta'] = time_delta
            data['number_of_comments'] = number_of_comments

            return data
