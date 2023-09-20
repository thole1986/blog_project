import os
from pathlib import Path
from datetime import datetime as dt
from uuid import uuid4
from slugify import slugify
from unidecode import unidecode
from apps import db
from apps.constant.address import ADDRESS_TYPE_CHOICES
from apps.models.address import _get_reference_zone, _get_address
from apps.utils.shared import create_new_folder, join_path


class TimeStamp(db.Document):
    created_at = db.DateTimeField(default=dt.now)
    updated_at = db.DateTimeField()

    meta = {
        'allow_inheritance': True,
        'abstract': True,
    }


class BaseLog(TimeStamp):
    created_by = db.ReferenceField('User')
    updated_by = db.ReferenceField('User')

    meta = {
        'abstract': True,
        'allow_inheritance': True,
    }


class BasePerson(BaseLog):
    name = db.StringField()
    unaccented_name = db.StringField()

    meta = {
        'abstract': True,
        'allow_inheritance': True,
    }

    def clean(self):
        pass


class BaseCategory(BaseLog):
    name = db.StringField(required=True)
    unaccented_name = db.StringField()
    description = db.StringField()
    slug = db.StringField()
    private_category = db.BooleanField(default=False)
    removed = db.BooleanField(default=False)
    active = db.BooleanField(default=True)
    external = db.BooleanField(default=False)

    meta = {
        'abstract': True,
        'allow_inheritance': True,
    }

    def clean(self):
        self.slug = f'{slugify(self.name)}'
        self.unaccented_name = unidecode(self.name)

    @property
    def children(self):
        return self.__class__.objects(parent=self)

    def has_children(self):
        return self.__class__.objects(parent=self).first() is not None

    @property
    def all_parent(self):
        parents = []
        parent_cat = self.parent
        while parent_cat:
            parents.append(parent_cat)
            parent_cat = parent_cat.parent

        return list(reversed(parents))

    def all_children(self, include_root=False):
        result = []
        if include_root:
            result.append(self)

        for child in self.children:
            result.append(child)
            if child.parent:
                result.extend(child.all_children())

        return result


class BaseComment(db.EmbeddedDocument):
    uid = db.UUIDField(binary=False, default=uuid4)
    content = db.StringField(required=True)
    response_to = db.UUIDField()  # reference to uid of another comment
    disabled = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=dt.now)

    meta = {
        'abstract': True,
        'allow_inheritance': True,
    }


class BaseAddress(db.EmbeddedDocument):
    address = db.StringField(required=True)
    address_type = db.IntField(default=ADDRESS_TYPE_CHOICES[0][0], choices=ADDRESS_TYPE_CHOICES)
    is_default = db.BooleanField(default=True)
    province = db.ReferenceField("Province")
    district = db.ReferenceField("District")
    ward = db.ReferenceField("Ward")
    remark = db.StringField()
    created_at = db.DateTimeField(default=dt.now)
    updated_at = db.DateTimeField()
    created_by = db.ReferenceField("User")
    updated_by = db.ReferenceField("User")

    meta = {
        'abstract': True,
        'allow_inheritance': True,
    }

    @classmethod
    def _get_reference_fields(cls, **kwargs):
        return _get_reference_zone(**kwargs)

    @classmethod
    def create_or_update_address(cls, **kwargs):
        _reference_data = cls._get_reference_fields(**kwargs)
        kwargs.update(**_reference_data)
        result = {}
        for k, v in kwargs.items():
            if k in list(cls._fields):
                if k == 'uid':
                    pass
                if k == 'address_type' and v in dict(ADDRESS_TYPE_CHOICES).keys():
                    result[k] = v
                else:
                    result[k] = v
        return cls(**result)

    @property
    def address_string(self):
        return _get_address(self)


class BaseStatus(TimeStamp):
    status_name = db.StringField()
    status_value = db.IntField()

    meta = {
        'abstract': True,
        'allow_inheritance': True,
    }


class BaseTag(BaseLog):
    name = db.StringField(required=True, unique=True)

    meta = {
        'abstract': True,
        'allow_inheritance': True,
    }


class Media(BaseLog):
    uid = db.UUIDField(binary=False, default=uuid4)
    original_filename = db.StringField(default=None)
    file_extension = db.StringField()
    content_type = db.StringField()
    file = db.FileField()

    meta = {
        'abstract': True,
        'allow_inheritance': True,
    }

    @staticmethod
    def create_folder_upload(new_path, file):
        return create_new_folder(join_path(new_path, file))

    @staticmethod
    def __image_file(path, file):
        full_path = join_path(path)
        _file = join_path(path, file)
        if not (os.path.isfile(_file)):
            return None
        return _file, full_path

    def remove_image_file(self, path, file):
        image_file = self.__image_file(path, file)
        if image_file:
            # Unpack to file and folder path
            _file, full_path = image_file
            # Remove file
            Path(_file).unlink()
            if not os.listdir(full_path):
                # Remove folder if not has any file.
                os.rmdir(full_path)
