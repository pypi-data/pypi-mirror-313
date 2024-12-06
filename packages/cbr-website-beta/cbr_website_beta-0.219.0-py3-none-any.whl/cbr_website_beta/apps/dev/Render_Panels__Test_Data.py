import inspect

from cbr_website_beta.apps.dev.Render_Panels import Render_Panels


class Render_Panels__Test_Data:

    def __init__(self):
        self.render_panels = Render_Panels()

    def available_classes_and_methods(self):
        result = {}
        for class_name, target_class in self.render_panels.target_classes.items():
            if hasattr(target_class, 'exposed_methods'):
                class_mappings = {}
                for method_name, method in target_class.exposed_methods().items():
                    # Retrieve the signature of the method
                    sig = inspect.signature(method)
                    method_info = {}
                    for param in sig.parameters.values():
                        # Check if parameter has a default value
                        if param.default is param.empty:
                            default_value = ''
                        else:
                            default_value = param.default or ''
                        # Store the parameter name and its default value
                        method_info[param.name] = default_value
                    # Map method name to its parameters and their default values
                    class_mappings[method_name] = method_info

                result[class_name] = class_mappings
        return result