#from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

from research_scrapers.items import ForumThread, Profile

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import time
import urllib2
import re
from random import randint
from string import replace


class YouTubeSpider(BaseSpider):
    name = "youtube"
    start_urls = ["http://productforums.google.com/forum/#%21categories/youtube"]

    # Rule(SgmlLinkExtractor(
    #     allow=('forum/#%21categories/youtube', ),
    #     deny=('forum/#%21category-topic/youtube/\d+', )), callback='parse_page'),
    # )

    def __init__(self):
        BaseSpider.__init__(self)
        self.verificationErrors = []
        response = urllib2.urlopen("http://code.jquery.com/jquery.min.js")
        jquery = response.read()
        self.jquery = jquery.decode('latin_1')
        self.browser = webdriver.Firefox() # Get local session of firefox


    def __del__(self):
        self.browser.close()
        print self.verificationErrors
        BaseSpider.__del__(self)

    def parse(self, response):
        self.load_page_with_jquery('http://productforums.google.com/forum/#%21categories/youtube')

        for i in range(5):
            self.browser.execute_script('$("div").animate({ scrollTop: 100000 }, "fast");')
            time.sleep(randint(1,4))

        try:
            divs = self.browser.find_elements_by_xpath("//div[@class='GAK2G4EDKL']")
            print 'divs: ' + str(len(divs))
            for div in divs:
                ft = ForumThread()
                a = div.find_element_by_class_name('GAK2G4EDOI')
                # Make it load all posts at once
                link = a.get_attribute('href') #+ '[1-9999-true]'
                # Enconde the !
                link = replace(link, '!', '%21')
                ft['url'] = link
                ft['title'] = a.text
                ft['author'] = div.find_element_by_class_name("GAK2G4EDEL").text
                # details: [number of posts, number of views, last updated]
                details = div.find_elements_by_class_name('GAK2G4EDCM')
                # n posts, get the n
                ft['number_of_comments'] = details[0].text.split(' ')[0]
                # n views, get the n
                ft['views'] = details[1].text.split(' ')[0]
                ft['responses'] = []
                request = Request(link, callback=self.parse_thread)
                request.meta['ft'] = ft
                yield request

        except NoSuchElementException:
            assert 0, "can't find seleniumhq"

    def parse_thread(self, response):
        browser = webdriver.Firefox()
        browser.get(response.url)

        divs = browser.find_elements_by_class_name('GAK2G4EDK2')
        ft = response.meta['ft']
        for div in divs:
            fp = {}
            fp['body'] = div.find_element_by_class_name('GAK2G4EDIAD').text
            fp['author'] = div.find_element_by_class_name('GAK2G4EDHFB').text
            fp['date'] = div.find_element_by_class_name('GAK2G4EDO3').text
            ft['responses'].append(fp)

        browser.close()
        return ft

    def load_page_with_jquery(self, url):
        self.browser.get(url) # Load page
        self.browser.execute_script(self.jquery) # Load jquery
        time.sleep(3) # Make sure we had enough time to load everything
