from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

class SpiderUtils(object):

    @staticmethod
    def days_hours_minutes(self, td):
        return td.days, td.seconds//3600, (td.seconds//60)%60

    @staticmethod
    def make_url_absolute(self, response, relative_url):
        base_url = get_base_url(response)
        return urljoin_rfc(base_url, relative_url)

    @staticmethod
    def safe_list_get(self, l, idx, default=''):
        try:
            return l[idx]
        except IndexError:
            return default
