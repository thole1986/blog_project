from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from wtforms.fields import EmailField
from apps.constant.common import MAX_SIZE_IMG_PROFILE
from apps.utils.shared import get_size
from apps.constant.forms import (
    ERROR_EMPTY_MESSAGE,
    ERROR_NOT_VALID_EMAIL,
    EMAIL_ALREADY_EXIT,
    ERROR_MAX_IMAGE_MESSAGE,
    ALLOW_IMAGE_EXTENSION,
    ERROR_EXTENSION_IMAGE_MESSAGE,
)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(ERROR_EMPTY_MESSAGE),
                                             Email(message=ERROR_NOT_VALID_EMAIL)])
    password = PasswordField('Mật khẩu', validators=[DataRequired(ERROR_EMPTY_MESSAGE)])


class SignUpForm(FlaskForm):
    name = StringField('Họ và tên', [DataRequired(ERROR_EMPTY_MESSAGE)])
    email = EmailField('Email', [DataRequired(ERROR_EMPTY_MESSAGE),
                                 Email(ERROR_NOT_VALID_EMAIL)])
    password = PasswordField('Mật khẩu', validators=[
        DataRequired(ERROR_EMPTY_MESSAGE), EqualTo('password2', message='Mật khẩu không trùng khớp')])
    password2 = PasswordField('Xác nhận mật khẩu', validators=[
        DataRequired(ERROR_EMPTY_MESSAGE)])

    def __init__(self, user, _cls_company, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.user = user

    def validate_email(self, field):
        if self.user.__class__.objects.filter(email=field.data).first():
            raise ValidationError(EMAIL_ALREADY_EXIT)


class UpdateProfileForm(FlaskForm):
    image_profile = FileField('Hình tài khoản', validators=[
        DataRequired(ERROR_EMPTY_MESSAGE),
        FileAllowed(ALLOW_IMAGE_EXTENSION, ERROR_EXTENSION_IMAGE_MESSAGE)
    ])

    def validate_image_profile(self, field):
        if get_size(field.data) > MAX_SIZE_IMG_PROFILE:
            raise ValidationError(ERROR_MAX_IMAGE_MESSAGE)