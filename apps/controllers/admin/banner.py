import os
from datetime import datetime as dt
from flask import request, url_for, redirect, render_template, jsonify, flash
from flask_login import current_user
from mongoengine import Q, DoesNotExist
from . import admin
from apps.decorators import role_required
from apps.constant.common import PER_PAGE, DEFAULT_PAGE, NOT_FOUND_CODE, BAD_REQUEST_CODE, SUCCESS_CODE, \
    ALREADY_FOUND_CODE, MAIN_BANNER_IMAGE_UPLOAD_FOLDER, SUB_BANNER_IMAGE_UPLOAD_FOLDER
from apps.models.banner import MainBanner, SubBanner, BannerMedia
from .forms.banner_forms import AddBannerForm, AddBannerImage, EditBannerImage, EditBannerForm


@admin.route('/admin/banner/main/manage/', defaults={'path': ''}, methods=['GET', 'POST'])
@admin.route('/admin/banner/main/manage/<path:path>', methods=['GET', 'POST'])
@role_required(['Admin', 'Staff'])
def manage_main_banner(path):
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
        return redirect(url_for('admin.manage_main_banner', **params))

    query = {
        'is_removed': False,
    }
    if params.get('search'):
        field_search = params.get('search')
        pagination = MainBanner.objects(
            Q(title__icontains=field_search) |
            Q(unaccented_title__icontains=field_search),
            **query,
        ).order_by('-id').paginate(page=page, per_page=PER_PAGE)
    else:
        pagination = MainBanner.objects(**query).order_by('-id').paginate(page=page, per_page=PER_PAGE)
    banners = pagination.items
    form = AddBannerForm()
    return render_template('pages/admin/banner/manage_main_banner.html',
                           banners=banners,
                           pagination=pagination,
                           params=params,
                           form=form,
                           )


@admin.route('/admin/banner/main/add/', methods=['POST'])
@role_required(['Admin', 'Staff'])
def add_main_banner():
    form = AddBannerForm()
    if form.validate_on_submit():
        try:
            main_banner = MainBanner.objects.get(title=form.title.data)
        except DoesNotExist:
            main_banner = MainBanner(
                title=form.title.data
            ).save()
            flash('Thêm mới banner chính thành công!', 'success')
            return jsonify({
                'status_code': SUCCESS_CODE,
                'url_edit': url_for('admin.edit_main_banner', banner_id=main_banner.id)
            })
        if main_banner:
            return jsonify({
                'status_code': ALREADY_FOUND_CODE,
                'msg': 'Tiêu đề banner đã tồn tại!'
            })
    else:
        return jsonify({
            'status_code': BAD_REQUEST_CODE,
            'errors': form.errors,
        })


@admin.route('/admin/banner/main/edit/<banner_id>/', methods=['GET', 'POST'])
@role_required(['Admin', 'Staff'])
def edit_main_banner(banner_id):
    banner = MainBanner.objects.get_or_404(id=banner_id)
    form_upload = AddBannerImage()
    form = EditBannerForm(banner)
    if form.validate_on_submit():
        banner.title = form.title.data
        if form.published.data and bool(form.published.data) is True:
            banner.published_time = dt.now()
        banner.published = form.published.data
        banner.description = form.description.data
        banner.save()
        flash("Cập nhật thành công!", "success")
        return redirect(request.url)

    form.title.data = banner.title
    form.published.data = banner.published
    form.description.data = banner.description

    return render_template('pages/admin/banner/edit_main_banner.html',
                           banner=banner,
                           form_upload=form_upload,
                           form=form,
                           )


