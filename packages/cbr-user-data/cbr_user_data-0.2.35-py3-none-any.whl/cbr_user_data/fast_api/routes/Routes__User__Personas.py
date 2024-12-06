from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes


class Routes__User__Personas(Fast_API_Routes):
    tag : str = 'personas'
    def personas_id(self):
        return {"message": "Personas id"}

    def setup_routes(self):
        self.add_route_get(self.personas_id)
        return self