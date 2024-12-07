def register_hooks(app):
    from cbr_website_beta.cbr__flask.hooks.add_cookies_to_g import add_cookies_to_g
    from cbr_website_beta.cbr__flask.hooks.allow_anonymous import allow_anonymous, admins_only
    from cbr_website_beta.cbr__flask.hooks.populate_variable_g import populate_variable_g

    app.before_request(add_cookies_to_g     )
    app.before_request(populate_variable_g  )
    app.before_request(admins_only          )
    app.before_request(allow_anonymous      )

    #app.after_request (set_test_cookies     )