from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Optional

from apps.constant.common import ZERO_VALUE
from apps.constant.forms import (
    ERROR_EMPTY_MESSAGE,
    DEFAULT_OPTION_CHOICES, CATEGORY_NAME_ALREADY_EXIST, ERROR_NOT_VALID_VALUE,
)
from apps.controllers.admin.forms.common_forms import SubIntField


class AddBlogCategory(FlaskForm):
    name = StringField('Tên danh mục', [DataRequired(ERROR_EMPTY_MESSAGE)])
    parent = SelectField('Danh mục cha', coerce=str)
    description = TextAreaField('Mô tả', [Optional()])

    def __init__(self, category, *args, **kwargs):
        super(AddBlogCategory, self).__init__(*args, **kwargs)
        self.category = category
        category_choices = list(DEFAULT_OPTION_CHOICES)
        categories = [(str(cat.id), f'{cat.name}') for cat in
                      self.category.__class__.objects(active=True).order_by('name')]
        if categories:
            category_choices.extend(categories)
        self.parent.choices = category_choices

    def validate(self, extra_validators=None):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        if self.category.__class__.objects(name=self.name.data).first():
            self.name.errors.append(CATEGORY_NAME_ALREADY_EXIST)
            return False
        return True


class EditBlogCategory(FlaskForm):
    name = StringField('Tên danh mục', [DataRequired(ERROR_EMPTY_MESSAGE)])
    sort_number = SubIntField('Số thứ tự hiển thị', [Optional()])
    parent = SelectField('Danh mục mẹ', coerce=str, validate_choice=False)
    external = BooleanField('Cho phép hiển thị danh mục này trên trang chủ?', validators=[Optional()])
    description = TextAreaField('Mô tả', [Optional()])

    def __init__(self, category, *args, **kwargs):
        super(EditBlogCategory, self).__init__(*args, **kwargs)
        self.category = category
        category_choices = list(DEFAULT_OPTION_CHOICES)
        categories = [(str(cat.id), f'{cat.name}') for cat in
                      self.category.__class__.objects(id__ne=self.category.id, active=True).order_by('name')]
        if categories:
            category_choices.extend(categories)
        self.parent.choices = category_choices

    def validate_sort_number(self, field):
        if field.data:
            if not isinstance(field.data, int):
                self.sort_number.errors.append(ERROR_NOT_VALID_VALUE)
                return False
            if field.data <= ZERO_VALUE:
                self.sort_number.errors.append(ERROR_NOT_VALID_VALUE)
                return False
        return True

    def validate(self, extra_validators=None):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        if (self.name.data != self.category.name) and \
                self.category.__class__.objects(name=self.name.data).first():
            self.name.errors.append(CATEGORY_NAME_ALREADY_EXIST)
            return False
        return True

