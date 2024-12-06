from starlette.requests                                         import Request
from cbr_shared.cbr_backend.session.S3_DB__Session              import S3_DB__Session
from cbr_shared.cbr_backend.session.decorators.with_db_session  import with_db_session
from cbr_shared.cbr_backend.users.S3_DB__Users                  import S3_DB__Users
from osbot_fast_api.api.Fast_API_Routes                         import Fast_API_Routes

class Routes__User__Session(Fast_API_Routes):
    tag     : str = 'session'
    db_users: S3_DB__Users

    @with_db_session
    def session_config(self, request: Request):
        db_session : S3_DB__Session = request.state.db_session
        return db_session.session_config()

    @with_db_session
    def logged_in(self, request: Request):
        db_session : S3_DB__Session = request.state.db_session
        return {"logged_in": db_session.exists()}

    def setup_routes(self):
        self.add_route_get(self.logged_in    )
        self.add_route_get(self.session_config)
        return self