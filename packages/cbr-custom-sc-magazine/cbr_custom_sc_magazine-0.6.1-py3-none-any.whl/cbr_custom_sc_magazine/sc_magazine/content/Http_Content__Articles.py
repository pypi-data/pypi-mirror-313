import requests
from bs4                                 import BeautifulSoup
from osbot_utils.base_classes.Type_Safe  import Type_Safe
from osbot_utils.utils.Http              import url_join_safe


class Http_Content__Articles(Type_Safe):
    server: str = 'https://insight.scmagazineuk.com/'

    def requests_get(self, path=''):
        url = url_join_safe(self.server, path)
        return requests.get(url)

    def articles__html(self):
        return self.requests_get().text

    def articles__soup(self):
        html = self.articles__html()
        return BeautifulSoup(html, 'html.parser')