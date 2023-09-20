from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, ValidationError, Optional, Length, Email
from apps.constant.forms import (
    ERROR_EMPTY_MESSAGE,
    DEFAULT_OPTION_CHOICES,
    MAX_LENGTH_TEXT, MAX_LENGTH_TEXT_MESSAGE,
    ERROR_NOT_VALID_PHONE, ERROR_NOT_VALID_EMAIL,
)
from apps.utils.location import cached_provinces
from apps.utils.validate import is_valid_mobile


class SearchForm(FlaskForm):
    q = StringField(None, validators=[Optional()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class ContactForm(FlaskForm):
    name = StringField('Họ và tên', validators=[DataRequired(ERROR_EMPTY_MESSAGE)])
    title = StringField('Tiêu đề', validators=[DataRequired(ERROR_EMPTY_MESSAGE)])
    phone = StringField('Số di động', validators=[DataRequired(ERROR_EMPTY_MESSAGE)])
    email = StringField('Email', validators=[DataRequired(ERROR_EMPTY_MESSAGE), Email(message=ERROR_NOT_VALID_EMAIL)])
    description = TextAreaField('Thông tin cần liên hệ', validators=[Optional()])
