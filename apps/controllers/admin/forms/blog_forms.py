from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField, FileField, URLField
from wtforms.validators import DataRequired, Optional, Length, URL
from apps.constant.forms import (
    ERROR_EMPTY_MESSAGE,
    DEFAULT_OPTION_CHOICES, MAX_LENGTH, MAX_LENGTH_MESSAGE, BLOG_TITLE_ALREADY_EXIST, INVALID_URL_MESSAGE
)
from apps.controllers.admin.forms.common_forms import CommonImageForm
from apps.controllers.functions import _validate_image


class AddBlogForm(FlaskForm):
    name = StringField('Tên bài viết', [DataRequired(ERROR_EMPTY_MESSAGE)])
    category = SelectField('Thuộc danh mục', coerce=str, validate_choice=False)

    def __init__(self, new_subject, _cls, *args, **kwargs):
        super(AddBlogForm, self).__init__(*args, **kwargs)
        self.new_subject = new_subject
        category_choices = list(DEFAULT_OPTION_CHOICES)
        categories = [(str(cat.id), f'{cat.name}') for cat in
                      _cls.objects(active=True).order_by('name')]
        if categories:
            category_choices.extend(categories)
        self.category.choices = category_choices

    def validate(self, extra_validators=None):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        if self.new_subject.__class__.objects(name=self.name.data).first():
            self.name.errors.append(BLOG_TITLE_ALREADY_EXIST)
            return False
        return True


class EditBlogForm(CommonImageForm):
    name = StringField('Tên bài viết', [DataRequired(ERROR_EMPTY_MESSAGE)])
    content = TextAreaField('Nội dung', [Optional()])
    link_video = StringField('Đường dẫn nhúng video từ Youtube', [Optional(), URL(message=INVALID_URL_MESSAGE)])
    excerpt = TextAreaField('Trích dẫn', [Optional(), Length(max=MAX_LENGTH, message=MAX_LENGTH_MESSAGE)])
    published = BooleanField('Cho phép đăng lên trang chủ?', validators=[Optional()])
    category = SelectField('Danh mục mẹ', coerce=str)

    def __init__(self, blog, blog_image, cls, *args, **kwargs):
        super(EditBlogForm, self).__init__(*args, **kwargs)
        self.blog = blog
        self._image = blog_image
        self.cls = cls
        category_choices = list(DEFAULT_OPTION_CHOICES)
        categories = [(str(cat.id), f'{cat.name}') for cat in
                      cls.objects(active=True).order_by('name')]
        if categories:
            category_choices.extend(categories)
        self.category.choices = category_choices

    def validate(self, extra_validators=None):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        if self.name.data != self.blog.name and \
                self.blog.__class__.objects(name=self.name.data).first():
            self.name.errors.append(BLOG_TITLE_ALREADY_EXIST)
            return False
        return True

    def validate_image(self, field):
        _validate_image(self, field)