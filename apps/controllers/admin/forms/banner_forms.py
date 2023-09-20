from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Optional, ValidationError, Length
from apps.constant.common import ZERO_VALUE
from apps.controllers.admin.forms.common_forms import CommonImageForm
from apps.constant.forms import (
    ERROR_EMPTY_MESSAGE,
    FILE_NAME_ALREADY_EXIST, MAX_SIZE_IMAGE, ERROR_MAX_IMAGE_MESSAGE, ALLOW_IMAGE_EXTENSION,
    ERROR_EXTENSION_IMAGE_MESSAGE, MAX_LENGTH_TEXT, MAX_LENGTH_TEXT_MESSAGE, ERROR_BANNER_TITLE_ALREADY_EXIST,
)
from apps.utils.shared import get_size


class AddBannerForm(FlaskForm):
    title = StringField('Tiêu đề', [DataRequired(ERROR_EMPTY_MESSAGE)])


class EditBannerForm(FlaskForm):
    title = StringField('Tiêu đề', [DataRequired(ERROR_EMPTY_MESSAGE)])
    description = TextAreaField('Mô tả', [Optional(), Length(max=MAX_LENGTH_TEXT, message=MAX_LENGTH_TEXT_MESSAGE)])
    published = BooleanField('Cho phép đăng banner lên trang chủ?', validators=[Optional()], default=False)

    def __init__(self, banner, *args, **kwargs):
        self.banner = banner
        super(EditBannerForm, self).__init__(*args, **kwargs)

    def validate_title(self, field):
        if field.data and field.data != self.banner.title and\
                self.banner.__class__.objects(title=field.data).count() > ZERO_VALUE:
            raise ValidationError(ERROR_BANNER_TITLE_ALREADY_EXIST)


class AddBannerImage(CommonImageForm):

    def validate_file(self, field):
        filename = secure_filename(field.data.filename)
        if filename:
            if BannerMedia.objects(original_filename=field.data.filename).first():
                self.file.errors.append(FILE_NAME_ALREADY_EXIST)
            if get_size(field.data) > MAX_SIZE_IMAGE:
                self.file.errors.append(ERROR_MAX_IMAGE_MESSAGE)
            if not ('.' in filename and filename.rsplit('.', 1)[1] in ALLOW_IMAGE_EXTENSION):
                self.file.errors.append(ERROR_EXTENSION_IMAGE_MESSAGE)
        if self.file.errors:
            return False


class EditBannerImage(CommonImageForm):

    def __init__(self, banner_image, *args, **kwargs):
        self.banner_image = banner_image
        super(EditBannerImage, self).__init__(*args, **kwargs)

    def validate_file(self, field):
        filename = secure_filename(field.data.filename)
        if filename:
            if field.data.filename != self.banner_image.original_filename \
                    and BannerMedia.objects(original_filename=field.data.filename).first():
                self.file.errors.append(FILE_NAME_ALREADY_EXIST)
            if get_size(field.data) > MAX_SIZE_IMAGE:
                self.file.errors.append(ERROR_MAX_IMAGE_MESSAGE)
            if not ('.' in filename and filename.rsplit('.', 1)[1] in ALLOW_IMAGE_EXTENSION):
                self.file.errors.append(ERROR_EXTENSION_IMAGE_MESSAGE)
        if self.file.errors:
            return False