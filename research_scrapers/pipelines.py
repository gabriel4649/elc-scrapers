# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import os, json

class NanoWrimoPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        f = 'data/' + spider.__class__.__name__ + '/' + item['url'].split('/')[-1] + item.__class__.__name__ + '.txt'
        d = os.path.dirname(f)
        if not os.path.exists(d):
            os.makedirs(d)
        item_file = open(f, 'wb')

        item_text = json.dumps(dict(item), indent=4)
        item_text.replace('{', '')
        item_text.replace('}', '')
        item_text.replace('[', '')
        item_text.replace(']', '')

        item_file.write(item_text)

        return item
