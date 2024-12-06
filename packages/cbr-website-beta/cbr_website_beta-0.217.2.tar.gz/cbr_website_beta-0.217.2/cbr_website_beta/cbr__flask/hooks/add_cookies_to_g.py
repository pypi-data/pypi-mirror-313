from flask                                       import request, g
from cbr_shared.cbr_sites.CBR__Shared__Constants import COOKIE_NAME__CBR__SESSION_ID__ACTIVE

MAX_COOKIE_SIZE = 25

#@xray_trace("add_cookies_to_g")
def add_cookies_to_g():
    cookie_dict = {}
    session_id = None
    for key, value in request.cookies.items():
        if len(value) > MAX_COOKIE_SIZE:
            formatted_value = f"{value[:MAX_COOKIE_SIZE]} - size: {len(value)}"
        else:
            formatted_value = value

        cookie_dict[key] = formatted_value
        if key == COOKIE_NAME__CBR__SESSION_ID__ACTIVE:
            session_id = value

    g.cookies    = cookie_dict
    g.session_id = session_id