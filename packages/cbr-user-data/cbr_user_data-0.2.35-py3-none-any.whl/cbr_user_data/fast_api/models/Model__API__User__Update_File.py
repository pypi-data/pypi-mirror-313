from fastapi                            import Body
from dataclasses                        import dataclass
from osbot_utils.base_classes.Type_Safe import Type_Safe

SWAGGER_EXAMPLE__Model__API__User__Update_File  = Body(..., example=dict( file_bytes__base64 = b'new file contents',
                                                                                  file_id  = ''                            ))
@dataclass
class Model__API__User__Update_File(Type_Safe):
    file_bytes__base64 : str
    file_id            : str = None                                  # todo: find way to make Random_Guid work here

