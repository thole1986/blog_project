from flask import Flask, redirect, url_for, request
from flask_caching import Cache
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_babel import Babel, lazy_gettext as _l
from flask_mail import Mail
from flask_moment import Moment
from flask_mongoengine import MongoEngine
from config import config


login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.login_message = _l('Vui lòng đăng nhập để tiếp tục.')
login_manager.login_message_category = 'warning'
db = MongoEngine()
mail = Mail()
moment = Moment()
babel = Babel()
csrf = CSRFProtect()
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('user.login', next=request.url))


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)

    from apps.errors import errors as errors_blueprint
    from apps.controllers.admin import admin as admin_blueprint
    from apps.controllers.main import main as main_blueprint
    from apps.controllers.blog import blog as blog_blueprint
    from apps.controllers.user import user as user_blueprint
    from apps.controllers.common import common as common_blueprint
    from apps.filters import filters as filter_blueprint

    app.register_blueprint(errors_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(blog_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(common_blueprint)
    app.register_blueprint(filter_blueprint)

    if not app.debug and not app.testing:
        pass
        # if app.config['MAIL_SERVER']:
        #     auth = None
        #     if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        #         auth = (app.config['MAIL_USERNAME'],
        #                 app.config['MAIL_PASSWORD'])
        #     secure = None
        #     if app.config['MAIL_USE_TLS']:
        #         secure = ()
        #     mail_handler = SMTPHandler(
        #         mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        #         fromaddr='no-reply@' + app.config['MAIL_SERVER'],
        #         toaddrs=app.config['ADMINS'], subject='TechSolution Failure',
        #         credentials=auth, secure=secure)
        #
        #     mail_handler.setLevel(logging.ERROR)
        #     app.logger.addHandler(mail_handler)
        #
        # if app.config.get('LOG_TO_STDOUT', None):
        #     stream_handler = logging.StreamHandler()
        #     stream_handler.setLevel(logging.INFO)
        #     app.logger.addHandler(stream_handler)
        # else:
        #     if not os.path.exists('logs'):
        #         os.mkdir('logs')
        #
        #     file_handler = RotatingFileHandler('logs/techsolution.log',
        #                                        maxBytes=10240, backupCount=10)
        #     file_handler.setFormatter(logging.Formatter(
        #         '%(asctime)s %(levelname)s: %(message)s '
        #         '[in %(pathname)s:%(lineno)d]'))
        #     file_handler.setLevel(logging.INFO)
        #     app.logger.addHandler(file_handler)
        #
        # app.logger.setLevel(logging.INFO)
        # app.logger.info('TechSolution startup')

    return app