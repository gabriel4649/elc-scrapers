from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request

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

    def parse_thread(self, response):
        helper = self.helper(HtmlXPathSelector(response))

        # data_key was ft
        if helper.data_key in response.meta:
            data = response.meta[helper.data_key]
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
            next_page_url_relative = helper.get_next_page_relative()

            next_page_url = make_url_absolute(response, next_page_url_relative)

            # Make recursive call
            request = Request(next_page_url,
                      callback=self.parse_thread)
            request.meta[helper.data_key] = data
            return request
        # There is no other page, return forum post items
        else:
            responses = data['responses']
            first_post, last_post = helper.get_first_and_last_posts(responses)
            get_time_obj = helper.time_function()
            time_delta_obj = get_time_obj(last_post['date']) - get_time_obj(first_post['date'])
            time_delta = str(days_hours_minutes(time_delta_obj))
            number_of_comments = str(len(responses))
            data['time_delta'] = time_delta
            data['number_of_comments'] = number_of_comments

            return data
