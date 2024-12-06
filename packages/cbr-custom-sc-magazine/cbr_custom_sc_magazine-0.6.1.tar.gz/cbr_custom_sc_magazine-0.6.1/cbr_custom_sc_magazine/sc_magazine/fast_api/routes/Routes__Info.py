from osbot_fast_api.api.Fast_API_Routes   import Fast_API_Routes
from cbr_custom_sc_magazine.utils.Version import version__cbr_custom_sc_magazine

ROUTES_PATHS__INFO = ['/info/version']

class Routes__Info(Fast_API_Routes):
    tag :str = 'info'

    def version(self):
        return {'version': version__cbr_custom_sc_magazine}

    def setup_routes(self):
        self.add_route_get(self.version)

