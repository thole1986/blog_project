from flask import render_template, make_response, request, jsonify
from flask_babel import lazy_gettext as _l
from werkzeug.http import HTTP_STATUS_CODES
from apps.errors import errors


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, _l('Unknown error'))}
    if message:
        payload['message'] = message
    payload['status_code'] = status_code
    payload['success'] = False

    response = jsonify(payload)
    response.status_code = status_code
    return response


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


@errors.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return error_response(404)
    resp = make_response(render_template('errors/404.html'), 404)
    return resp


@errors.app_errorhandler(403)
def forbidden(error):
    if wants_json_response():
        return error_response(403)
    resp = make_response(render_template('errors/403.html'), 403)
    return resp


@errors.app_errorhandler(500)
def internal_error(error):
    if wants_json_response():
        return error_response(500)
    resp = make_response(render_template('errors/500.html'), 500)
    return resp


@errors.app_errorhandler(400)
def bad_request(message):
    if wants_json_response():
        return error_response(400)
    resp = make_response(render_template('errors/404.html'), 400)
    return resp
