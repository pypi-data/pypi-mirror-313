import requests
from bs4                                                            import BeautifulSoup
from osbot_utils.base_classes.Type_Safe                             import Type_Safe
from osbot_utils.decorators.methods.cache_on_self                   import cache_on_self
from osbot_utils.utils.Http                                         import url_join_safe
from cbr_custom_sc_magazine.sc_magazine.content.SC_Magazine_Parser  import SC_Magazine_Parser

class Http_Content__Articles(Type_Safe):
    server: str = 'https://insight.scmagazineuk.com/'

    #@cache_on_self                                  # todo: add a better caching architecture (for example onne based on S3_DB__Cache)
    def requests_get(self, path='', params=None):
        print(path, params)
        url = url_join_safe(self.server, path)
        return requests.get(url, params=params)


    def articles__data(self, page=1):
        page_html          = self.articles__html(page=page)
        sc_magazine_parser = SC_Magazine_Parser(page_html)
        return sc_magazine_parser.parse_articles_page().json()

    def articles__html(self, page=1):
        path = f'articles'
        params = dict(page=page)
        return self.requests_get(path, params).text

    def articles__soup(self):
        html = self.articles__html()
        return BeautifulSoup(html, 'html.parser')

    def homepage__html(self):
        return self.requests_get().text

    def homepage__data(self):
        page_html          = self.homepage__html()
        sc_magazine_parser = SC_Magazine_Parser(page_html)
        return sc_magazine_parser.parse_homepage().json()
