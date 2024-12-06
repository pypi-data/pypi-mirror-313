
from cbr_shared.schemas.data_models.Model__User__Profile  import Model__User__Profile

EXPECTED_ROUTES__LLMS = []
INTRO_TO_USER_DATA     = "We have asked the user to provide some information and included below is the data provided, please customise the answers as much as possible to these user preferences:\n"

# todo: refactor this into a separate file and class
def user_data_for_prompt():
    user_profile = current_user_data()                         # todo: needs fixing to reflect new Model__User__Profile_Data
    if not user_profile:
        return ""

    lines_of_data = [INTRO_TO_USER_DATA]


    for key,value in user_profile.json().items():               # Format the data into a readable list, aligned in columns
        if value:
            line = f"{key:<{30 + 2}}: {value}"
            lines_of_data.append(line)

    user_data = "\n".join(lines_of_data)                        # Join the lines into a single string with newline separation
    return user_data


# todo: this code needs refactoring, specially the bucket creation code below
def current_user_data() -> Model__User__Profile:
    from flask import g
    from cbr_shared.cbr_sites.CBR__Shared_Objects import cbr_shared_objects
    from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website

    if server_config__cbr_website.login_disabled():
        return None
    user_data = g.user_data
    if user_data:
        user_id = user_data.user_id                                     # todo: refactor this logic out of this function
        db_users = cbr_shared_objects.db_users()
        db_user  = db_users.db_user(user_id)
        if db_user.exists() is False:                                   # create user if needed
            print(f"Creating user: {user_id}")
            db_user.create()
        return db_user.user_profile()
    return None





