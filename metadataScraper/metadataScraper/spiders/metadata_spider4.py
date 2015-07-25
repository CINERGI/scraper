# Metadata Scraper v4
# Scrapes metadata URLs from http://hydro10.sdsc.edu/metadata/ScienceBase_WAF_dump/
# Passes URLs to metadata scraper to get links under <gmd:URL> tag, title, author
# Run in terminal with scrapy crawl metadata
# SAMPLE OUTPUT can be found in s3output.json
# Date: July 8 2015
# Quirk: the TO PARENT DIRECTORY url also gets scraped from hydro10 resulting in
# an empty entry in the output json {"title": [], "author": []} because it
# doesn't link to an xml document but rather goes up a level in the directory


import scrapy
# from scrapy import signals
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import json
import time
from metadataScraper.items import MetadatascraperItem

# timestamp = time.strftime("%Y-%m-%d_%H%M%S")
# filename = "metadata_" + timestamp + ".json"
#filename = "SPIDER_METADATA_4.json"
#f = open(filename, 'w')

class MetadataSpider(scrapy.Spider):
    name = "sciencebase"
    allowed_domains = ["hydro10.sdsc.edu"]
    start_urls = [
        "http://hydro10.sdsc.edu/metadata/ScienceBase_WAF_dump/"
    ]

    def parse(self, response):

        for href in response.xpath("//a/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_metadata)

    def parse_metadata(self, response):

        item = MetadatascraperItem()
        response.selector.remove_namespaces()

        if response.xpath('//abstract/CharacterString/text()').extract() == [u'REQUIRED FIELD']:
            item['title'] = response.xpath('//title/CharacterString/text()').extract()
            #item['author'] = response.xpath('//individualName/CharacterString/text()').extract()
            for sel in response.xpath('//linkage'):
                link = response.xpath('//URL/text()').extract()

                for i in range(len(link)):
                    linkstring = str(link[i])
                    if linkstring.find(".pdf") != -1:
                        item['pdf'] = link[i]
                    elif linkstring.find("file/get") != -1:
                        item['download'] = link[i]
                    elif linkstring.find("catalog/item") != -1:
                        item ['catalogItem'] = link[i]
                    else:
                        item['otherLinks'] = link[i]

            # json.dump(dict(item), f, sort_keys=True)
            # f.write("\n")

            # temporary
            yield item
