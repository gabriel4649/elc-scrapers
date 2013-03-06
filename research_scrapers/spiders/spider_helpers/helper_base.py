import abc

class HelperBase(object):
    __metaclass__ = abc.ABCMeta

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
