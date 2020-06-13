import unittest

from scrapy.settings import Settings
from scrapy_script import Job, Processor
from scrapyorg.scrapyorg.spiders.example import ExampleSpider
from scrapyorg.scrapyorg.spiders.parameterspassed import ParameterspassedSpider


class ScrapyScriptTests(unittest.TestCase):
    def test_create_valid_job(self):
        spider = ExampleSpider
        job = Job(spider)
        self.assertIsInstance(job, Job)

    def test_parameters_passed_to_spider(self):
        spider = ParameterspassedSpider
        job = Job(spider, 'cat1', fruit='banana')
        result = Processor().run_jobs(job)
        self.assertEqual(result, [dict(category='cat1', fruit='banana')])

    def test_no_spider_provided(self):
        self.assertRaises(TypeError, Job)

    def test_settings_flow_through_to_spider(self):
        settings = Settings()
        settings['BOT_NAME'] = 'alpha'
        job = Job(ExampleSpider, url='http://www.python.org')
        results = Processor(settings=settings).run_jobs(job)

        self.assertIn({'bot': 'alpha'}, results)

    def test_mulitple_jobs(self):
        jobs = [
            Job(ExampleSpider, url='http://www.python.org'),
            Job(ExampleSpider, url='http://www.github.com')
        ]

        results = Processor().run_jobs(jobs)
        self.assertEqual(len(results), 4)
