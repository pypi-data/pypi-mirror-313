from cbr_user_data.ui.models.Model__UI__User__Menu  import Model__UI__User__Menu
from osbot_utils.base_classes.Type_Safe             import Type_Safe
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self

FILE__CBR__USER__SITE_MENU_CONFIG = 'en/site/left-menu.toml'

class UI__User__Menu(Type_Safe):

    user_menu : Model__UI__User__Menu

    def load_cbr_user_menu(self):
        toml__user_menu = self.path__cbr_user_menu()
        self.load_from_file(toml__user_menu)

    def load_from_file(self, toml__user_menu):
        from osbot_utils.utils.Toml import toml_from_file

        menu_data      = toml_from_file(toml__user_menu)
        self.user_menu = Model__UI__User__Menu.from_json(menu_data)

    def path__cbr_user_menu(self):
        import cbr_content
        from osbot_utils.utils.Files import path_combine_safe

        return path_combine_safe(cbr_content.path, FILE__CBR__USER__SITE_MENU_CONFIG)

    @cache_on_self
    def json__cached(self):
        return self.user_menu.json()
