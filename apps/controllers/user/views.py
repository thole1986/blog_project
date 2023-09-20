from flask import request, url_for, redirect, flash, render_template
from flask_login import login_user, current_user, login_required, logout_user
from uuid import uuid4
from datetime import datetime as dt
from . import user
from .forms import LoginForm, SignUpForm
from apps.models.user import User
from apps.send_mail import send_email
from ...constant.status import ACTIVE
from ...utils.validate import is_safe_url


@user.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'user' \
                and request.endpoint != 'static':
            return redirect(url_for('user.unconfirmed'))


@user.route('/chua-xac-thuc-tai-khoan')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('pages/user/unconfirmed.html')


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            if user.status == ACTIVE:
                user.session_token = str(uuid4())
                user.last_login = dt.now()
                user.save()
                login_user(user)
                next_url = request.form.get("next")
                if not next_url or not is_safe_url(next_url):
                    next_url = url_for('main.index')
                return redirect(next_url)
            else:
                flash('Tài khoản chưa được kích hoạt!', 'danger')
                return render_template('admin/auth/login.html', form=form)
        else:
            flash('Email hoặc mật khẩu không hợp lệ!', 'warning')
    return render_template('admin/auth/login.html', form=form)


# @user.route('/dang-ky', methods=['GET', 'POST'])
# def signup():
#     new_user = User()
#     form = SignUpForm(new_user)
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     if form.validate_on_submit():
#         new_user.email = form.email.data
#         new_user.full_name = form.name.data
#         new_user.password = form.password.data
#         new_user.save()
#         # flash('Đăng ký thành công! Vui lòng kiểm tra hộp thư và làm theo hướng dẫn để kích hoạt tài khoản.', 'success')
#         flash('Đăng ký thành công!', 'success')
#         return redirect(url_for('user.login'))
#     return render_template('admin/auth/signup.html',
#                            form=form,
#                            )


@user.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))



