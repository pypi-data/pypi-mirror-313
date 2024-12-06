from osbot_fast_api.api.Fast_API import Fast_API

class User_Data__Fast_API(Fast_API):
    base_path  : str  = '/user-data'
    enable_cors: bool = True

    def setup_routes(self):

        from cbr_user_data.fast_api.routes.Routes__User__Notifications  import Routes__User__Notifications
        from cbr_user_data.fast_api.routes.Routes__Info                 import Routes__Info
        from cbr_user_data.fast_api.routes.Routes__User                 import Routes__User
        from cbr_user_data.fast_api.routes.Routes__User__Chats          import Routes__User__Chats
        from cbr_user_data.fast_api.routes.Routes__User__File_To_LLMs   import Routes__User__File_To_LLMs
        from cbr_user_data.fast_api.routes.Routes__User__File_System    import Routes__User__File_System
        from cbr_user_data.fast_api.routes.Routes__User__Session        import Routes__User__Session
        from cbr_user_data.fast_api.routes.Routes__User__Personas       import Routes__User__Personas
        from cbr_user_data.fast_api.routes.Routes__User__UI             import Routes__User__UI

        self.add_routes(Routes__Info               )
        self.add_routes(Routes__User               )
        self.add_routes(Routes__User__UI           )
        self.add_routes(Routes__User__Chats        )
        self.add_routes(Routes__User__File_To_LLMs )
        self.add_routes(Routes__User__File_System  )
        self.add_routes(Routes__User__Session      )
        self.add_routes(Routes__User__Personas     )
        self.add_routes(Routes__User__Notifications)