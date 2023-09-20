from flask import request, url_for, redirect, render_template, flash
from flask_login import current_user
from datetime import datetime as dt
from mongoengine import Q
from . import admin
from .forms.blog_forms import AddBlogForm, EditBlogForm
from ..functions import _handle_render_file
from ...constant.common import PER_PAGE, DEFAULT_PAGE
from ...decorators import role_required
from ...models.blog import Blog, BlogCategory, BlogMedia


@admin.route('/admin/blog/', methods=['GET', 'POST'])
@role_required(['Admin', 'User', 'Manager'])
def manage_blog():
    user = current_user._get_current_object()
    params = {}
    query = {}
    if user.has_role('User'):
        query = {
            'created_by': user
        }
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
        return redirect(url_for('admin.manage_blog', **params))
    if params.get('search'):
        field_search = params.get('search')
        pagination = Blog.objects(
            Q(name__icontains=field_search) |
            Q(slug__icontains=field_search) |
            Q(unaccented_name__icontains=field_search),
            **query
        ).order_by('-id').paginate(page=page, per_page=PER_PAGE)
    else:
        pagination = Blog.objects(**query).order_by('-id').paginate(page=page, per_page=PER_PAGE)

    blogs = pagination.items
    return render_template('admin/blog/manage_blog.html',
                           blogs=blogs,
                           pagination=pagination,
                           params=params,
                           )


@admin.route('/admin/blog/add/', methods=['GET', 'POST'])
@role_required(['Admin', 'User'])
def add_blog():
    new_blog = Blog()
    form = AddBlogForm(new_blog, BlogCategory)
    if form.validate_on_submit():
        new_blog.name = form.name.data
        new_blog.created_by = current_user._get_current_object()
        try:
            category = BlogCategory.objects.get(id=form.category.data)
        except Exception:
            category = None
        new_blog.category = category
        new_blog.save()
        flash("Bài viết đã được thêm mới thành công.", "success")
        return redirect(url_for('admin.edit_blog', blog_id=new_blog.id))

    return render_template('admin/blog/add_blog.html',
                           form=form,
                           )


@admin.route('/admin/blog/edit/<blog_id>/', methods=['GET', 'POST'])
@role_required(['Admin', 'User'])
def edit_blog(blog_id):
    blog = Blog.objects.get_or_404(id=blog_id)
    new_image = BlogMedia()
    user = current_user._get_current_object()
    form = EditBlogForm(blog, new_image, BlogCategory)
    if form.validate_on_submit():
        blog.name = form.name.data
        blog.excerpt = form.excerpt.data
        blog.content = form.content.data
        blog.published = form.published.data
        if form.link_video.data:
            blog.link_video = form.link_video.data
        if bool(form.published.data) is True:
            blog.published_at = dt.now()
            blog.published_by = user
        try:
            category = BlogCategory.objects.get(id=form.category.data)
        except Exception:
            category = None
        blog.category = category
        blog.updated_by = user
        blog.updated_at = dt.now()
        image_file = form.image.data
        if image_file and image_file.filename:
            content_type = image_file.content_type
            original_filename = image_file.filename
            file_extension = image_file.filename.split('.')[1]
            if 'image' in request.form and request.form.get('image'):
                try:
                    image = BlogMedia.objects(id=request.form.get('image')).first()
                except Exception:
                    image = None
                if image:
                    image.original_filename = original_filename
                    image.file_extension = file_extension
                    image.content_type = content_type
                    image.updated_by = user
                    image.file.replace(image_file, content_type=content_type)
                    image.save()
            else:
                new_image.original_filename = original_filename
                new_image.file_extension = file_extension
                new_image.content_type = content_type
                new_image.created_by = user
                new_image.file.put(image_file, content_type=content_type)
                new_image.save()
                blog.image = new_image
        blog.save()
        flash("Cập nhật bài viết thành công!", "success")
        return redirect(request.url)

    form.name.data = blog.name
    form.excerpt.data = blog.excerpt
    form.category.data = str(blog.category.id) if blog.category else None
    form.published.data = blog.published
    form.content.data = blog.content
    form.link_video.data = blog.link_video

    return render_template('admin/blog/edit_blog.html',
                           form=form,
                           blog=blog,
                           )


@admin.route('/admin/blog/preview/<blog_id>/', methods=['GET', 'POST'])
@role_required(['Admin', 'User', 'Manager'])
def preview(blog_id):
    post = Blog.objects.get_or_404(id=blog_id)
    return render_template('admin/blog/preview.html',
                           post=post,
                           )


@admin.route('/admin/blog/image/<uid>/', methods=['GET'])
def serve_blog_image(uid):
    return _handle_render_file(BlogMedia, **{'uid': uid})