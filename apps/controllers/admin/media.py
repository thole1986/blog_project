from flask import request, url_for, redirect, render_template
from . import admin
from apps.decorators import role_required
from ...constant.common import PER_PAGE, DEFAULT_PAGE


@admin.route('/admin/media/product/manage/', methods=['GET', 'POST'])
@role_required(['Admin'])
def manage_product_image():
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
        return redirect(url_for('admin.manage_product_image', **params))
    if params.get('search'):
        field_search = params.get('search')
        pagination = ProductImage.objects(
            original_filename__icontains=field_search
        ).order_by('-id').paginate(page=page, per_page=PER_PAGE)
    else:
        pagination = ProductImage.objects().order_by('-id').paginate(page=page, per_page=PER_PAGE)

    images = pagination.items
    return render_template('pages/admin/media/product/manage_product_image.html',
                           pagination=pagination,
                           images=images,
                           params=params,
                           )