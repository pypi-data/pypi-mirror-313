from osbot_fast_api.api.Fast_API_Routes                                 import Fast_API_Routes
from cbr_custom_sc_magazine.sc_magazine.content.Http_Content__Articles  import Http_Content__Articles

ROUTES_PATHS__UK = ['/uk/articles-data',
                    '/uk/articles-html',
                    '/uk/homepage-data',
                    '/uk/homepage-html']

class Routes__UK(Fast_API_Routes):
    tag                  : str = 'uk'
    http_content_articles: Http_Content__Articles

    def articles_data(self, page=1):
        return self.http_content_articles.articles__data(page=page)

    def articles_html(self, page=1):
        return self.http_content_articles.articles__html(page=page)

    def homepage_data(self):
        return self.http_content_articles.homepage__data()

    def homepage_html(self):
        return self.http_content_articles.homepage__html()

    def setup_routes(self):
        self.add_route_get(self.articles_data)
        self.add_route_get(self.articles_html)
        self.add_route_get(self.homepage_data)
        self.add_route_get(self.homepage_html)

