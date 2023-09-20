from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from datetime import datetime as dt, timezone, timedelta
import jwt
from mongoengine import DoesNotExist
from unidecode import unidecode
from werkzeug.security import check_password_hash, generate_password_hash
from apps.models.base import BasePerson, Media, TimeStamp
from apps.constant.status import ACTIVE, STATUS_CHOICES
from apps import db, login_manager


ADMIN = 'Admin'


class Role(db.Document):
    name = db.StringField(unique=True, required=True)
    description = db.StringField()
    created_at = db.DateTimeField(default=dt.now)
    updated_at = db.DateTimeField()

    def __repr__(self):
        return self.name

    @classmethod
    def create_admin_role(cls):
        role = Role.objects(name=ADMIN).first()
        if not role:
            Role(
                name=ADMIN,
                description=ADMIN,
            ).save()

    meta = {
        'allow_inheritance': False,
    }


class ChildMenu(db.EmbeddedDocument):
    name = db.StringField(required=True)
    endpoint = db.StringField()
    related_endpoints = db.ListField(db.StringField(), default=[])


class UserMenu(db.Document):
    roles = db.ListField(db.ReferenceField(Role), default=[])
    name = db.StringField(required=True)
    unaccented_name = db.StringField()
    icon = db.StringField()
    dropdown = db.BooleanField(default=True)
    child_menus = db.EmbeddedDocumentListField(ChildMenu, default=[])
    removed = db.BooleanField(default=False)

    def __repr__(self):
        return self.name

    def clean(self):
        self.unaccented_name = unidecode(self.name)

    def add_child(self, child_menu: ChildMenu):
        return self.modify(add_to_set__child_menus=child_menu)

    def user_menu(self, user):
        return list(set(user.roles).intersection(self.roles)) is not None


class User(BasePerson, UserMixin):
    email = db.EmailField(required=True, unique=True)
    phone = db.StringField()
    full_name = db.StringField()
    unaccented_fullname = db.StringField()
    password_hash = db.StringField()
    is_admin = db.BooleanField(default=False)
    roles = db.ListField(db.ReferenceField(Role), default=[])
    confirmed = db.BooleanField(default=False)
    session_token = db.StringField()
    last_login = db.DateTimeField(default=dt.now)
    confirmed_at = db.DateTimeField()
    company = db.ReferenceField('Company', default=None)
    status = db.IntField(default=ACTIVE)

    meta = {
        'indexes': ['email', 'status'],
    }

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.session_token)

    @property
    def status_name(self):
        return STATUS_CHOICES[self.status - 1][1]

    def generate_confirmation_token(self, expiration=3600):
        payload = {'confirm': str(
            self.id), 'exp': dt.now() + timedelta(seconds=expiration)}
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

    def confirm(self, token, leeway=10):
        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], leeway=leeway, algorithms=["HS256"])
        except:
            return False
        if data.get('confirm') != str(self.id):
            return False
        self.confirmed = True
        self.status = ACTIVE
        self.save()
        return True

    def generate_reset_token(self, expiration=3600):
        payload = {'reset': str(self.id), 'exp': dt.now() +
                   timedelta(seconds=expiration)}
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

    @staticmethod
    def reset_password(token, new_password, leeway=10):
        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], leeway=leeway, algorithms=["HS256"])
        except:
            return False
        try:
            user = User.objects.get(id=data.get('reset'))
        except DoesNotExist:
            return False
        user.password = new_password
        user.save()
        return True

    def generate_email_change_token(self, new_email, expiration=600):
        payload = {'user_id': str(self.id), 'new_email': new_email,
                   'exp': dt.now() + timedelta(seconds=expiration)}
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

    def change_email(self, token, leeway=10):
        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], leeway=leeway, algorithms=["HS256"])
        except:
            return False
        if data.get('user_id') != str(self.id):
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if User.objects(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.save()
        return True

    def generate_auth_token(self, expiration=600):
        payload = {'user_id': self.id,
                   'exp': dt.now() + timedelta(seconds=expiration)}
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

    @staticmethod
    def verify_auth_token(token, leeway=10):
        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], leeway=leeway, algorithms=["HS256"])
        except:
            return None
        try:
            return User.objects.get(id=data.get('user_id'))
        except DoesNotExist:
            return None

    def has_role(self, role_name):
        try:
            r = Role.objects.get(name=role_name)
        except DoesNotExist:
            return False
        if r and r in self.roles:
            result = True
        else:
            result = False
        return result

    def ping(self):
        self.last_login = dt.now()
        self.save()

    def add_role(self, role_name):
        try:
            role = Role.objects.get(name=role_name)
        except DoesNotExist:
            role = Role(
                name=role_name,
                description=role_name,
            ).save()
        if role and role not in self.roles:
            self.__class__.objects(id=self.id).update(add_to_set__roles=role)
            self.reload()
            return True


class Notification(TimeStamp):
    name = db.StringField()
    user = db.ReferenceField(User)


class Task(TimeStamp):
    name = db.StringField()
    description = db.StringField()
    user = db.ReferenceField(User)
    complete = db.BooleanField(default=False)


class Profile(db.Document):
    user = db.ReferenceField(User)


class AnonymousUser(AnonymousUserMixin):

    def is_administrator(self):
        return False

    def has_role(self, role_name=None):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(session_token):
    try:
        user = User.objects(session_token=session_token).first()
    except Exception:
        user = None
    return user
