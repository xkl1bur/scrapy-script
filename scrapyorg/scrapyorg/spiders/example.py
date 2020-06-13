# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapyorg.scrapyorg.items import ScrapyorgItem


# Define a Scrapy Spider, which can accept *args or **kwargs
# https://doc.scrapy.org/en/latest/topics/spiders.html#spider-arguments
class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['scrapy.org']

    # start_urls = ['http://scrapy.org/']

    def parse(self, response):
        item = ScrapyorgItem()
        item['url'] = response.request.url
        item['title'] = response.xpath('//title/text()').extract_first()
        yield item

    def start_requests(self):
        yield Request(self.url)  # spider-arguments
