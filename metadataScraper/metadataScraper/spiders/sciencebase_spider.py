# Sciencebase Abstract Spider v1
# Reads output json file from metadata_scraper for catalogItem URL
# Concatenates ?json=True to catalogItem then visits page
# Scrapes JSON for parentID; concatenates to sciencebase URL and visits page
# Scrapes parent page for abstract using HTML paths
# Date created: July 13 2015

# 7/14/15: Triple quotes at beginning and end only

'''
import scrapy
# from scrapy import signals
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import json
import time
from metadataScraper.items import MetadatascraperItem

# timestamp = time.strftime("%Y-%m-%d_%H%M%S")
# filename = "metadata_" + timestamp + ".json"
filename = "SPIDER_METADATA_4.json"
f = open(filename, 'r')

class MetadataSpider(scrapy.Spider):
    name = "parentabstract"
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
            item['author'] = response.xpath('//individualName/CharacterString/text()').extract()
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

            json.dump(dict(item), f, sort_keys=True)
            f.write("\n")
'''
