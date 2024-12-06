from pydantic import BaseModel

class Log_Entry(BaseModel):
    # required index field
    message     : str
    # indexes
    level       : str = 'NA'
    source      : str = 'NA'
    topic       : str = 'NA'

    # other
    user_id     : str = 'NA'
    extra_data  : dict = {}

