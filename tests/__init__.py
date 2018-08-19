import asyncio
from unittest import TestCase
from unittest.mock import Mock

from main import Crawler


class BaseAsyncTest(TestCase):
    def setUp(self):
        super().setUp()
        self.url = 'http://wikipedia.com'

    def get_crawler(self, urls=None, **kwargs):
        urls = urls or [self.url]
        return Crawler(urls, **kwargs)

    def run_coroutine(self, coroutine):
        return asyncio.get_event_loop().run_until_complete(coroutine)

    def _get_mock_coroutine(self, *args, **kwargs):
        """
        This mocks out an async function.

        See: https://blog.miguelgrinberg.com/post/unit-testing-asyncio-code
        """
        m = Mock(*args, **kwargs)

        async def mock_coroutine(*args, **kwargs):
            return m(*args, **kwargs)

        mock_coroutine.mock = m
        return mock_coroutine

    def get_mock_session(self, get_response):
        session = Mock()
        session.get = self._get_mock_coroutine(return_value=get_response)
        session.close = self._get_mock_coroutine(side_effect=None)

        return session

    def get_mock_url_utils(self, process_response_results):
        url_utils = Mock()
        url_utils.process_response = self._get_mock_coroutine(return_value=process_response_results)

        return url_utils

    def get_mock_response(self, status_code, response_text=None, **kwargs):
        response = Mock(status=status_code)
        response.text = self._get_mock_coroutine(return_value=response_text or '', **kwargs)

        return response

