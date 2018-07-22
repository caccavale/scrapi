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
    def __init__(self, domain, cookies=None, cache=False, max_cache_size=128, *args, **kwargs):
        if not domain.startswith('http'):
            domain = 'http://' + domain
        self.domain = domain
        self.cookies = cookies if cookies is not None else {}
        super().__init__(__name__, *args, **kwargs)

        if cache:
            self.got = functools.lru_cache(maxsize=max_cache_size)(self.got)
        self.route('/<path:path>', methods=['GET'])(self.get)
        self.route('/', methods=['GET'])(self.get)

    def get(self, path=''):
        return self.got(path, urllib.parse.unquote(request.query_string.decode()))

    def got(self, path='', query_string=''):
        page = requests.get('/'.join([self.domain, path]), cookies=self.cookies).text
        if not query_string:
            return page

        soup = Soup(page, 'lxml')
        results = {}
        for key, selectors in urllib.parse.parse_qs(query_string).items():
            for selector in selectors:
                results[key] = results.get(key, []) + [str(tag) for tag in soup.select(selector)]

        return json.dumps(results)

if __name__ == '__main__':
    import sys
    Scrapi(sys.argv[1]).run()