from fastapi                                              import Request
from cbr_shared.cbr_backend.users.S3_DB__Users            import S3_DB__Users
from cbr_shared.cbr_backend.users.decorators.with_db_user import with_db_user
from osbot_fast_api.api.Fast_API_Routes                   import Fast_API_Routes

class Routes__User__Chats(Fast_API_Routes):
    tag      : str = 'chats'
    db_users : S3_DB__Users

    @with_db_user
    def db_user(self, request: Request):
        db_user = request.state.db_user
        return db_user

    def chats(self, request: Request):
        db_user = self.db_user(request)
        if db_user:
            return db_user.user_past_chats()
        return {}

    def chats_table(self, request: Request):
        db_user = self.db_user(request)
        if db_user:
            return db_user.user_past_chats__in_table()
        return {}

    def chat_add(self, request: Request, chat_path):

        db_user = self.db_user(request)
        if db_user:
            return db_user.user_past_chats__add_chat(chat_path)
        return False

    def chats_clear(self,request: Request):
        db_user = self.db_user(request)
        if db_user:
            return db_user.user_past_chats__clear()



    def setup_routes(self):
        self.add_route_post  (self.chat_add    )
        self.add_route_get   (self.chats       )
        self.add_route_get   (self.chats_table )
        self.add_route_delete(self.chats_clear )

