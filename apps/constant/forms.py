from flask_babel import lazy_gettext as _l

ERROR_EMPTY_MESSAGE = _l('Giá trị không được phép rỗng!')
ERROR_NOT_VALID_EMAIL = _l('Email không hợp lệ!')
ERROR_NOT_VALID_VALUE = _l('Giá trị không hợp lệ!')
ERROR_MAX_IMAGE_MESSAGE = _l('Dung lượng file vượt giới hạn cho phép (5MB)')
ERROR_EXTENSION_IMAGE_MESSAGE = _l('Chỉ chọn tập tin hình có định dạng: (.jpg, .png, .jpeg, .gif, .webp)')
EMAIL_ALREADY_EXIT = _l('Email đã tồn tại!')
ERROR_MAX_FILE_MESSAGE = _l('Dung lượng file vượt giới hạn cho phép (10MB)')
MAX_SIZE_IMAGE = 5242880  # 5 Megabytes
MAX_SIZE_FILE = 10485760  # 10 Megabytes
ALLOWED_EXTENSIONS = {'xlsx', 'doc', 'docx', 'ppt', 'pptx', 'csv', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'rar', 'zip'}
ERROR_EXTENSION_MESSAGE = _l('Chỉ chọn tập tin có định dạng: (.xlsx, .doc, .docx, .ppt, .pptx, .csv, .txt, .pdf, .png, .jpg, .jpeg, .gif, .rar, .zip)')
ALLOW_IMAGE_EXTENSION = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
VIEW_INLINE_PDF_EXTENSION = {'pdf'}
ALLOW_VIEW_INLINE_EXTENSION = ALLOW_IMAGE_EXTENSION.union(VIEW_INLINE_PDF_EXTENSION)
CATEGORY_NAME_CODE_ALREADY_EXIST = _l('Tên và mã danh mục đã tồn tại!')
DEFAULT_OPTION_CHOICES = [('', 'Chọn')]
DEFAULT_OPTION_CHOICES_MULTIPLE = [('', '')]
FILE_NAME_ALREADY_EXIST = _l('Tên tập tin đã tồn tại!')
INVALID_COUPON_CODE = _l('Mã khuyến mãi không hợp lệ!')
MAX_LENGTH_TEXT = 200
MAX_LENGTH_TEXT_MESSAGE = _l('Không nhiều hơn 200 ký tự!')
ERROR_NOT_VALID_PHONE = _l('Số di động không hợp lệ')
ERROR_BANNER_TITLE_ALREADY_EXIST = _l('Tiêu đề banner đã tồn tại!')
ERROR_NAME_ALREADY_EXIST = _l('Tên đã tồn tại!')
ERROR_CODE_ALREADY_EXIST = _l('Mã định danh đã tồn tại!')
ERROR_ROLE_NAME_ALREADY_EXIST = _l('Tên vai trò đã tồn tại!')
MAX_LENGTH = 500
MAX_LENGTH_MESSAGE = _l('Không nhiều hơn 500 ký tự!')
BLOG_TITLE_ALREADY_EXIST = _l('Tên bài viết đã tồn tại!')
FILE_TITLE_ALREADY_EXIST = _l('Tên hồ sơ đã tồn tại!')
CATEGORY_NAME_ALREADY_EXIST = _l('Tên danh mục đã tồn tại!')
INVALID_URL_MESSAGE = _l('Đường dẫn không hợp lệ!')

