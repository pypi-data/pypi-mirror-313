import os
import typer

from cbr_website_beta.cbr__fastapi.CBR__Fast_API    import CBR__Fast_API
from osbot_fast_api.cli.Fast_API__CLI               import Fast_API__CLI
from osbot_fast_api.utils.Fast_API_Server           import Fast_API_Server



class CBR_Fast_API__CLI(Fast_API__CLI):
    def __init__(self):
        self.fast_api        = CBR__Fast_API().setup()
        #self.fast_api_server = Fast_API_Server(app=self.fast_api.app())
        super().__init__()

if __name__ == "__main__":
    cli = CBR_Fast_API__CLI().setup()
    cli.run()
