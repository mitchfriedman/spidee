import os

import asyncio

import datetime

import aiohttp

from crawler.url_utils import UrlUtils

PARENT_PATH = os.path.abspath(os.path.dirname(__file__)) + '/../'
SEEDS_PATH = PARENT_PATH + 'seed.txt'
SEEN_PATH = PARENT_PATH + 'seen.txt'


class Crawler(object):
    MAX_URLS = 20
    MAX_CONCURRENT_TASKS = 4

    def __init__(self, urls, url_utils=None, loop=None, session=None, num_urls_to_crawl=None,
                 max_concurrent_tasks=None):
        self.loop = loop or asyncio.get_event_loop()
        self.urls = urls
        self.num_urls_to_crawl = num_urls_to_crawl or self.MAX_URLS
        self.max_concurrent_tasks = max_concurrent_tasks or self.MAX_CONCURRENT_TASKS
        self.url_utils = url_utils or UrlUtils()

        self.seen = set()
        self.session = session or aiohttp.ClientSession(loop=self.loop)
        self.queue = asyncio.Queue(loop=self.loop)
        self.prepare_queue()

    def prepare_queue(self):
        for url in self.urls:
            self.queue.put_nowait(url)

    @property
    def seen_urls(self):
        return len(self.seen)

    async def fetch_url(self, url):
        self.seen.add(url)
        try:
            response = await self.session.get(url, allow_redirects=False)

            links = await self.url_utils.process_response(response)
            for link in links:
                if link in self.seen:
                    continue
                self.queue.put_nowait(link)
        except:
            pass
        finally:
            await self.session.close()

    def run(self):
        start_time = datetime.datetime.now()
        try:
            self.loop.run_until_complete(self.process())
        finally:
            self.loop.close()

        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        hours = duration // 3600
        mins = (duration - (hours * 3600)) // 60
        seconds = (duration - (hours * 3600) - (mins * 60))

        print('Done processing {} urls in {:0>2}:{:0>2}:{:05.2f}'.format(self.seen_urls,
                                                                         int(hours), int(mins), seconds))
        self.write_seen_urls()

    def write_seen_urls(self):
        with open(SEEN_PATH, 'w') as f:
            for url in self.seen:
                f.write('{}\n'.format(url))

    async def work(self):
        while self.seen_urls < self.num_urls_to_crawl:
            url = await self.queue.get()
            await self.fetch_url(url)
            self.queue.task_done()

    async def process(self):
        await asyncio.wait([asyncio.ensure_future(self.work()) for _ in range(self.max_concurrent_tasks)])
