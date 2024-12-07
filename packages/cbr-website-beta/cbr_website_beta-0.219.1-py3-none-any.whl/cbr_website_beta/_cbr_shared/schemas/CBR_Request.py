from decimal import Decimal

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


class CBR_Request(Kwargs_To_Self):
    # auto populated
    id          : str           # to be set by Dynamo_DB__Table
    timestamp   : int           # to be set by the request
    # indexes
    date        : str = 'NA'
    ip_address  : str = 'NA'
    host        : str = 'NA'
    level       : str = 'NA'
    method      : str = 'NA'
    path        : str = 'NA'
    referer     : str = 'NA'
    req_id      : str = 'NA'
    session_id  : str = 'NA'
    status_code : str = 'NA'
    source      : str = 'NA'
    user        : str = 'NA'
    user_role   : str = 'NA'
    user_status : str = 'NA'

    # other non-indexed data
    duration    : Decimal
    headers     : dict
    query       : dict

