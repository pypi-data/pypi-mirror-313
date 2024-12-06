from mangum                                         import Mangum
from cbr_user_data.fast_api.User_Data__Fast_API     import User_Data__Fast_API

fast_api_user_data = User_Data__Fast_API().setup()
app                = fast_api_user_data.app()
run                = Mangum(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)