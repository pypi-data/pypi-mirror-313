from typing                                             import Dict
from cbr_user_data.ui.models.Model__UI__User__Menu_Item import Model__UI__User__Menu_Item
from osbot_utils.base_classes.Type_Safe                 import Type_Safe
from osbot_utils.helpers.Safe_Id                        import Safe_Id

class Model__UI__User__Menu(Type_Safe):
    menu_items: Dict[Safe_Id, Model__UI__User__Menu_Item]