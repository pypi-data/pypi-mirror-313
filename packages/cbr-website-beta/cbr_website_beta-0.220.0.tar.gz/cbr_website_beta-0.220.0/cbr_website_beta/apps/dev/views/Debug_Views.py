from flask import render_template, g
from cbr_website_beta.cbr__flask.filters.Current_User import Current_User


class Debug_Views:

    def client_details(self):
        return render_template(**self.client_details__data())

    def request_details(self):
        return render_template(**self.request_details__data())

    def client_details__data(self):
        user_data = getattr(g, 'user_data', {})
        return { "template_name_or_list" : "dev/client_details.html",
                 "title"                 : "Client Details"         ,
                 "user_data"             : user_data                }

    def request_details__data(self):
        return {"template_name_or_list": "dev/request_details.html" ,
                "title"                : "Request Details"          }
