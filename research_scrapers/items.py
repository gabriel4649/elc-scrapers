# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class ForumThread(Item):
    title = Field()
    time_delta = Field()
    number_of_comments = Field()
    responses = Field()
    url = Field()

class Profile(Item):
    author = Field()
    age = Field()
    location = Field()
    occupation = Field()
    participation = Field()
    url = Field()