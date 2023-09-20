from flask import url_for
from unidecode import unidecode
from apps import db
from apps.constant.common import MAIN_BANNER_IMAGE_UPLOAD_FOLDER, SUB_BANNER_IMAGE_UPLOAD_FOLDER
from apps.models.base import Media, BaseLog


class BannerMedia(Media):
    pass


class Banner(BaseLog):
    background_image = db.ReferenceField('BannerMedia')
    title = db.StringField(required=True, unique=True)
    unaccented_title = db.StringField()
    description = db.StringField()
    published = db.BooleanField(default=False)
    published_time = db.DateTimeField()
    removed = db.BooleanField(default=False)

    meta = {
        'abstract': True,
        'allow_inheritance': True,
    }

    def clean(self):
        self.unaccented_title = unidecode(self.title)

    @property
    def status_name(self):
        status = 'Chưa áp dụng'
        if self.published is True:
            status = 'Đang áp dụng'
        return status


class MainBanner(Banner):

    @property
    def url_background(self):
        if not isinstance(self.background_image, BannerMedia):
            return None
        return url_for('common.serve_file',
                       path=f"{MAIN_BANNER_IMAGE_UPLOAD_FOLDER}/"
                            f"{self.background_image.id}.{self.background_image.file_extension}"
                       )


class SubBanner(Banner):

    @property
    def url_background(self):
        if not isinstance(self.background_image, BannerMedia):
            return None
        return url_for('common.serve_file',
                       path=f"{SUB_BANNER_IMAGE_UPLOAD_FOLDER}/"
                            f"{self.background_image.id}.{self.background_image.file_extension}"
                       )






