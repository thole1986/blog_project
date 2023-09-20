import re
import email_validator
from urllib.parse import urlparse, urljoin
from flask import request
from apps.constant.common import ZERO_VALUE


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def validate_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url)


def is_valid_email(value):
    try:
        email_validator.validate_email(
            value
        )
    except email_validator.EmailNotValidError:
        return False

    return True


def is_valid_mobile(mobile_number):
    clear_mobile_text = "".join(mobile_number.split())
    if not clear_mobile_text:
        return False
    pattern = re.compile('^(0|\\+84)(\\s|\\.)?((3[2-9])|(5[689])|(7[06-9])|(8[1-689])|'
                         '(9[0-46-9]))(\\d)(\\s|\\.)?(\\d{3})(\\s|\\.)?(\\d{3})$')
    return True if pattern.match(clear_mobile_text) else False


def is_float(value) -> bool:
    try:
        float(value)
        return True
    except Exception:
        return False


def float_value(value):
    try:
        return float(value)
    except Exception:
        return ZERO_VALUE

