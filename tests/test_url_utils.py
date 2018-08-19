from crawler.url_utils import UrlUtils
from tests import BaseAsyncTest


class TestUrlUtils(BaseAsyncTest):
    def test_process_response_with_urls_ok(self):
        url_utils = UrlUtils()
        url1 = 'http://test.com'
        url2 = 'https://test2.com'
        response_text = '{},{}'.format(url1, url2)
        response = self.get_mock_response(200, response_text)
        urls = self.run_coroutine(url_utils.process_response(response))

        self.assertListEqual([url1, url2], urls)

    def test_process_response_url_not_found(self):
        url_utils = UrlUtils()
        response = self.get_mock_response(404)
        urls = self.run_coroutine(url_utils.process_response(response))

        self.assertListEqual([], urls)

    def test_process_response_throws_exception(self):
        url_utils = UrlUtils()
        response = self.get_mock_response(200, side_effect=Exception())

        with self.assertRaises(Exception):
            self.run_coroutine(url_utils.process_response(response))

