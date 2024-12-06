from starlette.requests                                     import Request
from cbr_shared.cbr_backend.llms.LLM__Content__Actions      import LLM__Content__Actions
from cbr_shared.cbr_backend.users.decorators.with_db_user   import with_db_user
from osbot_fast_api.api.Fast_API_Routes                     import Fast_API_Routes

class Routes__User__File_To_LLMs(Fast_API_Routes):
    tag                 : str                    = 'file-to-llms'
    llm_content_actions : LLM__Content__Actions

    def file_system(self, request: Request):
        from cbr_shared.cbr_backend.files.User__File__System import User__File__System

        db_user = request.state.db_user
        return User__File__System(db_user=db_user).setup()

    @with_db_user
    def file_summary(self, request: Request, file_id: str, re_create:bool=False):
        from osbot_utils.utils.Files  import file_extension
        from osbot_utils.utils.Status import status_ok

        file_system   = self.file_system(request)
        user_file     = file_system.file(file_id)

        file_summary  = user_file.summary() if re_create is False else ''
        if not file_summary:
            extension = file_extension(user_file.data().file_name)
            if extension == ".png":
                image_bytes = user_file.contents()
                file_summary = self.llm_content_actions.create_summary__for_image(image_bytes=image_bytes)
            else:
                file_contents = user_file.contents().decode()
                file_summary  = self.llm_content_actions.create_summary(target_text=file_contents)
            user_file.summary__update(file_summary)
        return status_ok(data=file_summary)

    @with_db_user
    def folder_summary(self, request: Request, folder_id: str, re_create: bool = False):            # todo: refactor out this code from here
        from osbot_utils.utils.Status import status_ok, status_error

        from osbot_utils.utils.Json import json_loads

        file_system    = self.file_system(request)

        folder_summary = file_system.folder_summary(folder_id=folder_id)
        if not folder_summary and re_create:
            user_folder = file_system.user_folders().user_folder(user_folder_id=folder_id)
            if not user_folder:
                return status_error(f'folder not found: {folder_id}')

            def process_files(files_ids, files_summaries__prompt):
                for file_id in files_ids:
                    user_file     = file_system.file(file_id)
                    file_data    = user_file.data()
                    file_summary = user_file.summary()
                    if file_summary:
                        #files_summaries[file_id] = file_summary.decode()
                        files_summaries__prompt += f"""\
******************************
## {file_data.file_name}

**updated_date**: {file_data.updated__date} | **file_id**: {file_id}
******************************

{ json_loads(file_summary.decode()) }
    
"""
                return files_summaries__prompt
            all_files_summaries__prompt = ""
            all_files_summaries__prompt = process_files(user_folder.files, all_files_summaries__prompt)

            for sub_folder_id in user_folder.folders:                                                   # todo: add support for all sub-folders (since this is only going one level deep)
                sub_folder                  = file_system.user_folders().user_folder(sub_folder_id)
                all_files_summaries__prompt = process_files(sub_folder.files, all_files_summaries__prompt)
            if all_files_summaries__prompt:
                folder_summary = self.llm_content_actions.create_summary(target_text=all_files_summaries__prompt)
                file_system.folder_summary__update(folder_id=folder_id, folder_summary=folder_summary)
            else:
                folder_summary = '... there were no files summary to work with'

        if folder_summary:
            return status_ok(data=folder_summary)
        return status_error(f'folder summary not found: {folder_id}')


    def setup_routes(self):
        self.add_route_post  (self.file_summary  )
        self.add_route_post  (self.folder_summary)

