from flask import request, url_for, redirect, render_template, flash
from . import admin
from apps.models.user import Role
from apps.decorators import role_required
from .forms.user_forms import AddRoleForm, EditRoleForm
from ...constant.common import PER_PAGE, DEFAULT_PAGE


@admin.route('/admin/role/', methods=['GET', 'POST'])
@role_required(['Admin'])
def manage_role():
    params = {}
    try:
        page = int(request.args.get('page', DEFAULT_PAGE))
    except (TypeError, ValueError):
        page = 1
    if request.method == 'GET':
        for k, v in request.args.items():
            if k not in ['page']:
                params[k] = str(v).strip()
    if request.method == 'POST':
        for k, v in request.form.items():
            if k != 'csrf_token' and v:
                params[k] = v
        return redirect(url_for('admin.manage_role', **params))
    if params.get('search'):
        field_search = params.get('search')
        pagination = Role.objects(name__icontains=field_search).order_by('-id').paginate(
            page=page, per_page=PER_PAGE)
    else:
        pagination = Role.objects().order_by('-id').paginate(page=page, per_page=PER_PAGE)
    roles = pagination.items
    return render_template('admin/role/manage_role.html',
                           roles=roles,
                           params=params,
                           pagination=pagination,
                           )


@admin.route('/admin/role/add/', methods=['GET', 'POST'])
@role_required(['Admin'])
def add_role():
    new_role = Role()
    form = AddRoleForm(new_role)
    if form.validate_on_submit():
        new_role.name = form.name.data
        new_role.description = form.description.data
        new_role.save()
        flash('Thêm mới thành công!', 'success')
        return redirect(url_for('.manage_role'))
    return render_template('admin/role/add_role.html',
                           form=form,
                           )


@admin.route('/admin/role/edit/<role_id>/', methods=['GET', 'POST'])
@role_required(['Admin'])
def edit_role(role_id):
    role = Role.objects.get_or_404(id=role_id)
    form = EditRoleForm(role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        role.save()
        flash('Cập nhật thành công!', 'success')
        return redirect(url_for('.manage_role'))
    form.name.data = role.name
    form.description.data = role.description
    return render_template('admin/role/edit_role.html',
                           form=form,
                           role=role,
                           )