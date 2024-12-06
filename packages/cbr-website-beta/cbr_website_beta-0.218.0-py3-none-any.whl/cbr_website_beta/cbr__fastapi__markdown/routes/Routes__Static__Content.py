from cbr_website_beta.content.CBR__Content__Static  import CBR__Content__Static
from osbot_fast_api.api.Fast_API_Routes             import Fast_API_Routes
from starlette.responses                            import FileResponse

ROUTE_PATH__STATIC_CONTENT  = 'static_content'
EXPECTED_SITE_INFO_ROUTES   = ['/extensions']
FILE_NAME__DB__CBR_CONTENTS = 'db_cbr_static_files.sqlite'
PATH__DB__CBR_CONTENTS      = f'/tmp/{FILE_NAME__DB__CBR_CONTENTS}'

class Routes__Static__Content(Fast_API_Routes):
    cbr_content_static : CBR__Content__Static
    tag                : str                  = ROUTE_PATH__STATIC_CONTENT

    def content_files(self):
        return self.cbr_content_static.content_files__md()

    def content_file(self, path='/'):
        return self.cbr_content_static.file_contents(path)

    def data_file(self, path):
        return self.cbr_content_static.file_data(path)

    def content_db(self):
        db_contents = self.cbr_content_static.all_contents__in_sqlite_db()
        db_file     = db_contents.save_to(PATH__DB__CBR_CONTENTS)
        return FileResponse(db_file, media_type='application/octet-stream', filename=FILE_NAME__DB__CBR_CONTENTS)

    def setup_routes(self):
        self.add_route_get(self.content_db   )
        self.add_route_get(self.content_file )
        self.add_route_get(self.content_files)
        self.add_route_get(self.data_file    )
