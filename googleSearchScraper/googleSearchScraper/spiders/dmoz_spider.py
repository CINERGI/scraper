import scrapy

# subclass scrapy.Spider and define some attributes
class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        #filename = response.url.split("/")[-2] + '.html'
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        for sel in response.xpath('//ul/li'):
            item = DmozItem()
            title = sel.xpath('a/text()').extract()
            link = sel.xpath('a/@href').extract()
            desc = sel.xpath('text()').extract()
            #print title, link, desc
            yield item
