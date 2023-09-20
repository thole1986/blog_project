from flask import Blueprint

common = Blueprint('common', __name__)

from . import media_views, zone_views
