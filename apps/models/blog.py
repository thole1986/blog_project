from flask import url_for
from slugify import slugify
from unidecode import unidecode
from apps import db
from apps.constant.common import DEFAULT_IMAGE, URL_VIEW_SERVE_IMAGE, ZERO_VALUE, DEFAULT_NONE
from apps.models.base import BaseCategory, BaseComment, Media, BaseLog, BaseTag


class BlogCategory(BaseCategory):
    parent = db.ReferenceField('self', default=DEFAULT_NONE)
    order_number = db.IntField(default=ZERO_VALUE)

    @property
    def total_blog(self):
        return Blog.objects(category__in=self.all_children(include_root=True), published=True, removed=False).count()


class Comment(BaseComment):
    pass


class BlogMedia(Media):
    pass


class BlogTag(BaseTag):
    pass


class Blog(BaseLog):
    name = db.StringField(required=True)
    unaccented_name = db.StringField()
    excerpt = db.StringField()
    content = db.StringField()
    comments = db.EmbeddedDocumentListField(Comment)
    slug = db.StringField()
    link_video = db.URLField()
    tags = db.ListField(db.ReferenceField(BlogTag), default=[])
    category = db.ReferenceField(BlogCategory)
    comment_allowed = db.BooleanField(default=True)
    image = db.ReferenceField(BlogMedia)
    published = db.BooleanField(default=False)
    published_by = db.ReferenceField("User")
    published_at = db.DateTimeField()
    pinned = db.BooleanField(default=False)
    removed = db.BooleanField(default=False)

    def clean(self):
        self.slug = f'{slugify(self.name)}.htm'
        self.unaccented_name = unidecode(self.name)

    @property
    def show_image(self):
        if isinstance(self.image, BlogMedia):
            return url_for(URL_VIEW_SERVE_IMAGE, uid=self.image.uid)
        return url_for('static', filename=DEFAULT_IMAGE)
