from pydantic import BaseModel


class Create_User_Session(BaseModel):
    user_name     : str
    session_id    : str
    source        : str
    cognito_tokens: dict