@admin.route('/admin/banner/main/image/add/', methods=['POST'])
@role_required(['Admin', 'Staff'])
def add_main_banner_image():
    try:
        banner = MainBanner.objects.get(id=request.form.get('banner_id'))
    except Exception:
        return jsonify({
            'status_code': NOT_FOUND_CODE,
            'msg': 'Thông tin banner không tìm thấy!'
        })
    user = current_user._get_current_object()
    form_upload = AddBannerImage()
    if form_upload.validate_on_submit():
        image_file = form_upload.file.data
        content_type = image_file.content_type
        original_filename = image_file.filename
        file_extension = image_file.filename.split('.')[1]
        banner_image = BannerMedia(
            original_filename=original_filename,
            content_type=content_type,
            file_extension=file_extension,
            created_by=user,
        ).save()
        new_filename = f'{banner_image.id}.{banner_image.file_extension}'
        image = banner_image.create_folder_upload(
            MAIN_BANNER_IMAGE_UPLOAD_FOLDER + os.sep,
            new_filename
        )
        image_file.save(image)
        banner.background_image = banner_image
        banner.updated_by = user
        banner.updated_at = dt.now()
        banner.save()
        flash("Thêm hình banner thành công!", 'success')
        return jsonify({
            'status_code': SUCCESS_CODE,
        })
    else:
        return jsonify({
            'status_code': BAD_REQUEST_CODE,
            'errors': form_upload.errors,
        })


@admin.route('/admin/banner/main/image/edit/', methods=['POST'])
@role_required(['Admin', 'Staff'])
def edit_main_banner_image():
    user = current_user._get_current_object()
    try:
        banner = MainBanner.objects.get(id=request.form.get('banner_id'))
    except Exception:
        return jsonify({
            'status_code': NOT_FOUND_CODE,
            'msg': 'Thông tin banner không tìm thấy!'
        })
    image_id = request.form.get('image_id')
    try:
        banner_image = BannerMedia.objects.get(id=image_id)
    except Exception:
        return jsonify({
            'status_code': NOT_FOUND_CODE,
            'msg': "Hình banner cần cập nhật không tồn tại!"
        })
    if banner.background_image != banner_image:
        return jsonify({
            'status_code': BAD_REQUEST_CODE,
            'msg': "Yêu cầu cập nhật không hợp lệ!"
        })
    form_upload = EditBannerImage(banner_image)
    if form_upload.validate_on_submit():
        image_file = form_upload.file.data
        new_filename = f'{banner_image.id}.{banner_image.file_extension}'
        image = banner_image.create_folder_upload(
            MAIN_BANNER_IMAGE_UPLOAD_FOLDER + os.sep,
            new_filename
        )
        image_file.save(image)
        banner_image.original_filename = image_file.filename
        banner_image.content_type = image_file.content_type
        banner_image.file_extension = image_file.filename.split('.')[1]
        banner_image.updated_by = user
        banner_image.update_at = dt.now()
        banner_image.save()
        flash("Cập nhật thành công!", 'success')
        return jsonify({
            'status_code': SUCCESS_CODE,
        })
    else:
        return jsonify({
            'status_code': BAD_REQUEST_CODE,
            'errors': form_upload.errors,
        })


@admin.route('/admin/banner/sub/manage/', defaults={'path': ''}, methods=['GET', 'POST'])
@admin.route('/admin/banner/sub/manage/<path:path>', methods=['GET', 'POST'])
@role_required(['Admin', 'Staff'])
def manage_sub_banner(path):
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
        return redirect(url_for('admin.manage_sub_banner', **params))

    query = {
        'is_removed': False,
    }
    if params.get('search'):
        field_search = params.get('search')
        pagination = SubBanner.objects(
            Q(title__icontains=field_search) |
            Q(unaccented_title__icontains=field_search),
            **query,
        ).order_by('-id').paginate(page=page, per_page=PER_PAGE)
    else:
        pagination = SubBanner.objects(**query).order_by('-id').paginate(page=page, per_page=PER_PAGE)
    banners = pagination.items
    form = AddBannerForm()
    return render_template('pages/admin/banner/manage_sub_banner.html',
                           banners=banners,
                           pagination=pagination,
                           params=params,
                           form=form,
                           )


@admin.route('/admin/banner/sub/add/', methods=['POST'])
@role_required(['Admin', 'Staff'])
def add_sub_banner():
    form = AddBannerForm()
    if form.validate_on_submit():
        try:
            sub_banner = SubBanner.objects.get(title=form.title.data)
        except DoesNotExist:
            sub_banner = SubBanner(
                title=form.title.data
            ).save()
            flash('Thêm mới banner thành công!', 'success')
            return jsonify({
                'status_code': SUCCESS_CODE,
                'url_edit': url_for('admin.edit_sub_banner', banner_id=sub_banner.id)
            })
        if sub_banner:
            return jsonify({
                'status_code': ALREADY_FOUND_CODE,
                'msg': 'Tiêu đề banner đã tồn tại!'
            })
    else:
        return jsonify({
            'status_code': BAD_REQUEST_CODE,
            'errors': form.errors,
        })


