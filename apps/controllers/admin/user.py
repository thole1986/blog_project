from flask import request, url_for, redirect, render_template, flash, abort
from flask_login import login_required, current_user, logout_user
from mongoengine import Q
from . import admin
from apps.models.user import User, Role
from apps.decorators import role_required
from .forms.user_forms import AddUserForm, EditUserForm, EditProfileForm
from ...constant.common import PER_PAGE, DEFAULT_PAGE, DEFAULT_USER_PASSWORD, NOT_FOUND_CODE
from ...constant.status import ACTIVE


@admin.route('/admin/user/', methods=['GET', 'POST'])
@role_required(['Admin'])
def manage_user():
    params = {}
    try:
        page = int(request.args.get('page', DEFAULT_PAGE))
    except (TypeError, ValueError):
        page = DEFAULT_PAGE
    if request.method == 'GET':
        for k, v in request.args.items():
            if k not in ['page']:
                params[k] = str(v).strip()
    if request.method == 'POST':
        for k, v in request.form.items():
            if k != 'csrf_token' and v:
                params[k] = v
        return redirect(url_for('admin.manage_user', **params))
    if params.get('search'):
        field_search = params.get('search')
        pagination = User.objects(
            Q(email__icontains=field_search) |
            Q(full_name__icontains=field_search) |
            Q(unaccented_fullname__icontains=field_search)
        ).order_by('-id').paginate(page=page, per_page=PER_PAGE)
    else:
        pagination = User.objects().order_by('-id').paginate(page=page, per_page=PER_PAGE)

    users = pagination.items
    return render_template('admin/user/manage_user.html',
                           users=users,
                           params=params,
                           pagination=pagination,
                           )


@admin.route('/admin/user/add/', methods=['GET', 'POST'])
@role_required(['Admin'])
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        new_user = User()
        new_user.full_name = form.name.data
        new_user.phone = form.phone.data
        new_user.email = form.email.data
        try:
            roles = Role.objects(id__in=form.roles.data)
        except Exception:
            roles = []
        if roles:
            new_user.roles = roles
        new_user.password = DEFAULT_USER_PASSWORD
        new_user.confirmed = True
        new_user.save()
        flash('Tạo mới tài khoản thành công!', 'success')
        return redirect(url_for('admin.manage_user'))
    return render_template('admin/user/add_user.html',
                           form=form,
                           )


@admin.route('/admin/user/edit/<user_id>/', methods=['GET', 'POST'])
@role_required(['Admin'])
def edit_user(user_id):
    edited_user = User.objects.get_or_404(id=user_id)
    form = EditUserForm(edited_user)
    edited_user_roles = [str(role.id) for role in edited_user.roles if edited_user.roles]
    if form.validate_on_submit():
        edited_user.full_name = form.name.data
        edited_user.email = form.email.data
        edited_user.status = form.status.data
        if form.status.data == ACTIVE:
            edited_user.confirmed = True
        else:
            edited_user.confirmed = False
        edited_user.phone = form.phone.data
        try:
            new_roles = Role.objects(id__in=form.roles.data)
        except Exception:
            new_roles = []
        if new_roles:
            edited_user.roles = new_roles
        edited_user.save()
        flash('Cập nhật tài khoản thành công!', 'success')
        return redirect(request.url)

    form.email.data = edited_user.email
    form.phone.data = edited_user.phone
    form.name.data = edited_user.full_name
    form.status.data = edited_user.status
    form.roles.data = edited_user_roles
    return render_template('admin/user/edit_user.html',
                           edited_user=edited_user,
                           form=form,
                           )


@admin.route('/thong-tin-nguoi-dung/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    form = EditProfileForm()
    try:
        edited_user = User.objects.get_or_404(id=user_id)
    except Exception:
        flash('Thông tin cá nhân không tồn tại!', 'warning')
        return abort(NOT_FOUND_CODE)

    if current_user != edited_user:
        return abort(NOT_FOUND_CODE)

    if form.validate_on_submit():
        edited_user.full_name = form.name.data
        edited_user.phone = form.phone.data
        if form.password.data:
            edited_user.password = form.password.data
            edited_user.save()
            logout_user()
            flash('Bạn đã cập nhật mật khẩu mới, vui lòng đăng nhập lại.', 'info')
            return redirect(url_for('user.login'))
        edited_user.save()
        flash('Thông tin cá nhân đã cập nhật thành công.', 'success')
        return redirect(url_for('.edit_profile', user_id=edited_user.id))

    form.name.data = edited_user.full_name
    form.phone.data = edited_user.phone

    return render_template('admin/user/edit_profile.html',
                           edited_user=edited_user,
                           form=form
                           )
