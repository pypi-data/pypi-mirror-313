from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes
from cbr_user_data.utils.Version        import version__cbr_user_data


class Routes__Info(Fast_API_Routes):
    tag : str = 'info'

    def ping(self):
        return {"pong" : '42' }

    def version(self):
        return {"version" : version__cbr_user_data }

    def setup_routes(self):
        self.add_route_get(self.ping   )
        self.add_route_get(self.version)
        return self