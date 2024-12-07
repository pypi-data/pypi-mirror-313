from cbr_website_beta.cbr__fastapi.CBR__Fast_API import cbr_fast_api

def reset_flask_cache():
    flask     = cbr_fast_api.cbr__flask()
    flask_app = flask.app()
    flask_app.jinja_env.cache.clear()