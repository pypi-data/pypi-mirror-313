# from cbr_website_beta.cbr__fastapi.CBR__Fast_API import cbr_fast_api
#
# app  = cbr_fast_api.app()

import sys
import traceback
from fastapi             import FastAPI
from starlette.responses import JSONResponse

app = FastAPI()

try:
    from cbr_website_beta.cbr__fastapi.CBR__Fast_API import cbr_fast_api

    cbr_fast_api.setup()
    app = cbr_fast_api.app()
except Exception as e:
    error_message =  f"Catastrophic ERROR: Failed to initialize the CBR application due to the error: {str(e)}"
    traceback_details = traceback.format_exc()
    print(traceback_details, file=sys.stderr)


    @app.api_route("/{path:path}", methods=["GET"])
    @app.get("/")
    def read_root():
        return JSONResponse(
            content={
                "error": error_message,
                "traceback": traceback_details.splitlines()
            },
            status_code=400
        )
