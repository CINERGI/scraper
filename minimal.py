import scrapy

class MinimalSpider(scrapy.Spider):
    """The smallest Scrapy-Spider in the world!"""
    name = 'minimal'

    '''
    def start_requests(self):
        return[scrapy.Request(url)
            for url in ['http://www.google.com', 'http://yahoo.com']]
    '''

    start_urls = [
        'http://www.google.com',
        'http://www.yahoo.com',
    ]

    def parse(self, response):
        self.log('GETTING URL: %s' % response.url)
