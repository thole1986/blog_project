import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TEMPLATES_AUTO_RELOAD = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
                   ['true', 'on', '1']
    MAIL_USERNAME = ''
    MAIL_SERVICE = ''
    MAIL_PASSWORD = ''
    MAIL_SUBJECT_PREFIX = '[KenKool]'
    ADMIN_PER_PAGE = 20
    UPLOADS = os.path.join(basedir, "apps" + os.sep + "uploads" + os.sep)
    DATA_IMPORT = os.path.join(basedir, "data" + os.sep)

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'DB': 'demodb',
        'host': os.environ.get('MONGO_HOST') or 'localhost',
    }


class ProductionConfig(Config):
    DEBUG = False
    MONGODB_SETTINGS = {
        'db': os.environ.get('MONGO_DBNAME'),
        'host': os.environ.get('MONGO_HOST'),
        'port': int(os.environ.get('MONGO_PORT') or '27017'),
        'username': os.environ.get('MONGODB_USERNAME'),
        "password": os.environ.get('MONGODB_PASSWORD'),
        'authentication_source': os.environ.get('AUTHENTICATION_SOURCE')
    }


config = {
    'development': DevConfig,
    'production': ProductionConfig,
    'default': DevConfig,
}
