from flask_babel import lazy_gettext as _l

CONTENT_TYPE_CHOICES = {
    'pdf': 'application/pdf',
    'xls': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.ms-excel',
    'doc': 'application/word',
    'docx': 'application/msword',
    'ppt': 'application/vnd.ms-powerpoint',
    'pptx': 'application/vnd.ms-powerpoint',
    'jpg': 'image/jpg',
    'jpeg': 'image/jpg',
    'gif': 'image/gif',
    'png': 'image/png',
    'rar': 'application/octet-stream',
    'zip': 'application/zip',
}

DEFAULT_NONE = None
ZERO_VALUE = 0
DEFAULT_PAGE = 1
LIMIT = 6
PER_PAGE = 6
MAX_SIZE_IMG_PROFILE = 1 * 1024 * 1024
DEFAULT_TEXT_NOT_UPDATED = _l('Chưa cập nhật')
LIMIT_MAIN_BANNER = 4
LIMIT_SUB_BANNER = 2
DEFAULT_USER_PASSWORD = '123abctechsolution@_2022'
DEFAULT_IMAGE = 'images/default_img.jpg'
URL_VIEW_SERVE_IMAGE = 'admin.serve_blog_image'

#  ERROR STATUS

SUCCESS_CODE = 200
FORBIDDEN_ERROR_CODE = 403
NOT_FOUND_CODE = 404
BAD_REQUEST_CODE = 400
SERVER_ERROR_CODE = 500
ALREADY_FOUND_CODE = 302
MAIN_BANNER_IMAGE_UPLOAD_FOLDER = "main_banner"
SUB_BANNER_IMAGE_UPLOAD_FOLDER = "sub_banner"


