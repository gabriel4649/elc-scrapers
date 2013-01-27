# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

class NanoWrimoPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):

        return item
