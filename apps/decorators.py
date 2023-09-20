from functools import wraps
from flask import abort, request, url_for, redirect
from flask_login import current_user, AnonymousUserMixin
from apps.constant.common import FORBIDDEN_ERROR_CODE


def role_required(role_list):
    def decorator(func):
        @wraps(func)
        def authorize(*args, **kwargs):
            has_access = False
            user = current_user._get_current_object()
            if isinstance(user, AnonymousUserMixin):
                return redirect(url_for('user.login', next=request.url))
            else:
                if user.has_role('Admin'):
                    has_access = True
                else:
                    for role_name in role_list:
                        if user.has_role(role_name):
                            has_access = True
                            break
                if has_access is True:
                    return func(*args, **kwargs)
                else:
                    return abort(FORBIDDEN_ERROR_CODE)
        return authorize
    return decorator
