from osbot_utils.utils.Objects import obj_data


class Obj_Data:

    filter_name = 'obj_data'

    def __init__(self, app):
        app.jinja_env.filters[self.filter_name] = self.obj_data_filter # todo: find a better way to register these filters

    def obj_data_filter(self,data):
        return obj_data(data)