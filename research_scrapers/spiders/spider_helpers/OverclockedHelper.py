from research_scrapers.items import ForumThread, Profile
from SpiderUtils import make_url_absolute

class OverclockedHelper(object):

    def __init__(self, hxs):
        self.data_key = 'ft'
        self.hxs = hsx

    def get_posts(self):
        return hxs.select("//div[@id='posts']/div")

    def load_first_page(self, ft):
        ft['title'] = self.hxs.select("//div[@class='smallfont']/strong/text()").extract()[0]
        ft['url'] = self.hxs.response.url
        ft['responses'] = []

    def populate_post_data(self, p):
        fp = {}

        body = ""

        #Check if quoting
        quote = p.select(".//td[@class='alt2']/div[@style='font-style:italic']/text()").extract()

        if quote:
            body += "Quote: \n" + quote[0]
            author = p.select(".//td[@class='alt2']/div/strong/text()").extract()[0]
            body += "By: " + author

        body += "\n Comment: \n" + p.select(".//div[@class='forumpost']/text()").extract()[-1]

        fp['body'] = body
        fp['author'] = p.select(".//a[@class='bigusername']/text()").extract()[0]
        fp['date'] = ''.join(p.select(".//div[@class='normal']/text()").extract()[4].split())

        return fp

    def new_item(self):
        return ForumThread()

    def next_page(self):
        links = self.hxs.select("//a[@rel='next']/@href").extract()

        return len(links) > 0

    def get_next_page(self):
        return make_url_absolute(self.hxs.select("//a[@rel='next']/@href").extract()[0])

    def populate_meta_data(self):
        return lambda x: datetime.strptime(x, '%m-%d-%Y,%I:%M%p')