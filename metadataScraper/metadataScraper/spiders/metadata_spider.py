# Metadata Scraper v1
# ***Currently not working; use metadata_spider2.py***

import scrapy
from scrapy.selector import Selector

from metadataScraper.items import MetadatascraperItem

class MetadataSpider(scrapy.Spider):
    name = "metadata-spider"
    allowed_domains = ["cinergi.cloudapp.net"]
    start_urls = [
        "http://cinergi.cloudapp.net/geoportal/rest/document?id={11161776-58F6-4552-A0A2-DB9A6EEAB29D}"
    ]

    def parse(self, response):
        '''
        for sel in response.xpath('//ul/li'):
            item = MetadatascraperItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item
        '''

        item = MetadatascraperItem()
        # item['title'] = response.xpath('//gmd:title/gco:CharacterString/text()').extract()

        response.register_namespace("gmd", "http://www.isotc211.org/2005/gmd/")
        for sel in response.xpath('//gmd:linkage/gmd:URL'):
            #sel.register_namespace("gmd", "http://www.isotc211.org/2005/gmd/")
            item['link'] = sel.xpath('text()').extract()

        yield item
