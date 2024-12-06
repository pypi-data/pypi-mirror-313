from mangum                                              import Mangum
from osbot_utils.utils.Env                               import get_env
from cbr_custom_file_data.fast_api.File_Data__Fast_API import File_Data__Fast_API

fast_api__file_data = File_Data__Fast_API().setup()
app                  = fast_api__file_data.app()
run                  = Mangum(app)

if __name__ == "__main__":                              # pragma: no cover
    import uvicorn
    port = get_env('PORT', 8080)
    uvicorn.run(app, host="0.0.0.0", port=port)