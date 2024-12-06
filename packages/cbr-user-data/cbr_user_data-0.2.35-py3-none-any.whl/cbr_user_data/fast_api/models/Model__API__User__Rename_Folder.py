from fastapi                            import Body
from dataclasses                        import dataclass
from osbot_utils.base_classes.Type_Safe import Type_Safe

SWAGGER_EXAMPLE__Model__API__User__Rename_Folder  = Body(..., example=dict(folder_id       = ''        ,
                                                                                  new_folder_name = 'new-name'))
@dataclass
class Model__API__User__Rename_Folder(Type_Safe):
    folder_id       : str                                   # todo: find way to make Random_Guid work here
    new_folder_name : str

