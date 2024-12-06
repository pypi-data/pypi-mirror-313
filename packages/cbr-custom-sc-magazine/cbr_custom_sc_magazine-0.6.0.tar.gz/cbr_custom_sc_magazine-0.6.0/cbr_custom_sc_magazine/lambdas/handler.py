from mangum                                                            import Mangum
from osbot_utils.utils.Env                                             import get_env
from cbr_custom_sc_magazine.sc_magazine.fast_api.SC_Magazine__Fast_API import SC_Magazine__Fast_API

fast_api__sc_magazine = SC_Magazine__Fast_API().setup()
app                   = fast_api__sc_magazine.app()
run                   = Mangum(app)

if __name__ == "__main__":                              # pragma: no cover
    import uvicorn
    port = get_env('PORT', 8080)
    uvicorn.run(app, host="0.0.0.0", port=port)