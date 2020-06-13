"""
Run scrapy spiders from a script.

Blocks and runs all requests in parallel.  Accumulated items from all
spiders are returned as a list.
"""

import collections
from billiard.context import Process  # fork of multiprocessing that works with celery
from billiard.queues import Queue
from pydispatch import dispatcher
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


class ScrapyScriptException(Exception):
    pass


class Job(object):
    """A job is a single request to call a specific spider. *args and **kwargs
    will be passed to the spider constructor.
    """

    def __init__(self, spider, *args, **kwargs):
        """Parms:
          spider (spidercls): the spider to be run for this job.
        """
        self.spider = spider
        self.args = args
        self.kwargs = kwargs


class Processor(Process):
    """ Start a twisted reactor and run the provided scrapy spiders.
    Blocks until all have finished.
    """

    def __init__(self, settings=None, item_scraped=True):
        """
        Parms:
          settings (scrapy.settings.Settings) - settings to apply.  Defaults
        to Scrapy default settings.
        """
        Process.__init__(self)
        kwargs = {'ctx': __import__('billiard.synchronize')}

        self.results = Queue(**kwargs)
        self.items = {}
        self.item_scraped = item_scraped
        self.settings = settings or Settings()

    def _item_passed(self, item, response, spider):
        if spider.name not in self.items.keys():
            self.items[spider.name] = []
        if self.item_scraped is True:
            self.items[spider.name].append(dict(item))

    def _crawl(self, requests):
        """
        Parameters:
            requests (Request) - One or more Jobs. All will
                                 be loaded into a single invocation of the reactor.
        """
        self.crawler = CrawlerProcess(self.settings)

        # signal to result data
        dispatcher.connect(self._item_passed, signals.item_scraped)

        # crawl can be called multiple times to queue several requests
        for req in requests:
            self.crawler.crawl(req.spider, *req.args, **req.kwargs)

        self.crawler.start()
        self.crawler.stop()
        self.results.put(self.items)

    def run_jobs(self, jobs):
        """Start the Scrapy engine, and execute all jobs.  Return consolidated results
        in a single list.

        Parms:
          jobs ([Job]) - one or more Job objects to be processed.

        Returns:
          List of objects yielded by the spiders after all jobs have run.
        """
        if not isinstance(jobs, collections.Iterable):
            jobs = [jobs]
        self.validate(jobs)

        p = Process(target=self._crawl, args=[jobs])
        p.start()
        # p.join()
        # p.terminate()

    def data(self):
        return self.results.get()

    @staticmethod
    def validate(jobs):
        if not all([isinstance(x, Job) for x in jobs]):
            raise ScrapyScriptException('scrapy-script requires Job objects.')
