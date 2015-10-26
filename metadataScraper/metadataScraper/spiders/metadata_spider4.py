# Metadata Scraper v4
# Scrapes metadata URLs from http://hydro10.sdsc.edu/metadata/ScienceBase_WAF_dump/
# Passes URLs to metadata scraper to get links under <gmd:URL> tag, title, author

# Run in terminal with scrapy crawl sciencebase -o test.json
# to redirect stderr to file: text.json &> sciencebase_stderr.txt


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
        "http://hydro10.sdsc.edu/metadata/cuahsi/"
    ]
    # sciencebase - 1374 output; 626 missing abstract
    # cuahsi - 93 output; 9 no abstract

    def parse(self, response):
        for href in response.xpath("//a/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_metadata)

    def parse_metadata(self, response):
        item = MetadatascraperItem()
        response.selector.remove_namespaces()

        item['identifier'] = response.xpath('//fileIdentifier/CharacterString/text()').extract_first()
        self.logger.info(item['identifier'] )

        #abstract = response.xpath('//abstract/CharacterString/text()').extract()[0]
        # self.logger.info(len( abstract ) )
        hasAbstract, abstract = self.abstractChecker(response)

        #if hasAbstract is False and abstract < 100:
        if hasAbstract is False:
            item['title'] = response.xpath('//title/CharacterString/text()').extract()
            #item['webUrl'] = response.geturl().extract()
            item['webUrl'] = response.url
            item['abstractCount'] = abstract

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
            yield item

    def abstractChecker(self, response):
        try:
           abstract = "0"
           abstract = str(len (response.xpath('//abstract/CharacterString/text()').extract()[0] ))
           if (response.xpath('//abstract/CharacterString/text()').extract() == [u'REQUIRED FIELD']):
               return False, None
           if (response.xpath('//abstract/CharacterString/text()') == None ):
               return False, None
           if (len (response.xpath('//abstract/CharacterString/text()').extract()) == 0):
               return False, None  # no abstract
           #abstract = len (response.xpath('//abstract/CharacterString/text()').extract()[0] )
           if (len (abstract) < 100):
               return False, abstract  # short abstract  #return true
        except:
            #self.logger.info('ERROR getting abstract. Work on logic for abstractChecker')
            return False, abstract  # error abstract #return true
        else:
            return False, abstract
        #return True, None

# Trying to get only 9 abstract < 100 and the no abstracts to print out.
# Need to find out from terminal output, somefile.txt what scrapy interprets as no abstract -fixed
'''
           abstract = len (response.xpath('//abstract/CharacterString/text()').extract()[0])
           if (len (abstract) < 500):
               return False,abstract  # short abstract
           return True, abstract
        except:
            self.logger.info('ERROR getting abstract. Work on logic for abstractChecker')
            return False,None  # error abstract
        return False, None
'''
