import io
from starlette.requests                                             import Request
from starlette.responses                                            import PlainTextResponse, StreamingResponse, Response
from cbr_shared.cbr_backend.files.User__File__System                import User__File__System
from cbr_shared.cbr_backend.users.decorators.with_db_user           import with_db_user
from cbr_user_data.fast_api.models.Model__API__User__Rename_File    import Model__API__User__Rename_File, SWAGGER_EXAMPLE__Model__API__User__Rename_File
from cbr_user_data.fast_api.models.Model__API__User__Rename_Folder  import Model__API__User__Rename_Folder, SWAGGER_EXAMPLE__Model__API__User__Rename_Folder
from cbr_user_data.fast_api.models.Model__API__User__Add_Folder     import Model__API__User__Add_Folder   , SWAGGER_EXAMPLE__Model__API__User__Add_Folder
from cbr_user_data.fast_api.models.Model__API__User__Add_File       import Model__API__User__Add_File     , SWAGGER_EXAMPLE__Model__API__User__Add_File
from cbr_user_data.fast_api.models.Model__API__User__Update_File    import Model__API__User__Update_File  , SWAGGER_EXAMPLE__Model__API__User__Update_File
from osbot_fast_api.api.Fast_API_Routes                             import Fast_API_Routes
from osbot_utils.utils.Misc                                         import base64_to_bytes
from osbot_utils.utils.Status                                       import status_ok, status_error


