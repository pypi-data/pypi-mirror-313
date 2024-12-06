from cbr_website_beta.apps.chat                                 import blueprint
from cbr_website_beta.cbr__flask.decorators.allow_annonymous    import allow_anonymous, admin_only

@blueprint.route('/stats')
@admin_only
def chat_stats():
    from flask import render_template

    from cbr_athena.llms.storage.CBR__Chats__Analysis import CBR__Chats__Analysis
    title         = "Chat - Stats"
    content_view  = '/llms/chats/stats.html'
    template_name = '/pages/page_with_view.html'


    chats_stats = CBR__Chats__Analysis().chats_stats()

    return render_template( template_name_or_list = template_name ,
                            content_view          = content_view  ,
                            title                 = title         ,
                            stats                 = chats_stats   )

@blueprint.route('/history')
@admin_only
def chat_history():
    from flask import render_template

    from cbr_athena.llms.storage.CBR__Chats_Storage__Local import CBR__Chats_Storage__Local
    title         = "Chat - History"
    content_view  = '/llms/chats/history.html'
    template_name = '/pages/page_with_view.html'


    cbr_chats_storage_local = CBR__Chats_Storage__Local().setup()
    #chat_ids = cbr_chats_storage_local.chats_ids()
    chats_latest = cbr_chats_storage_local.chats_latest()

    return render_template( template_name_or_list = template_name ,
                            content_view          = content_view  ,
                            title                 = title         ,
                            chats                 = chats_latest  )

@blueprint.route('/view/<path:path>/image')
@allow_anonymous
def chat_view__from_chat_id__image(path=None):
    from osbot_utils.utils.Http                           import GET_json
    from osbot_utils.utils.Misc                           import base64_to_bytes
    from cbr_website_beta.cbr__flask.utils.current_server import current_server


    from flask import Response
    url_for_screenshot = f'{current_server()}web/chat/view/{path}'                 # todo: add path validation
    screenshot_data_url = f'https://serverless-flows.dev.aws.cyber-boardroom.com/browser/url-screenshot?url={url_for_screenshot}'

    screenshot_data     = GET_json(screenshot_data_url)
    screenshot_bytes    = base64_to_bytes(screenshot_data.get('screenshot_base64'))

    return Response(
        screenshot_bytes,
        content_type='image/png'
    )


@blueprint.route('/view/<path:path>/pdf')
@allow_anonymous
def chat_view__from_chat_id__pdf(path=None):
    from osbot_utils.utils.Misc                           import base64_to_bytes
    from osbot_utils.utils.Http                           import GET_json
    from cbr_website_beta.cbr__flask.utils.current_server import current_server


    from flask import Response
    target_server = current_server()
    if target_server == "http://localhost:5001/":
        target_server = "https://dev.cyber-boardroom.com/"
    url_for_screenshot = f'{target_server}web/chat/view/{path}'                 # todo: add path validation
    pdf_data_url = f'https://serverless-flows.dev.aws.cyber-boardroom.com/browser/url-pdf?url={url_for_screenshot}'
    pdf_data     = GET_json(pdf_data_url)
    pdf_base_64  = pdf_data.get('pdf_base64')
    if not pdf_base_64:
        return f"failed to get pdf data from {pdf_data_url}"

    pdf_bytes    = base64_to_bytes(pdf_base_64)

    return Response(
        pdf_bytes,
        content_type='application/pdf',
        headers={"Content-Disposition": "inline; filename=document.pdf"}
    )

@blueprint.route('/view/<path:path>')
@allow_anonymous
def chat_view__from_chat_id(path=None):
    from flask                                        import render_template
    from cbr_shared.config.Server_Config__CBR_Website import server_config__cbr_website

    title             = "Chat - View past chat"
    content_view      = '/llms/chat_with_llms/view_chat_from_chat_id.html'
    template_name     = '/pages/page_with_view.html'
    url_athena        = server_config__cbr_website.target_athena_url()  + '/llms/chat/completion'
    url_chat_data     = server_config__cbr_website.target_athena_url()  + f'/llms/chat/view?chat_id={path}'
    platform = "Groq (Free)"
    provider = "1. Meta"
    model    = "llama3-70b-8192"

    return render_template( template_name_or_list = template_name ,
                            content_view          = content_view  ,
                            title                 = title         ,
                            url_athena            = url_athena    ,
                            platform              = platform      ,
                            provider              = provider      ,
                            model                 = model         ,
                            chat_id               = path          ,
                            url_chat_data         = url_chat_data )