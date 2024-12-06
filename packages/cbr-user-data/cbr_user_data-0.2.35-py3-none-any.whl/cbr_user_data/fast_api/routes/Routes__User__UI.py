from cbr_user_data.ui.UI__User__Menu    import UI__User__Menu
from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes


class Routes__User__UI(Fast_API_Routes):
    tag          : str = 'ui'
    ui_user_menu : UI__User__Menu

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ui_user_menu.load_cbr_user_menu()


    def left_menu(self):
        return self.ui_user_menu.json__cached()

    def setup_routes(self):
        self.add_route_get(self.left_menu)