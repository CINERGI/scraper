'''
# Metadata Scraper v2
# Scrapes the Metadata XML doc and finds URLs in the <gmd:URL> tags
# Run in terminal with scrapy crawl mdspiderv1

import scrapy
from scrapy.selector import Selector
# See http://doc.scrapy.org/en/latest/topics/selectors.html

from metadataScraper.items import MetadatascraperItem
# A class from items.py; copied from tutorial

# Reads URLs to be scraped from a text file
def readLinks():
    filename = raw_input("Enter file name containing URLs to be scraped: ")
    f = open(filename)
    return f.read().splitlines()

class MetadataSpider(scrapy.Spider):
    name = "mdspiderv1"
    allowed_domains = ["cinergi.cloudapp.net"]

    start_urls = readLinks()


    start_urls = [
        "http://cinergi.cloudapp.net/geoportal/rest/document?id={11161776-58F6-4552-A0A2-DB9A6EEAB29D}",
        "http://cinergi.cloudapp.net/geoportal/rest/document?id={11F9E635-15B6-4C70-8563-7081B8814783}",
        "http://cinergi.cloudapp.net/geoportal/rest/document?id={12C37D9E-519D-4478-BE18-63F0C784F7E0}"
    ]
    
    # Change this later to accept input and multiple URLS

    def parse(self, response):
        item = MetadatascraperItem()

        response.selector.remove_namespaces()
        # See http://doc.scrapy.org/en/latest/topics/selectors.html#removing-namespaces
        # xpath had issues because the metadata documents contained namespaces
        # e.g. <gmd:URL> instead of <URL>
        # response.xpath("//gmd:URL") doesn't work; look into later
        # remove_namespaces() takes out gmd: so xpath('//URL') works

        item['title'] = response.xpath('//title/CharacterString/text()').extract()

        item['author'] = response.xpath('//individualName/CharacterString/text()').extract()

        for sel in response.xpath('//linkage'):
            item['link'] = response.xpath('//URL/text()').extract()
            # Finds text in <gmd:URL> tags (the links)
            # Adds them to link in items.py

        print "\n"
        yield item # prints contents of MetadatascraperItem() from items.py
        print "\n"
    '''
