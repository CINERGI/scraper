import scrapy
import json
from pprint import pprint
#import webbrowser

#https://www.youtube.com/watch?v=YLj1kuSZWcU

#open a new tab
#new=2
#title_to_search = raw_input("Enter the title: ")
#tabUrl = "https://www.google.com/search?q=";
#webbrowser.open(tabUrl + title_to_search, new=new);
data = []
with open('spider4_metadata_abstractmissingonly_pdf_title.json') as data_file:
    for line in data_file:
        data.append(json.loads(line))
    #data = json.load(data_file)
pprint(data)
    #json_data.close()


# subclass scrapy.Spider and define some attributes
class GoogleScraperSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        ""
    ]

        #tabUrl + title_to_search


#    def parse(self, response):
#        filename = response.url.split("/")[-2] + '.html'
#        with open(filename, 'wb') as f:
#            f.write(response.body)
'''
    def parse(self, response):
        for sel in response.xpath('//ul/li/h3/div/div/cite/'):
            link = sel.xpath('text()').extract()
            print link
'''
