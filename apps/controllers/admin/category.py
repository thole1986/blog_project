from flask import request, url_for, redirect, render_template, flash
from flask_login import current_user
from datetime import datetime as dt
from mongoengine import Q
from . import admin
from apps.decorators import role_required
from .forms.blog_category_form import AddBlogCategory, EditBlogCategory
from ...constant.common import PER_PAGE, DEFAULT_PAGE
from ...models.blog import BlogCategory


@admin.route('/admin/category/', methods=['GET', 'POST'])
@role_required(['Admin'])
def manage_category():
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
        return redirect(url_for('admin.manage_category', **params))
    per_page = PER_PAGE
    if params.get('search'):
        field_search = params.get('search')
        pagination = BlogCategory.objects(
            Q(name__icontains=field_search) |
            Q(slug__icontains=field_search) |
            Q(unaccented_name__icontains=field_search),
            active=True,
        ).order_by('-id').paginate(page=page, per_page=per_page)
    else:
        pagination = BlogCategory.objects(active=True).order_by('-id').paginate(page=page, per_page=per_page)

    categories = pagination.items
    return render_template('admin/category/manage_category.html',
                           categories=categories,
                           pagination=pagination,
                           params=params,
                           )


@admin.route('/admin/subject/category/add/', methods=['GET', 'POST'])
@role_required(['Admin'])
def add_category():
    new_category = BlogCategory()
    form = AddBlogCategory(new_category)
    if form.validate_on_submit():
        new_category.name = form.name.data
        new_category.description = form.description.data
        new_category.created_by = current_user._get_current_object()
        new_category.created_at = dt.now()
        new_category.save()
        try:
            parent = BlogCategory.objects.get(id=form.parent.data)
        except Exception:
            parent = None
        new_category.parent = parent
        new_category.save()
        flash("Danh mục đã được thêm mới thành công", "success")
        return redirect(url_for('admin.manage_category'))

    return render_template('admin/category/add_category.html',
                           form=form,
                           )


@admin.route('/admin/category/edit/<category_id>/', methods=['GET', 'POST'])
@role_required(['Admin'])
def edit_category(category_id):
    category = BlogCategory.objects.get_or_404(id=category_id)
    form = EditBlogCategory(category)
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        category.external = form.external.data
        category.updated_by = current_user._get_current_object()
        category.updated_at = dt.now()
        try:
            parent = BlogCategory.objects.get(id=form.parent.data)
        except Exception:
            parent = None
        category.parent = parent
        category.save()
        flash("Cập nhật danh mục thành công!", "success")
        return redirect(request.url)

    form.description.data = category.description
    form.name.data = category.name
    form.external.data = category.external
    form.parent.data = str(category.parent.id) if category.parent else None

    return render_template('admin/category/edit_category.html',
                           form=form,
                           category=category,
                           )

