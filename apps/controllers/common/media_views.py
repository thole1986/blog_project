from flask import current_app, send_from_directory, abort
from apps.constant.common import NOT_FOUND_CODE
from apps.controllers.common import common


@common.route('/images/<path:path>', methods=['GET'])
def serve_file(path):
    try:
        return send_from_directory(current_app._get_current_object().config['UPLOADS'], path)
    except Exception:
        abort(NOT_FOUND_CODE)


