import re


class UrlUtils(object):
    URL_REGEX = 'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'

    def __init__(self, url_regex=None):
        self.url_regex = url_regex or self.URL_REGEX

    def find_urls(self, response):
        try:
            return re.findall(self.url_regex, response)
        except:
            return []

    async def process_response(self, response):
        if response.status != 200:
            return []

        response_text = await response.text()

        return self.find_urls(response_text)
