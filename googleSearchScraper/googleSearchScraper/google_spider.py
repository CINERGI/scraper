import scrapy
import webbrowser

#https://www.youtube.com/watch?v=YLj1kuSZWcU

#open a new tab
new=2

title_to_search = raw_input("Enter the title: ")

tabUrl = "https://www.google.com/search?q=";

webbrowser.open(tabUrl + title_to_search, new=new);

subclass scrapy.Spider and define some attributes
class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["www.google.com"]
    start_urls = [
        tabUrl + title_to_search,
    ]

#    def parse(self, response):
#        filename = response.url.split("/")[-2] + '.html'
#        with open(filename, 'wb') as f:
#            f.write(response.body)

        #for sel in response.xpath('//ul/li'):
        #    item = DmozItem()
        #    title = sel.xpath('a/text()').extract()
        #    link = sel.xpath('a/@href').extract()
        #    desc = sel.xpath('text()').extract()
        #    #print title, link, desc
        #    yield item
