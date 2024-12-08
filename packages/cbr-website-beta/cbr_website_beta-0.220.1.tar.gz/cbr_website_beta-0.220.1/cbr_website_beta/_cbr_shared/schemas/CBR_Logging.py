from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self

# todo : refactor this out of this code since in the future this will need to be a REST call to ODIN
#        who will be responsible for capturing the logs

class CBR_Logging(Kwargs_To_Self):
    # auto populated
    id          : str           # to be set by Dynamo_DB__Table
    timestamp   : int           # to be set by the request
    # indexes
    date        : str   = 'NA'
    level       : str   = 'NA'
    message     : str   = 'NA'
    source      : str   = 'NA'
    topic       : str   = 'NA'

    # other
    city        : str   = 'NA'
    country     : str   = 'NA'
    user_id     : str   = 'NA'
    extra_data  : dict
