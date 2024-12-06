from cbr_shared.config.Server_Config__CBR_Website               import server_config__cbr_website
from cbr_website_beta.utils.health_checks.CBR__Health_Checks    import cbr_health_checks
from osbot_fast_api.api.Fast_API_Routes                         import Fast_API_Routes
#from osbot_fast_api.api.Fast_API__Thread__Trace_Request         import Fast_API__Thread__Trace_Request, fast_api_thread_trace_request

ROUTE_PATH__SITE_INFO     = 'site_info'
EXPECTED_SITE_INFO_ROUTES = ['/cbr-config-active', '/cbr-site-info', '/health-checks', '/attack-surface']


class CBR__Site_Info__Routes(Fast_API_Routes):

    tag : str = ROUTE_PATH__SITE_INFO

    def cbr_config_active(self):
        return server_config__cbr_website.cbr_config_active().json()

    def cbr_site_info(self):
            return server_config__cbr_website.cbr_site_info__data(reload_cache=True)

    def health_checks(self):
        return cbr_health_checks.execute_health_checks()

    def attack_surface(self):
        from cbr_website_beta.cbr__fastapi.CBR__Fast_API import cbr_fast_api
        return cbr_fast_api.attack_surface()

    def setup_routes(self):
        self.add_route_get(self.cbr_config_active)
        self.add_route_get(self.cbr_site_info    )
        self.add_route_get(self.health_checks    )
        self.add_route_get(self.attack_surface    )


