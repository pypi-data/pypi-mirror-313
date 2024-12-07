from cbr_website_beta.aws.s3.S3                         import S3
from osbot_aws.AWS_Config                               import aws_config
from osbot_utils.base_classes.Kwargs_To_Self            import Kwargs_To_Self
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self
from osbot_utils.decorators.methods.remove_return_value import remove_return_value
from osbot_utils.helpers.html.Tag__Base                 import Tag__Base
from osbot_utils.helpers.html.Tag__Div                  import Tag__Div
from osbot_utils.helpers.html.Tag__H                    import Tag__H
from osbot_utils.helpers.html.Tag__HR                   import Tag__HR
from osbot_utils.helpers.html.Tag__Html                 import Tag__Html
from osbot_utils.utils.Files                            import file_name
from osbot_utils.utils.Misc                             import date_now

BUCKET_NAME__CBR_STATIC_FILES       = '{account_id}-cbr'
S3_FOLDER__DOCUMENTATION_IMAGES     = 'cbr_website_docs'
S3_PATH__DOCUMENTATION_IMAGES       = f'cbr_website_static/{S3_FOLDER__DOCUMENTATION_IMAGES}/'
S3_FILE_NAME__DOCUMENTATION_IMAGES  = f'docs_images.html'
S3_KEY__DOCUMENTATION_IMAGES        = f'{S3_PATH__DOCUMENTATION_IMAGES}{S3_FILE_NAME__DOCUMENTATION_IMAGES}'
#URL_CBR_STATIC_FILES               = 'https://static.thecyberboardroom.com'                   # this one has some caching issues (due to cloudfront)
URL_CBR_STATIC_FILES                = "https://470426667096-cbr.s3.eu-west-2.amazonaws.com/"
URL_FILE__DOCUMENTATION_IMAGES      = f'{URL_CBR_STATIC_FILES}/{S3_PATH__DOCUMENTATION_IMAGES}/{S3_FILE_NAME__DOCUMENTATION_IMAGES}'

class CBR_Documentation_In_S3(Kwargs_To_Self):
    account_id  : str
    bucket_name : str
    folder_name : str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_id  = aws_config.account_id()
        self.bucket_name = BUCKET_NAME__CBR_STATIC_FILES.format(account_id=self.account_id)
        self.folder_name = S3_PATH__DOCUMENTATION_IMAGES

    @cache_on_self
    def s3(self):
        return S3()

    def create_html_for_page_with_images(self):

        images_names    = self.images_files_names()
        title           = 'Images from Unit Test'
        sub_title       = f'created on {date_now()}'
        row_elements    = self.create_html__row_elements(images_names)
        html_tag        = Tag__Html()
        head_tag        = html_tag.head
        div_container   = Tag__Div(tag_classes=['container-fluid', 'my-5'])
        hr              = Tag__HR()
        div_subtitle    = Tag__Div(tag_classes=['badge', 'bg-dark'], inner_html=sub_title)
        h_title         = Tag__H(1, title)
        div_row         = Tag__Div(tag_classes=['row'], elements=row_elements)

        div_container.append(h_title,
                             div_subtitle,
                             hr,
                             div_row)
        html_tag.body.append(div_container)
        head_tag.add_css_bootstrap()
        head_tag.title = title
        return html_tag

    def create_html__row_elements(self, images_names):
        row_elements = []
        for image_name in images_names:
            image_url   = f'{URL_CBR_STATIC_FILES}{S3_PATH__DOCUMENTATION_IMAGES}{image_name}'
            image_title = image_name.replace('_', ' ').replace('.png', '')
            div_image   = Tag__Div(tag_classes=['col', 'col-md-3', 'text-center'])
            div_badge   = Tag__Div(tag_classes=['fw-bold'],inner_html=image_title)
            #hr          = Tag__HR()
            img         = Tag__Base(tag_name="img", tag_classes=['base64-image', 'img-fluid'])
            img.attributes['src'  ] = image_url
            img.attributes['style'] = 'border:1px solid black; margin:10px'
            div_image.append(div_badge,
                             img,
                             #hr,
                             #div_text_title, div_text_value,
                             #div_negative_title, div_negative_value,
                             #div_comments_title, div_comments_value)
                             )
            row_elements.append(div_image)
        return row_elements

    def s3_create_html_page_for_images(self):
        html_tag               = self.create_html_for_page_with_images()
        html                   = html_tag.render()
        kwargs__s3_file_create = { 'file_contents': html,
                                   'bucket'       : self.bucket_name             ,
                                   'key'          : S3_KEY__DOCUMENTATION_IMAGES }
        kwargs__s3_content_type = {'bucket'       : self.bucket_name             ,
                                   'key'          : S3_KEY__DOCUMENTATION_IMAGES ,
                                   'metadata'     : {}                           ,
                                   'content_type': 'text/html; charset=utf-8'                   }
        if self.s3().file_create_from_string  (**kwargs__s3_file_create):
            self.s3().file_content_type_update(**kwargs__s3_content_type)
            return URL_FILE__DOCUMENTATION_IMAGES

    @remove_return_value('ResponseMetadata')
    def s3_info_for_html_file(self):
        return self.s3().file_details(bucket=self.bucket_name,key=S3_KEY__DOCUMENTATION_IMAGES)

    def images_files(self):
        return self.s3().find_files(self.bucket_name, prefix=self.folder_name, filter=".png")

    def images_files_names(self):
        files_names =[]
        for image_file in self.images_files():
            files_names.append(file_name(image_file, check_if_exists=False))
        return sorted(files_names)


