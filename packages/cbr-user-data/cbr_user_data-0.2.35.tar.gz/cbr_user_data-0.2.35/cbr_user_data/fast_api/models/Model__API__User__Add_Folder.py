from fastapi                            import Body
from dataclasses                        import dataclass
from osbot_utils.base_classes.Type_Safe import Type_Safe

SWAGGER_EXAMPLE__Model__API__User__Add_Folder  = Body(..., example=dict(folder_name      = 'new-folder'    ,
                                                                               parent_folder_id = ''              ))
@dataclass
class Model__API__User__Add_Folder(Type_Safe):
    folder_name      : str
    parent_folder_id : str = None                                  # todo: find way to make Random_Guid work here

