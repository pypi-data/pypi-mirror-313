from fastapi                            import Body
from dataclasses                        import dataclass
from osbot_utils.base_classes.Type_Safe import Type_Safe

SWAGGER_EXAMPLE__Model__API__User__Add_File  = Body(..., example=dict(file_name  ='an_file.txt'    ,
                                                                             file_bytes = b'file_contents',
                                                                             folder_id  = ''              ))
@dataclass
class Model__API__User__Add_File(Type_Safe):
    file_name          : str
    file_bytes__base64 : str
    folder_id          : str = None                                  # todo: find way to make Random_Guid work here

