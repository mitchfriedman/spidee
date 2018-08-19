from unittest.mock import Mock

from tests import BaseAsyncTest


class TestCrawler(BaseAsyncTest):
    def test_fetch_url_no_urls_found(self):
        response = Mock()
        session = self.get_mock_session(response)
        url_utils = self.get_mock_url_utils(list())

        crawler = self.get_crawler(session=session, url_utils=url_utils)

        self.run_coroutine(crawler.fetch_url(self.url))

        self.assertEqual(1, crawler.seen_urls)
        self.assertEqual(1, crawler.queue.qsize())
        url_utils.process_response.mock.assert_called_once_with(response)
        session.close.mock.assert_called_once_with()

    def test_fetch_url_more_urls_found(self):
        response = Mock()
        session = self.get_mock_session(response)
        url_utils = self.get_mock_url_utils(['http://other_url.com'])

        crawler = self.get_crawler(session=session, url_utils=url_utils)

        self.run_coroutine(crawler.fetch_url(self.url))

        self.assertEqual(1, crawler.seen_urls)
        self.assertEqual(2, crawler.queue.qsize())

        url_utils.process_response.mock.assert_called_once_with(response)
        session.close.mock.assert_called_once_with()

    def test_fetch_url_duplicate_urls_found(self):
        response = Mock()
        session = self.get_mock_session(response)
        url_utils = self.get_mock_url_utils([self.url])

        crawler = self.get_crawler(session=session, url_utils=url_utils)

        self.run_coroutine(crawler.fetch_url(self.url))

        self.assertEqual(1, crawler.seen_urls)
        self.assertEqual(1, crawler.queue.qsize())

        url_utils.process_response.mock.assert_called_once_with(response)
        session.close.mock.assert_called_once_with()
