from flask import render_template, request, redirect, url_for, abort
from mongoengine import Q
from unidecode import unidecode
from . import blog
from apps.models.blog import Blog, BlogCategory
from ...constant.common import DEFAULT_PAGE, PER_PAGE, NOT_FOUND_CODE
from ...utils.shared import clean_string


@blog.route('/danh-sach-bai-viet/', defaults={'path': ''}, methods=['GET'])
@blog.route('/danh-sach-bai-viet/<path:path>', methods=['GET'])
def list_blog(path):
    try:
        page = int(request.args.get('page', DEFAULT_PAGE))
    except (TypeError, ValueError):
        page = DEFAULT_PAGE
    params = {}
    if request.method == 'GET':
        for k, v in request.args.items():
            if k not in ['page']:
                params[k] = str(v).strip()
    category = None
    if params.get('category'):
        name = params.get('category')
        combination_fields = Q(**{'name__icontains': name}) | Q(
            **{'unaccented_name__icontains': unidecode(name)}
        ) | Q(**{'slug': name})
        category = BlogCategory.objects(combination_fields).first()
        if category:
            categories = category.all_children(True)
            pagination = Blog.objects(category__in=[str(cat.id) for cat in categories], published=True).order_by('-id').paginate(
                page=page,
                per_page=PER_PAGE
            )
        else:
            return abort(NOT_FOUND_CODE)
    else:
        pagination = Blog.objects(published=True).order_by(
            '-id'
        ).paginate(page=page, per_page=PER_PAGE)

    blogs = pagination.items 

    return render_template('ui_front/blog/list_blog.html',
                           blogs=blogs,
                           pagination=pagination,
                           params=params,
                           category=category,
                           )


@blog.route('/<slug>', methods=['GET'])
def blog_detail(slug):
    post = Blog.objects.get_or_404(slug=slug, published=True)
    # page.count_view()

    return render_template('web_ui/post.html',
                           post=post,
                           )


@blog.route('/ket-qua-tim-kiem/', defaults={'path': ''}, methods=['GET', 'POST'])
@blog.route('/ket-qua-tim-kiem/<path:path>', methods=['GET', 'POST'])
def search_result(path):
    try:
        page = int(request.args.get('page', DEFAULT_PAGE))
    except (TypeError, ValueError):
        page = DEFAULT_PAGE
    params = {}
    query = {
        'published': True,
    }
    if request.method == 'GET':
        for k, v in request.args.items():
            if k not in ['page']:
                params[k] = str(v).strip()
    if request.method == 'POST':
        for k, v in request.form.items():
            if k != 'csrf_token' and v:
                params[k] = v
        return redirect(url_for('blog.search_result', **params))

    if params.get('q') and clean_string(params.get('q')):
        field_search = clean_string(params.get('q'))
        combination_fields = Q(**{'title__icontains': field_search}) | Q(
            **{'unaccented_title__icontains': unidecode(field_search)})
        pagination = Blog.objects(combination_fields, **query).order_by('-id').paginate(
            page=page,
            per_page=PER_PAGE
        )
    else:
        pagination = Blog.objects().order_by(
            '-id'
        ).paginate(page=page, per_page=PER_PAGE)
    blogs = pagination.items
    return render_template('ui_front/blog/search_result.html',
                           blogs=blogs,
                           params=params,
                           pagination=pagination,
                           )
