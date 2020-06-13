import json
from scrapy_script import Job, Processor
from scrapyorg.scrapyorg.spiders.example import ExampleSpider

# Create jobs for each instance. *args and **kwargs supplied here will
# be passed to the spider constructor at runtime
githubJob = Job(ExampleSpider, url='https://www.github.com')
pythonJob = Job(ExampleSpider, url='https://www.python.org')

# Create a Processor, optionally passing in a Scrapy Settings object.
processor = Processor(settings=None, item_scraped=True)

# Start the reactor, and block until all spiders complete.
processor.run_jobs([githubJob, pythonJob])

# Print the consolidated results
print(json.dumps(processor.data(), indent=4, ensure_ascii=False))
