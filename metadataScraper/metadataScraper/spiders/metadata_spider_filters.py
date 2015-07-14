# Metadata Scraper v3
# Scrapes metadata URLs from http://hydro10.sdsc.edu/metadata/ScienceBase_WAF_dump/
# Passes URLs to metadata scraper to get links under <gmd:URL> tag, title, author
# Run in terminal with scrapy crawl metadata
# SAMPLE OUTPUT can be found in s3output.json
# Date: June 29 2015
# Quirk: the TO PARENT DIRECTORY url also gets scraped from hydro10 resulting in
# an empty entry in the output json {"title": [], "author": []} because it
# doesn't link to an xml document but rather goes up a level in the directory

import scrapy
from scrapy import signals
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import json
import time
import logging
# See http://doc.scrapy.org/en/latest/topics/selectors.html

from metadataScraper.items import MetadatascraperItem
# A class from items.py; copied from tutorial

# timestamp = time.strftime("%Y-%m-%d_%H%M%S")
# filename = "SPIDER_METADATA_FILTERED.json"
# filename = "metadata_" + timestamp + ".json"
# f = open(filename, 'w')

# logger = logging.getLogger(__name__)

class MetadataSpider(scrapy.Spider):
    name = "sciencebase-filtered"
    allowed_domains = ["hydro10.sdsc.edu"]
    start_urls = [
        "http://hydro10.sdsc.edu/metadata/ScienceBase_WAF_dump/"
    ]

    '''
    def from_crawler(self, crawler):
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
    '''

    def parse(self, response):
        # Finds all links to metadata XMLs on hydro10 directory page

        filename = "SPIDER_METADATA_FILTERED.json"
        # filename = "metadata_" + timestamp + ".json"
        f = open(filename, 'w')

        for href in response.xpath("//a/@href"):
            url = response.urljoin(href.extract())
            # Joins href's output (/metadata/Scien.../[id].xml) to
            # hydro10.sdsc.edu to make a valid link

            item = yield scrapy.Request(url, callback=self.parse_metadata)
            logging.info(item)

            json.dump(dict(item), f)
            f.write("\n")
            # Passes links to parse_metadata() function

        f.close()


    def parse_metadata(self, response):
        # Finds all links under <gmd:URL> XML tag in metadata documents
        # in addition to author and title

        item = MetadatascraperItem()
        response.selector.remove_namespaces()
        # See http://doc.scrapy.org/en/latest/topics/selectors.html#removing-namespaces
        # xpath had issues because the metadata documents contained namespaces
        # e.g. <gmd:URL> instead of <URL>
        # response.xpath("//gmd:URL") doesn't work; look into later
        # remove_namespaces() takes out gmd: so xpath('//URL') works
        if response.xpath('//abstract/CharacterString/text()').extract() == [u'REQUIRED FIELD']:
            item['title'] = response.xpath('//title/CharacterString/text()').extract()
            item['author'] = response.xpath('//individualName/CharacterString/text()').extract()
            for sel in response.xpath('//linkage'):
                link = response.xpath('//URL/text()').extract()
                linkstring = str(link)
                pdf = linkstring.find(".pdf", len(linkstring)-5, len(linkstring))
                download = linkstring.find("file/get", 36)
                if pdf == -1 and download == -1:
                    item['link'] = link
                # Finds text in multiple <gmd:URL> tags (the links)
                # Adds each of them to link in items.py
            # json.dump(dict(item), f)
            # f.write("\n")
            # return item (back to the parse function)
            return item

        '''
        print "\n"
        yield item # prints contents of MetadatascraperItem() from items.py
        print "\n"
        '''


    '''
    def spider_closed(self, spider):
        logger.info(">>>>>>>>>>>>>>>>>>> SPIDER CLOSED <<<<<<<<<<<<<<<<<<<<<")
        f.close()
    '''
