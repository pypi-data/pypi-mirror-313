from cbr_website_beta.apps.docs                                 import blueprint
from cbr_website_beta.cbr__flask.decorators.allow_annonymous    import allow_anonymous, admin_only


EXPECTED_ROUTES__DOCS = [ '/docs', '/markdown/examples']

@blueprint.route('/markdown/examples')
@allow_anonymous
def markdown_exampes(path='/'):
    from flask import render_template
    from osbot_markdown.markdown.Markdown_Examples import markdown_examples

    content_view  = 'docs/markdown_examples/markdown_examples.html'
    template_name = '/pages/page_with_view.html'
    title         = 'Markdown Examples'
    content       = '# Markdown Examples\n\nChange this content in the left and see the preview in the right'
    md_examples   = markdown_examples.all_examples()
    return render_template(template_name_or_list = template_name ,
                           title                 = title         ,
                           content_view          = content_view  ,
                           path                  = path          ,
                           content               = content       ,
                           markdown_examples     = md_examples   )


@blueprint.route('/markdown/save', methods=['POST'])
@admin_only
#@allow_anonymous
def markdown_save():                                 # todo refactor this from this class into the Render_Panels class
    from flask import request, jsonify
    from cbr_website_beta.content.CBR__Content__Static import cbr_content_static

    if request.is_json:
        try:
            data     = request.get_json()
            path     = data.get('path', '')
            contents = data.get('contents', '')
            if path and contents:
                cbr_content_static.save_file_contents__for__web_page(path, contents)
                return jsonify({'status': 'ok', 'message': 'data saved...'}), 200
            else:
                return jsonify({'status': 'error', 'message': 'no content was provided'}), 501
        except Exception as error:
            return jsonify({'status': 'error', 'message': f'Error: {error}'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Request must be JSON'}), 400


@blueprint.route('/markdown/edit')
@blueprint.route('/markdown/edit/<path:path>')
@admin_only
def markdown_edit(path='/'):
    from flask import render_template
    from cbr_website_beta.content.CBR__Content__Static import cbr_content_static

    content_view  = 'docs/edit.html'
    template_name = '/pages/page_with_view.html'
    title         = 'Edit page'
    if path == '' or path == '/':
        path = 'index'
    content       = cbr_content_static.file_contents__raw__for__web_page(path)

    return render_template(template_name_or_list = template_name,
                           title                 =  title        ,
                           content_view          = content_view  ,
                           path                  = path          ,
                           content               = content       )


@blueprint.route('')
#@blueprint.route('/')                  # this is not working with the route ''
@blueprint.route('/<path:path>')
#@blueprint.route('/<path:path>/')
@allow_anonymous
def show_docs_file(path='/'):
    from cbr_website_beta.content.CBR__Content__Static import cbr_content_static
    from flask import render_template

    content_view  = 'docs/view.html'
    template_name = '/pages/page_with_view.html'
    title         = 'Documentation'
    if path == '' or path == '/':
        path = 'index'
    if path.endswith('/'):
        path += 'index'

    content       = cbr_content_static.file_contents__for__web_page(path)
    base_folder   = cbr_content_static.base_folder                 (path)
    parent_folder = cbr_content_static.parent_folder               (path)
    folders       = cbr_content_static.folders                     (path)
    files         = cbr_content_static.files                       (path)
    return render_template(template_name_or_list = template_name,
                           title                 =  title        ,
                           content_view          = content_view  ,
                           path                  = path          ,
                           content               = content       ,
                           files                 = files         ,
                           folders               = folders       ,
                           base_folder           = base_folder   ,
                           parent_folder         = parent_folder )


