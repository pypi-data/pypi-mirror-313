import types

from cbr_website_beta.apps.dev.odin.Odin__Panels__Debug             import Odin__Panels__Debug
from cbr_website_beta.apps.dev.odin.Odin__Panels__Logs              import Odin__Panels__Logs
from cbr_website_beta.apps.dev.odin.Odin__Panels__Real_Time         import Odin__Panels__Real_Time
from cbr_website_beta.apps.dev.odin.Odin__Panels__Session_Management import Odin__Panels__Session_Management


# todo: add documentation and threat model for this class, since it can potentiall be quite an dangerous one
#       since it allows to call methods from classes that are in the target_classes dictionary
#       this danger is mitigated by the fact that the target_classes and target methods are all hardcoded
# todo: add explict RBAC checks and demands for the methods that are being called

class Render_Panels:

    def __init__(self):
        self.target_classes = self.get_target_classes()

    def get_target_classes(self):
        target_classes = { 'odin_debug'             : Odin__Panels__Debug             () ,
                           'odin_session_management': Odin__Panels__Session_Management() ,
                           'odin_logs'              : Odin__Panels__Logs              () ,
                           'odin_real_time'         : Odin__Panels__Real_Time         () }
        return target_classes

    def resolve_target_method(self, class_name, method_name):
        target_class = self.target_classes.get(class_name)
        if target_class is None:
            return {'status': 'error', 'data': f'no target class found for: {class_name}'}

        if hasattr(target_class, 'exposed_methods') is False:
            return {'status': 'error', 'data': f'no exposed_methods found for: {class_name}'}
        exposed_methods = target_class.exposed_methods()
        if method_name not in exposed_methods:
            return {'status': 'error', 'data': f'no method found for: {method_name} in {class_name}'}
        target_method = exposed_methods.get(method_name)
        return  {'status': 'ok', 'target_method': target_method}


    def render_panel(self, class_name, method_name, **kwargs):
        resolved_target_method = self.resolve_target_method(class_name, method_name)
        if resolved_target_method.get('status') == 'error':
            return resolved_target_method

        target_method: types.MethodType | None = resolved_target_method.get('target_method')

        try:
            return_value = target_method( **kwargs)
        except Exception as error:
            return {'status': 'error', 'data': f'Error: {error}'}
        if type(return_value) is bytes:
            return return_value
        return {'status': 'ok', 'return_value': return_value}
