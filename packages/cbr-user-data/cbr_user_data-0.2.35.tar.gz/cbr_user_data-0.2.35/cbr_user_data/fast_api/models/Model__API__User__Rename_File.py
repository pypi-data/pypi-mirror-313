from fastapi                            import Body
from dataclasses                        import dataclass
from osbot_utils.base_classes.Type_Safe import Type_Safe

SWAGGER_EXAMPLE__Model__API__User__Rename_File  = Body(..., example=dict(file_id       = ''                ,
                                                                                  new_file_name = 'new-file-name.md'))
@dataclass
class Model__API__User__Rename_File(Type_Safe):
    file_id      : str                                     # todo: find way to make Random_Guid work here
    new_file_name : str

