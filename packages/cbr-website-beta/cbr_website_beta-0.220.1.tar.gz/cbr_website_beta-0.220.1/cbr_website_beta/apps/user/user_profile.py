from flask                                               import request, redirect, render_template, g
from cbr_shared.cbr_backend.users.S3_DB__Users           import S3_DB__Users
from cbr_shared.schemas.data_models.Model__User__Profile import Model__User__Profile
from cbr_website_beta.cbr__flask.filters.Current_User    import g_user_data

def render_page__login_required(title='Login Required'):
    template_name = '/pages/page_with_view.html'
    title         = title
    content_view  = 'includes/login_required.html'
    return render_template(template_name, content_view=content_view, title=title)

def user_profile():
    db_users      = S3_DB__Users()
    user_data     = g_user_data()

    if user_data is None:
        return render_page__login_required('User Profile')

    user_id      = user_data.user_id
    db_user      = db_users.db_user(user_id)

    profile_data = db_user.user_profile().json()

    if request.method == 'POST':
        form_data    = request.form.to_dict()                                   # get the form data
        profile_data = Model__User__Profile.from_json(form_data)                # Convert to Model__User__Profile_Data
        db_user.user_profile__update(profile_data)                              # update the user profile
        user_profile_path = "/web/user/profile"                                 # redirect to the user profile page
        return redirect(user_profile_path)

    template_name = '/user/profile.html'
    form_fields = get_form_fields(profile_data)

    return render_template(template_name, user_id=user_id, profile_data=profile_data, form_fields=form_fields)

def get_form_fields(profile_data):
    form_fields        = []
    default_html_class = 'form-control ps-0 form-control-line'
    def add_fields(field_names, field_type, html_class=default_html_class):
        for field_name in field_names:
            field_value       = profile_data.get(field_name,'')
            field_name_for_ui = field_name.replace('_',' ').capitalize()
            field_data        = { 'name'       : field_name,
                                  'name_for_ui': field_name_for_ui,
                                  'type'       : field_type       ,
                                  'value'      : field_value      ,
                                  'html_class' : html_class       }
            form_fields.append(field_data)
    add_fields(['first_name', 'last_name', 'role', 'organisation', 'sector', 'size_of_organisation', 'country', 'linkedin'], field_type='text')
    add_fields(['additional_system_prompt'                                                                                ], field_type='textarea')
    return form_fields