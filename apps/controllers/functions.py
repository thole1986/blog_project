from flask import abort, make_response
from mongoengine import Q
from werkzeug.utils import secure_filename
from apps.constant.common import NOT_FOUND_CODE
from apps.constant.forms import ALLOW_VIEW_INLINE_EXTENSION, FILE_NAME_ALREADY_EXIST, MAX_SIZE_IMAGE, ERROR_MAX_IMAGE_MESSAGE, ALLOW_IMAGE_EXTENSION, ERROR_EXTENSION_IMAGE_MESSAGE, ALLOWED_EXTENSIONS, MAX_SIZE_FILE, ERROR_EXTENSION_MESSAGE, ERROR_MAX_FILE_MESSAGE
from apps.utils.shared import get_size


def _validate_image(obj, field):
    filename = secure_filename(field.data.filename)
    if filename:
        # if obj._image.__class__.objects(
        #         original_filename=field.data.filename,
        # ).first():
        #     obj.image.errors.append(FILE_NAME_ALREADY_EXIST)
        if get_size(field.data) > MAX_SIZE_IMAGE:
            obj.image.errors.append(ERROR_MAX_IMAGE_MESSAGE)
        if not ('.' in filename and filename.rsplit('.', 1)[1] in ALLOW_IMAGE_EXTENSION):
            obj.image.errors.append(ERROR_EXTENSION_IMAGE_MESSAGE)
    if obj.image.errors:
        return False


def _handle_render_file(_cls, **query):
    """
    :param _cls: The class object
    :param query: the params for _cls to implement
    :return: read file and return the file object on views
    """
    try:
        obj = _cls.objects.get(**query)
    except Exception:
        return abort(NOT_FOUND_CODE)
    file_obj = obj.file.read()
    if file_obj:
        response = make_response(file_obj)
        response.mimetype = obj.content_type
        if obj.file_extension in ALLOW_VIEW_INLINE_EXTENSION:
            response.headers.set('Content-Disposition', 'inline', filename=obj.original_filename)
        else:
            response.headers.set('Content-Disposition', 'attachment', filename=obj.original_filename)
        return response
    else:
        return make_response(abort(NOT_FOUND_CODE))


def _validate_file(obj_form, field_form):
    filename = secure_filename(field_form.data.filename)
    if filename:
        if get_size(field_form.data) > MAX_SIZE_FILE:
            obj_form.file.errors.append(ERROR_MAX_FILE_MESSAGE)
        if not ('.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS):
            obj_form.file.errors.append(ERROR_EXTENSION_MESSAGE)
    if obj_form.file.errors:
        return False


