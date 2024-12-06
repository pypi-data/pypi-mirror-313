from mangum                                              import Mangum
from osbot_utils.utils.Env                               import get_env
from cbr_custom_open_sec_summit.fast_api.Open_Sec_Summit__Fast_API import Open_Sec_Summit__Fast_API

fast_api__open_sec_summit = Open_Sec_Summit__Fast_API().setup()
app                  = fast_api__open_sec_summit.app()
run                  = Mangum(app)

if __name__ == "__main__":                              # pragma: no cover
    import uvicorn
    port = get_env('PORT', 8080)
    uvicorn.run(app, host="0.0.0.0", port=port)