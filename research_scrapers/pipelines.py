# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import os, json

from research_scrapers.items import ForumThread, Profile

class NanoWrimoPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        f = 'data/' + spider.__class__.__name__ + '/' + item['url'].split('/')[-1] + item.__class__.__name__ + '.txt'
        d = os.path.dirname(f)
        if not os.path.exists(d):
            os.makedirs(d)

        if type(item) is Profile:
            item_text = 'User Profile \n\n'
            item_text += "author: " + item.get("author", "") + '\n'
            item_text += "age: " + item.get("age", "") + '\n'
            item_text += "location: " + item.get("location", "") + '\n'
            item_text += "occupation: " + item.get("occupation", "") + '\n'
            item_text += "participation: \n" + item.get("participation", "") + '\n'
            item_text += "url: \n" + item.get("url", "")

        elif type(item) is ForumThread:
            item_text = 'Forum Thread \n\n'
            item_text += "title: " + item.get("title", "") + '\n'
            item_text += "author: " + item.get("author", "") + '\n'
            item_text += "time_delta: " + item.get("time_delta", "") + '\n'
            item_text += "number_of_comments: " + item.get("number_of_comments", "") + '\n'
            item_text += "views: " + item.get("views", "") + '\n'
            item_text += "url: \n" + item.get("url", "") + '\n'
            responses = item.get("responses", "")
            responses_string = ''
            for post in responses:
                responses_string += '-----------------------------------\n'
                responses_string += "author: " + post.get('author', '') + '\n'
                responses_string += "date: " + post.get('date', '') + '\n'
                responses_string += "body: " + post.get('body', '') + '\n'
                responses_string += '\n-----------------------------------\n'

            item_text += "responses: \n"
            item_text += responses_string

        item_file = open(f, 'wb')
        item_file.write(item_text.encode('utf8'))

        return item
