from flask import url_for, render_template, jsonify, g, \
    current_app, request, abort
from mongoengine import Q
from unidecode import unidecode

from . import main
from .forms import SearchForm, ContactForm
from apps.constant.common import SUCCESS_CODE, BAD_REQUEST_CODE, DEFAULT_PAGE, PER_PAGE, NOT_FOUND_CODE
from ...models.blog import BlogCategory, Blog
from ...send_mail import send_email


@main.before_app_request
def before_request():
    g.search_form = SearchForm()


@main.route('/', methods=['GET'])
def index():
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

    next_url = url_for('main.index', page=pagination.next_num) \
        if pagination.has_next else None
    prev_url = url_for('main.index', page=pagination.prev_num) \
        if pagination.has_prev else None

    blogs = pagination.items
    return render_template('web_ui/index.html',
                           blogs=blogs,
                           next_url=next_url,
                           prev_url=prev_url,
                           )


@main.route('/lien-he', methods=['GET'])
def contact_us():
    form = ContactForm()
    return render_template('pages/main/contact.html',
                           form=form,
                           )


@main.route('/ve-chung-toi', methods=['GET'])
def about_us():
    return render_template('pages/main/about_us.html')


@main.route('/contact/send/', methods=['POST'])
def send_contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        title = form.title.data
        phone = form.phone.data
        email = form.email.data
        description = form.description.data
        send_email(current_app.config['MAIL_SERVICE'], title,
                   'pages/main/__mail-contact',
                   name=name,
                   phone=phone,
                   email=email,
                   description=description,
                   )
        return jsonify({
            'status_code': SUCCESS_CODE,
            'url': url_for('main.mail_success_page'),
        })
    else:
        return {
            'status_code': BAD_REQUEST_CODE,
            'errors': form.errors,
        }


@main.route('/gui-thu-thanh-cong', methods=['GET'])
def mail_success_page():
    return render_template('pages/main/mail_success.html')