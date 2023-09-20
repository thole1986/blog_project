import errno
import os
import secrets
import uuid
from datetime import datetime as dt
from flask import current_app
from apps.constant.common import CONTENT_TYPE_CHOICES, ZERO_VALUE
from apps.utils.validate import is_float


def join_path(path, file=None):
    uploads = current_app._get_current_object().config['UPLOADS']
    if file:
        return os.path.join(uploads + path, file)
    return os.path.join(uploads + path)


def convert_to_datetime_object(value, type_format='%d/%m/%Y'):
    datetime_object = None
    if not value:
        return datetime_object
    if isinstance(value, str):
        try:
            datetime_object = dt.strptime(value, type_format)
        except Exception:
            pass

    return datetime_object


def clean_string(format_string: str):
    result = ''
    if isinstance(format_string, str):
        result = " ".join(format_string.split())
    return result


def create_new_folder(path_directory):
    if not os.path.exists(path_directory):
        try:
            os.makedirs(os.path.dirname(path_directory))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    return path_directory


def timesince(date_time, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = dt.now()
    diff = now - date_time

    periods = (
        (diff.days / 365, "năm", "năm"),
        (diff.days / 30, "month", "tháng"),
        (diff.days / 7, "week", "tuần"),
        (diff.days, "ngày", "ngày"),
        (diff.seconds / 3600, "giờ", "giờ"),
        (diff.seconds / 60, "phút", "phút"),
        (diff.seconds, "giây", "giây"),
    )

    for period, singular, plural in periods:

        if period:
            return "%d %s" % (period, singular if period == 1 else plural)

    return default


def generate_random_token(length=16):
    return secrets.token_hex(length)


def get_size(file_request):
    if file_request.content_length:
        return file_request.content_length
    try:
        pos = file_request.tell()
        file_request.seek(0, 2)  # seek to end
        size = file_request.tell()
        file_request.seek(pos)  # back to original position
        return size
    except (AttributeError, IOError):
        pass

    return ZERO_VALUE


def get_random_string(length=16):
    return uuid.uuid4().hex[:length].upper()


def get_number_from_datetime(datetime_format=None):
    if not datetime_format:
        datetime_format = '%Y%m%d%H%M%S'
    return dt.now().strftime(datetime_format)


def find_content_type(file_ext):
    file_ext = file_ext.lower()
    if file_ext in CONTENT_TYPE_CHOICES.keys():
        return CONTENT_TYPE_CHOICES[file_ext]
    return None


def get_file_extension(filename):
    ext = os.path.splitext(filename)[1]
    if ext.startswith('.'):
        ext = ext[1:]
    return ext.lower()


def format_currency(value):
    _value = ZERO_VALUE
    if is_float(value):
        _value = "{:,.0f}".format(value).replace(',', '.')
    return _value

