# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class ForumPost(Item):
    time_delta = Field()
    number_of_comments = Field()
    body = Field()
    date = Field()
    author = Field()
    url = Field()

class Profile(Item):
    author = Field()
    age = Field()
    location = Field()
    occupation = Field()
    participation = Field()
    url = Field()
