from research_scrapers.spiders.spider_helpers.helper_base import HelperBase

class ExampleHelper(HelperBase):

    def __init__(self):
        HelperBase.__init__(self)
        self.time_string = ""

    def get_posts(self):
        pass

    def load_first_page(self, ft):
        ft['title'] = ""
        ft['author'] = ""
        ft['url'] = ""
        ft['forum_name'] = ""
        ft['responses'] = ""

    def populate_post_data(self, p):
        fp = {}

        fp['body'] = ""
        fp['author'] = ""
        fp['date'] = ""

        return fp

    def prepare_for_processing(self, responses):
        pass

    def get_next_page(self):
        pass
