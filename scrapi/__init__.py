import functools
import json
import logging
import os
import ssl
import urllib.parse

from bs4 import BeautifulSoup as Soup
from flask import Flask, request
import requests

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


class Scrapi(Flask):
    def __init__(self, domain, cookies=None, cache=False, max_cache=128, *args, **kwargs):
        super().__init__(__name__, *args, **kwargs)
        self.domain = domain if domain.startswith('http') else 'http://' + domain
        self.cookies = cookies if cookies is not None else {}
        self.cache = cache
        if self.cache:
            for func in [self.cached, self.get_soup, self.get_page]:
                setattr(self, func.__name__, functools.lru_cache(max_cache)(func))
        self.route('/<path:path>', methods=['GET'])(self.get)
        self.route('/', methods=['GET'])(self.get)

    def get(self, path=''):
        query_string = urllib.parse.unquote(request.query_string.decode())
        if not query_string:
            return self.get_page(path)

        if self.cache is True:
            selector_to_tags = lambda selector: self.cached(path, selector)
        else:
            soup = self.get_soup(path)
            selector_to_tags = lambda selector: soup.select(selector)

        return json.dumps({key: [str(tag) for selector in selectors
                                 for tag in selector_to_tags(selector)] for
                           key, selectors in urllib.parse.parse_qs(query_string).items()})

    def cached(self, path, selector):
        soup = self.get_soup(path)
        return soup.select(selector)

    def get_soup(self, path):
        return Soup(self.get_page(path), 'lxml')

    def get_page(self, path):
        return requests.get('/'.join([self.domain, path]), cookies=self.cookies).text

if __name__ == '__main__':
    import sys
    Scrapi(sys.argv[1]).run()