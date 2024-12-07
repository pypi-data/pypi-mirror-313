from cbr_website_beta.utils.health_checks.Health_Checks__CBR__Internal_Data     import Health_Checks__CBR__Internal_Data
from cbr_website_beta.utils.health_checks.Health_Checks__Http__External_Sites   import Health_Checks__Http__External_Sites
from osbot_utils.context_managers.capture_duration                              import capture_duration
from osbot_utils.base_classes.Type_Safe                                         import Type_Safe
from osbot_utils.utils.Objects                                                  import class_functions
from osbot_utils.utils.Status                                                   import status_ok, status_error



class CBR__Health_Checks(Type_Safe):

    def execute_health_check(self, function):
        with capture_duration() as duration:
            try:
                return_value = function()
                result       = status_ok(data=return_value)
            except Exception as error:
                result       = status_error(error=f'{error}')

        result['duration'     ] = duration.seconds
        return result

    def execute_health_checks(self):
        results     = {}
        health_checks  = [ Health_Checks__CBR__Internal_Data  ,
                           Health_Checks__Http__External_Sites]

        for health_check_class in health_checks:
            results[health_check_class.__name__] = self.execute_health_checks__from_class(health_check_class)
        return results

    def execute_health_checks__from_class(self, class_with_health_checks):
        items = {}

        http_perf_functions = class_functions(class_with_health_checks())
        for function_name, function in http_perf_functions.items():
            items[function_name] = self.execute_health_check(function)
        return items


cbr_health_checks = CBR__Health_Checks()