@admin.route('/admin/banner/sub/edit/<banner_id>/', methods=['GET', 'POST'])
@role_required(['Admin', 'Staff'])
def edit_sub_banner(banner_id):
    banner = SubBanner.objects.get_or_404(id=banner_id)
    form_upload = AddBannerImage()
    form = EditBannerForm(banner)
    if form.validate_on_submit():
        banner.title = form.title.data
        if form.published.data and bool(form.published.data) is True:
            banner.published_time = dt.now()
        banner.published = form.published.data
        banner.description = form.description.data
        banner.save()
        flash("Cập nhật thành công!", "success")
        return redirect(request.url)

    form.title.data = banner.title
    form.published.data = banner.published
    form.description.data = banner.description

    return render_template('pages/admin/banner/edit_sub_banner.html',
                           banner=banner,
                           form_upload=form_upload,
                           form=form,
                           )


@admin.route('/admin/banner/sub/image/add/', methods=['POST'])
@role_required(['Admin', 'Staff'])
def add_sub_banner_image():
    try:
        banner = SubBanner.objects.get(id=request.form.get('banner_id'))
    except Exception:
        return jsonify({
            'status_code': NOT_FOUND_CODE,
            'msg': 'Thông tin banner không tìm thấy!'
        })
    user = current_user._get_current_object()
    form_upload = AddBannerImage()
    if form_upload.validate_on_submit():
        image_file = form_upload.file.data
        content_type = image_file.content_type
        original_filename = image_file.filename
        file_extension = image_file.filename.split('.')[1]
        banner_image = BannerMedia(
            original_filename=original_filename,
            content_type=content_type,
            file_extension=file_extension,
            created_by=user,
        ).save()
        new_filename = f'{banner_image.id}.{banner_image.file_extension}'
        image = banner_image.create_folder_upload(
            SUB_BANNER_IMAGE_UPLOAD_FOLDER + os.sep,
            new_filename
        )
        image_file.save(image)
        banner.background_image = banner_image
        banner.updated_by = user
        banner.updated_at = dt.now()
        banner.save()
        flash("Thêm hình banner thành công!", 'success')
        return jsonify({
            'status_code': SUCCESS_CODE,
        })
    else:
        return jsonify({
            'status_code': BAD_REQUEST_CODE,
            'errors': form_upload.errors,
        })


@admin.route('/admin/banner/sub/image/edit/', methods=['POST'])
@role_required(['Admin', 'Staff'])
def edit_sub_banner_image():
    user = current_user._get_current_object()
    try:
        banner = SubBanner.objects.get(id=request.form.get('banner_id'))
    except Exception:
        return jsonify({
            'status_code': NOT_FOUND_CODE,
            'msg': 'Thông tin banner không tìm thấy!'
        })
    image_id = request.form.get('image_id')
    try:
        banner_image = BannerMedia.objects.get(id=image_id)
    except Exception:
        return jsonify({
            'status_code': NOT_FOUND_CODE,
            'msg': "Hình banner cần cập nhật không tồn tại!"
        })
    if banner.background_image != banner_image:
        return jsonify({
            'status_code': BAD_REQUEST_CODE,
            'msg': "Yêu cầu cập nhật không hợp lệ!"
        })
    form_upload = EditBannerImage(banner_image)
    if form_upload.validate_on_submit():
        image_file = form_upload.file.data
        new_filename = f'{banner_image.id}.{banner_image.file_extension}'
        image = banner_image.create_folder_upload(
            SUB_BANNER_IMAGE_UPLOAD_FOLDER + os.sep,
            new_filename
        )
        image_file.save(image)
        banner_image.original_filename = image_file.filename
        banner_image.content_type = image_file.content_type
        banner_image.file_extension = image_file.filename.split('.')[1]
        banner_image.updated_by = user
        banner_image.update_at = dt.now()
        banner_image.save()
        flash("Cập nhật thành công!", 'success')
        return jsonify({
            'status_code': SUCCESS_CODE,
        })
    else:
        return jsonify({
            'status_code': BAD_REQUEST_CODE,
            'errors': form_upload.errors,
        })