# import os
#
# if __name__ == "__main__":
#     import uvicorn
#     port = int(os.environ.get("PORT", 5001)) #
#     uvicorn.run("cbr_website_beta.fast_api_main:app", host="0.0.0.0", port=port, reload=True, force_exit=True)

import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))

    config = uvicorn.Config(app    = "cbr_website_beta.fast_api_main:app",
                            host   = "0.0.0.0"                           ,
                            port   = port                                ,
                            reload = True                                )
    server = uvicorn.Server(config)
    server.run()