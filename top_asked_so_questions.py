'''
import scrapy
import urlparse


class Question(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    excerpt = scrapy.Field()
    tags = scrapy.Field()
    #abstract = scrapy.Field()

class StackoverflowTopQuestionsSpider(scrapy.Spider):
    name = 'so-top-questions'

    def __init__(self, tag=None):
        questions_url = 'http://stackoverflow.com/questions'
        #questions_url = 'https://www.sciencebase.gov/catalog/item/537f6a94e4b021317a86e794'
        if tag:
            questions_url += '/tagged/%s' % tag

        self.start_urls = [questions_url + '?sort=frequent']
        #self.start_urls = [questions_url]

    def parse(self, response):
        build_full_url = lambda link: urlparse.urljoin(response.url, link)

        #hidden-xs
        for qsel in response.css("questions > div"):
            it = Question()

            it['link'] = build_full_url(
                #/div[@class='summary']/h3/a[@class='question-hyperlink']
                qsel.css('.summary h3 > a').xpath('@href')[0].extract())
            it['title'] = qsel.css('.summary h3 > a::text')[0].extract()
            it['tags'] = qsel.css('a.post-tag::text').extract()
            it['excerpt'] = qsel.css('div.excerpt::text')[0].extract()
            #it['abstract'] = qsel.css('.sb-expander-content span::text')[0].extract()

            yield it
'''

import scrapy
import urlparse


class Question(scrapy.Item):
    #link = scrapy.Field()
    #title = scrapy.Field()
    #excerpt = scrapy.Field()
    abstract = scrapy.Field()

class StackoverflowTopQuestionsSpider(scrapy.Spider):
    name = 'so-top-questions'

    def __init__(self, tag=None):
        questions_url = 'https://www.sciencebase.gov/catalog/item'
        #if tag:
        #    questions_url += '/tagged/%s' % tag

        self.start_urls = [questions_url + '/537f6a94e4b021317a86e794']

    def parse(self, response):
        #build_full_url = lambda link: urlparse.urljoin(response.url, link)

        for qsel in response.css("*"):
            it = Question()

            #it['link'] = build_full_url(
            #    qsel.css('.summary h3 > a').xpath('@href')[0].extract())
            #it['title'] = qsel.css('.summary h3 > a::text')[0].extract()
            it['abstract'] = qsel.css('.sb-expander-content span::text')[0].extract()
            #it['excerpt'] = qsel.css('div.excerpt::text')[0].extract()

            yield it
