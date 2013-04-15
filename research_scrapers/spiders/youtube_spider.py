from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from research_scrapers.items import ForumThread

from selenium import webdriver
import time
import urllib2
from random import randint
from code import interact

class YouTubeSpider(CrawlSpider):
    name = "youtube"
    start_urls = ["http://productforums.google.com/forum/#%21categories/youtube"]

    rules = [Rule(SgmlLinkExtractor(
    allow=('youtube')), callback='parse_page')]

    def __init__(self):
        CrawlSpider.__init__(self)
        self.verificationErrors = []
        response = urllib2.urlopen("http://code.jquery.com/jquery.min.js")
        jquery = response.read()
        self.jquery = jquery.decode('latin_1')
        self.browser = webdriver.Firefox() # Get local session of firefox

    def __del__(self):
        self.browser.close()
        print self.verificationErrors
        CrawlSpider.__del__(self)

    def parse_page(self, response):
        self.load_page_with_jquery('http://productforums.google.com/forum/#%21categories/youtube')

        self.scroll_page(self.browser,1)

        divs = self.browser.find_elements_by_xpath('//div[starts-with(@id,"topic_row_")]')
        #divs = self.browser.find_elements_by_xpath('//div[@role="listitem"]')
        for div in divs:
            ft = ForumThread()

            a = div.find_element_by_xpath(".//a")
            link = a.get_attribute('href')
            # Enconde the !
            link.replace('!', '%21')
            ft['url'] = link
            ft['title'] = a.text
            print "TITLE"
            print a.text
            print "LINK"
            print link
            ft['author'] = div.find_element_by_xpath(".//span[starts-with(text(),'By ')]").text[3:]

            # n posts, get the n
            ft['number_of_comments'] = div.find_element_by_xpath(".//span[contains(text(),'post')]").text
            # n views, get the n
            ft['views'] = div.find_element_by_xpath(".//span[contains(text(),'view')]").text

            ft['responses'] = []
            request = Request(link, dont_filter=True, callback=self.parse_thread)
            request.meta['ft'] = ft

            yield request

    def parse_thread(self, response):
        ft = response.meta['ft']
        browser = webdriver.Firefox()
        browser.get(ft['url'])
        browser.execute_script(self.jquery) # Load jquery
        time.sleep(4) # wait for page to load

        self.scroll_page(browser,1)


        divs = browser.find_elements_by_xpath('//div[@id="tm-tl"]/div')

        for div in divs:
            fp = {}

            try:
                author = div.find_element_by_xpath(".//span[@class='_username']/span").text
            except:
                continue

            fp['author'] = author
            #interact(local=locals())
            fp['body'] = div.find_element_by_xpath(".//div[@style='overflow: hidden']/descendant-or-self::*").text
            fp['date'] =  div.find_element_by_xpath(".//td[@valign='top' and @align='right']/div[2]").text
            ft['responses'].append(fp)

        browser.close()
        return ft

    def load_page_with_jquery(self, url):
        self.browser.get(url) # Load page
        self.browser.execute_script(self.jquery) # Load jquery
        time.sleep(3) # Make sure we had enough time to load everything

    def scroll_page(self, browser, scrolls):
        for i in range(scrolls):
            browser.execute_script('$("div").animate({ scrollTop: 100000 }, "fast");')
            time.sleep(randint(1,4))
