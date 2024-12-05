from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes

ROUTES_PATHS__SC_MAGAZINE__UK = ['/raw-html']

class Routes__SC_Magazine__UK(Fast_API_Routes):
    tag : str = 'uk'

    def raw_html(self, path='/'):
        return 'will be here'

    def setup_routes(self):
        self.add_route_get(self.raw_html)

