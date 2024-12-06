

def register_processors(app):
    from cbr_website_beta.cbr__flask.processors.available_models import available_models
    from cbr_website_beta.cbr__flask.processors.date_time_now    import date_time_now
    from cbr_website_beta.cbr__flask.processors.menu_links       import menu_links


    @app.context_processor
    def register__date_time_now():
        return {'date_time_now': date_time_now()}

    @app.context_processor
    def register__menu_links():
        return { 'menu_links' : menu_links }

    @app.context_processor
    def register__available_models():
        return {'available_models': available_models}