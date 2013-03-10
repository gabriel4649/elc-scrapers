import httplib
import urlparse

from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

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

