import scrapy
import webbrowser

#https://www.youtube.com/watch?v=YLj1kuSZWcU

#open a new tab
#new=2
#title_to_search = raw_input("Enter the title: ")
#tabUrl = "https://www.google.com/search?q=";
#webbrowser.open(tabUrl + title_to_search, new=new);

# subclass scrapy.Spider and define some attributes
class DmozSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["file:///"]
    start_urls = [
        "file:///Users/aarongong/CINERGIScrapy/googleSearchScraper/tutorial/www.google.com.html"
    ]
        #tabUrl + title_to_search


#    def parse(self, response):
#        filename = response.url.split("/")[-2] + '.html'
#        with open(filename, 'wb') as f:
#            f.write(response.body)

    def parse(self, response):
        for sel in response.xpath('//ul/li/h3/div/div/cite/'):
            link = sel.xpath('text()').extract()
            print link
