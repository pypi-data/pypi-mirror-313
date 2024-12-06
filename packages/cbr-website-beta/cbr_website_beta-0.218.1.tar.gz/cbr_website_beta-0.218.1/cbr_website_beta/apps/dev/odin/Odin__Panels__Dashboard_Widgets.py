# from flask import render_template
#
# from cbr_website_beta.aws.cloudwatch.Cloud_Watch_Metrics import Cloud_Watch_Metrics
# from osbot_utils.utils.Misc import list_set, bytes_to_base64
#
# TCB_DASHBOARD_NAME   = 'TCB-Widgets'        # todo: refactor into separate class
#
# class Odin__Panels__Dashboard_Widgets:
#
#     def exposed_methods(self):                                                  # todo: find a better name for this method and move into base class
#         return { 'dashboard_metrics': self.dashboard_metrics,
#                  'widget_screenshot': self.widget_screenshot}
#
#     def dashboard_metrics(self):
#         return render_template(**self.dashboard_metrics__render_kwargs())
#
#     def dashboard_metrics__render_kwargs(self):
#         cloud_watch_metrics = Cloud_Watch_Metrics()
#
#         dashboards_metrics = cloud_watch_metrics.dashboard_widgets(TCB_DASHBOARD_NAME)
#
#         return { "dashboards_metrics"    : dashboards_metrics                      ,
#                  "template_name_or_list" : "dev/cloudwatch/dashboard-metrics.html" ,
#                  "title"                 : "Dashboard - Metrics"                   }
#
#     def widget_screenshot(self, widget_name, start="-PT2H", end="P0D"):
#         cloud_watch_metrics = Cloud_Watch_Metrics()
#         image_png = cloud_watch_metrics.widget_screenshot(TCB_DASHBOARD_NAME, widget_name, start=start, end=end)
#         return image_png
#         #image_base64 = bytes_to_base64(image_png)
#         #return image_base64
#
#
# #
# #
# # def test_dashboard_metrics(self):
# #     dashboard_metrics = self.logs_views.dashboard_metrics()
# #     print(dashboard_metrics)
# #
# #
#
