# -*- coding: utf-8 -*-
import scrapy


class ParameterspassedSpider(scrapy.Spider):
    name = 'myspider'
    allowed_domains = ['python.org']
    start_urls = ['http://www.python.org']

    def __init__(self, category=None, *args, **kwargs):
        super(ParameterspassedSpider, self).__init__(*args, **kwargs)
        self.category = category

    def parse(self, response):
        return dict(category=self.category, fruit=self.fruit)
