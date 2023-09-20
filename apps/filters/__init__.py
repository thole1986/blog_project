from flask import Blueprint

filters = Blueprint("filters", __name__)

from apps.filters import functions, user, category