class Routes__User__File_System(Fast_API_Routes):
    tag: str = 'files'

    def file_system(self, request: Request):
        db_user = request.state.db_user
        return User__File__System(db_user=db_user).setup()

    @with_db_user
    def add_file(self, request: Request, model_add_file: Model__API__User__Add_File = SWAGGER_EXAMPLE__Model__API__User__Add_File):
        file_system = self.file_system(request)
        kwargs      = dict(file_name      =  model_add_file.file_name                          ,
                           file_bytes     =  base64_to_bytes(model_add_file.file_bytes__base64),
                           user_folder_id =  model_add_file.folder_id                         )
        user_file = file_system.add_file(**kwargs)
        return status_ok(message='File added', data = dict(file_id=user_file.file_id))

    @with_db_user
    def add_folder(self, request: Request, model_add_folder: Model__API__User__Add_Folder = SWAGGER_EXAMPLE__Model__API__User__Add_Folder):
        file_system = self.file_system(request)
        folder      = file_system.add_folder(parent_folder_id=model_add_folder.parent_folder_id, folder_name=model_add_folder.folder_name)
        return status_ok(message='folder created', data=dict(folder_id=folder.folder_id))


    @with_db_user
    def delete_file(self, request: Request, file_id:str):
        file_system = self.file_system(request)
        if file_system.delete_file(file_id):
            return status_ok(message="File deleted")
        return status_error(message="File not found")

    @with_db_user
    def delete_folder(self, request: Request, folder_id: str):
        file_system = self.file_system(request)
        try:
            if file_system.delete_folder(folder_id):
                return status_ok(message="Folder deleted")
            return status_error(message="Folder not found")
        except Exception as error:
            return status_error(message=str(error))

    @with_db_user
    def file_bytes(self, request: Request, file_id: str, version_id: str = None):
        file_system = self.file_system(request)
        file__bytes = file_system.file__bytes(file_id=file_id, version_id=version_id)
        if file__bytes:
            return status_ok(data=file__bytes)
        return status_error(message='file not found')

    @with_db_user
    def file_contents(self, request: Request, file_id: str):
        file_system   = self.file_system(request)
        file_contents = file_system.file__contents(file_id=file_id)
        if file_contents:
            return status_ok(data=file_contents)
        return status_error(message='file not found')

    @with_db_user
    def file_download(self, request: Request, file_id: str):
        file_system = self.file_system(request)
        file_contents = file_system.file__contents(file_id=file_id)
        if file_contents:
            file_bytes = base64_to_bytes(file_contents.get('file_bytes__base64'))
            file_name   = file_contents.get('file_data').get('file_name')

            return StreamingResponse(io.BytesIO(file_bytes),                                                # Use StreamingResponse to stream the file back to the client
                                     media_type="application/octet-stream",                                  # Specify generic binary file, adjust as needed
                                     headers={ "Content-Disposition": f"attachment; filename={file_name}"})

        else:
            return Response(status_code=404, content="File not found")


    @with_db_user
    def file_temp_signed_url(self, request: Request, file_id: str):
        file_system = self.file_system(request)
        signed_url = file_system.file__temp_signed_url(file_id)
        if signed_url:
            return status_ok(data=signed_url)
        return status_error(message='file not found')

    @with_db_user
    def file_versions(self, request: Request, file_id: str):
        file_system = self.file_system(request)
        versions = file_system.file_versions(file_id)
        if versions:
            return status_ok(data=versions)
        return status_error(message='file not found')

    @with_db_user
    def files(self, request: Request):
        file_system = self.file_system(request)
        return file_system.folder_structure__files()

    @with_db_user
    def folder(self, request: Request, folder_id: str = None):
        file_system = self.file_system(request)
        folder = file_system.folder(user_folder_id=folder_id)
        if folder:
            return status_ok(data=folder.json())
        return status_error(message='Folder not found')

    @with_db_user
    def folder_structure(self, request: Request):
        file_system = self.file_system(request)
        return file_system.folder_structure().json()

    @with_db_user
    def folder_rename(self, request: Request, model_rename_folder: Model__API__User__Rename_Folder = SWAGGER_EXAMPLE__Model__API__User__Rename_Folder):
        file_system = self.file_system(request)
        if  file_system.rename_folder(folder_id=model_rename_folder.folder_id, new_folder_name=model_rename_folder.new_folder_name):
            return status_ok(message='folder renamed')
        return status_error(message='folder not found')


    @with_db_user
    def json_view(self, request: Request):
        file_system = self.file_system(request)
        return file_system.json_view()

    @with_db_user
    def rename_file(self, request: Request, model_rename_file:Model__API__User__Rename_File = SWAGGER_EXAMPLE__Model__API__User__Rename_File):
        file_system = self.file_system(request)
        file_id     = model_rename_file.file_id
        file_name   = model_rename_file.new_file_name
        if file_system.rename_file(file_id, file_name):
            return status_ok(message='File renamed')
        return status_error(message='file not found')

    @with_db_user
    def rename_folder(self, request: Request, folder_id: str, new_name: str):
        file_system = self.file_system(request)
        if file_system.folder_rename(folder_id, new_name):
            return status_ok(message="File deleted")
        return status_error(message="File not found")

    @with_db_user
    def update_file(self, request: Request, model_update_file: Model__API__User__Update_File = SWAGGER_EXAMPLE__Model__API__User__Update_File):
        file_system  = self.file_system(request)
        file_id      = model_update_file.file_id
        file_bytes   = base64_to_bytes(model_update_file.file_bytes__base64)
        file         = file_system.file(file_id=file_id)
        if file:
            file.contents__update(file_bytes)
            return status_ok(message='File updated')
        return status_error(message='file not found')

    @with_db_user
    def tree_view(self, request: Request):
        file_system = self.file_system(request)
        tree_view   = file_system.tree_view()
        return PlainTextResponse(content=tree_view)


    def setup_routes(self):
        self.add_route_post  (self.add_file            )
        self.add_route_post  (self.add_folder          )
        self.add_route_delete(self.delete_file         )
        self.add_route_delete(self.delete_folder       )
        self.add_route_get   (self.file_temp_signed_url)
        self.add_route_get   (self.files               )
        self.add_route_get   (self.file_bytes          )
        self.add_route_get   (self.file_contents       )
        self.add_route_get   (self.file_download       )
        self.add_route_get   (self.file_versions       )
        self.add_route_get   (self.folder              )
        self.add_route_get   (self.folder_structure    )
        self.add_route_post  (self.folder_rename       )
        self.add_route_get   (self.json_view           )
        self.add_route_put   (self.update_file         )
        self.add_route_put   (self.rename_file         )
        self.add_route_get   (self.tree_view           )

        # self.add_route_delete(self.delete_file_system)

    # @with_db_user                                                        # todo: find better place to put this, since this feels quite dangerous to have like this
    # def delete_file_system(self, request: Request):                      # todo: we really should add an 'are you sure?" check there :)
    #     file_system = self.file_system(request)
    #     file_system.delete()
    #     return status_ok(message="File System deleted")
