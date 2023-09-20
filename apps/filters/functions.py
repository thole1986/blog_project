from urllib import request
from PIL import ImageFile
from babel.numbers import format_decimal
import re
from jinja2 import pass_eval_context
from markupsafe import Markup, escape
from urllib.parse import urlparse, parse_qs
from apps.filters import filters
from apps.utils.shared import format_currency


@filters.app_template_filter()
def yt_embed(yt_url):
    """
    :param yt_url: a normal youtube video url e.g https://www.youtube.com/watch?v=QgjkjsqAzvo
    :return: the embedded url for a youtube video e.g https://www.youtube.com/embed/QgjkjsqAzvo
    """
    url_data = urlparse(yt_url)
    if "https://www.youtube.com" not in yt_url:
        raise Exception('Not valid YouTube Video URL')
    else:
        query = parse_qs(url_data.query)
        if 'v' in query:
            video_id = query['v'][0]
        else:
            video_id = None

        if video_id:
            result = "https://www.youtube.com/embed/%s" % video_id
        else:
            result = yt_url
        return result


@pass_eval_context
@filters.app_template_filter()
def newline_to_br(context, value: str) -> str:
    result = "<br />".join(re.split(r'(?:\r\n|\r|\n){2,}', escape(value)))

    if context.autoescape:
        result = Markup(result)

    return result


@filters.app_template_filter()
def format_decimal_number(value):
    return format_decimal(value)


@filters.app_template_filter()
def format_amount(value):
    return format_currency(value)


@filters.app_template_filter()
def get_size_file_from_url(url):
    url = 'http://localhost:5000/' + url
    file = request.urlopen(url)
    size = file.headers.get("content-length")
    if size:
        size = int(size)
    p = ImageFile.Parser()
    while 1:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            break
    file.close()
    return size

