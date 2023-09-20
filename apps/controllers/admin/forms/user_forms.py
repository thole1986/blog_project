from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, SelectMultipleField, SelectField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError, Length, Optional, EqualTo
from wtforms.fields import EmailField
from apps.constant.status import STATUS_CHOICES, ACTIVE
from apps.models.user import User, Role
from apps.utils.shared import get_size, clean_string
from apps.constant.forms import (
    ERROR_EMPTY_MESSAGE,
    ERROR_NOT_VALID_EMAIL,
    EMAIL_ALREADY_EXIT, MAX_LENGTH_TEXT, MAX_LENGTH_TEXT_MESSAGE, ERROR_ROLE_NAME_ALREADY_EXIST,
)


class AddUserForm(FlaskForm):
    name = StringField('Họ và tên', [DataRequired(ERROR_EMPTY_MESSAGE), Length(min=2, max=64, message=_l('Từ (2-64) ký tự!'))])
    email = EmailField('Email', [DataRequired(ERROR_EMPTY_MESSAGE),
                                 Email(ERROR_NOT_VALID_EMAIL)])
    roles = SelectMultipleField('Vai trò', [DataRequired(ERROR_EMPTY_MESSAGE)], coerce=str)
    status = SelectField('Trạng thái', choices=STATUS_CHOICES, coerce=int, default=ACTIVE)
    phone = StringField('Số điện thoại', [Optional()])

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.status.choices = STATUS_CHOICES
        self.roles.choices = [(str(role.id), role.name) for role in Role.objects().order_by('name')]

    def validate_email(self, field):
        if User.objects(email=field.data).first():
            raise ValidationError(EMAIL_ALREADY_EXIT)


class EditUserForm(FlaskForm):
    name = StringField('Họ và tên',
                       [DataRequired(ERROR_EMPTY_MESSAGE), Length(min=2, max=64, message=_l('Từ (2-64) ký tự!'))])
    email = EmailField('Email', [DataRequired(ERROR_EMPTY_MESSAGE),
                                 Email(ERROR_NOT_VALID_EMAIL)])
    roles = SelectMultipleField('Vai trò', [DataRequired(ERROR_EMPTY_MESSAGE)], coerce=str)
    status = SelectField('Trạng thái', choices=STATUS_CHOICES, coerce=int)
    phone = StringField('Số điện thoại', [Optional()])

    def __init__(self, user, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.user = user
        self.status.choices = STATUS_CHOICES
        self.roles.choices = [(str(role.id), role.name) for role in Role.objects().order_by('name')]

    def validate_email(self, field):
        if field.data != self.user.email and User.objects(email=field.data).first():
            raise ValidationError(EMAIL_ALREADY_EXIT)


class AddRoleForm(FlaskForm):
    name = StringField('Tên vai trò', [DataRequired(ERROR_EMPTY_MESSAGE)])
    description = TextAreaField('Mô tả', [Optional(),
                                          Length(max=MAX_LENGTH_TEXT, message=MAX_LENGTH_TEXT_MESSAGE)])

    def __init__(self, *args, **kwargs):
        super(AddRoleForm, self).__init__(*args, **kwargs)

    def validate_name(self, field):
        if Role.objects(name=clean_string(field.data)).first():
            raise ValidationError(_l('Tên vai trò đã tồn tại!'))


class EditRoleForm(FlaskForm):
    name = StringField('Tên vai trò', [DataRequired(ERROR_EMPTY_MESSAGE)])
    description = TextAreaField('Mô tả', [Optional(), Length(max=MAX_LENGTH_TEXT, message=MAX_LENGTH_TEXT_MESSAGE)])

    def __init__(self, role, *args, **kwargs):
        super(EditRoleForm, self).__init__(*args, **kwargs)
        self.role = role

    def validate_name(self, field):
        if self.role.name != field.data and \
                Role.objects(name=clean_string(field.data)).first():
            raise ValidationError(ERROR_ROLE_NAME_ALREADY_EXIST)


class EditProfileForm(FlaskForm):
    name = StringField('Họ và tên', [DataRequired(ERROR_EMPTY_MESSAGE)])
    phone = StringField('Số điện thoại', [Optional()])
    password = PasswordField('Mật khẩu mới', [Optional(), EqualTo('password2', message='Mật khẩu không trùng khớp')])
    password2 = PasswordField('Xác nhận mật khẩu', [Optional()])