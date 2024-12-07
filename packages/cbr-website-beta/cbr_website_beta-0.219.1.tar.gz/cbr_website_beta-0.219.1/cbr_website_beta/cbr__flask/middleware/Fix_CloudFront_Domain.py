# todo: see if we still need this (specially now that the main redirect is done by CBR__Fast_API)

# this was added because Flask was picking up the domain from the Lambda URL (which is not the domain we want)
# IMPORTANT: this relies on a manually set Cloudfront-Domain header that needs to be added in CloudFront (that indicates the domain we want to use)
#            without this, for example, the redirects use the Lambda URL and amongst other things, break cognito auth flow

class Fix_CloudFront_Domain(object):
    def __init__(self, app):
        self.app = app

    #@trace_calls(include=['cbr_website_beta'], show_class=True)
    def __call__(self, environ, start_response):
        cloudfront_domain = environ.get('HTTP_CLOUDFRONT_DOMAIN', None)
        if cloudfront_domain:
            environ['HTTP_HOST'] = cloudfront_domain
        return self.app(environ, start_response)