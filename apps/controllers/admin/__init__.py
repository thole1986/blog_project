from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import dashboard, user, banner, media, role, blog, category
