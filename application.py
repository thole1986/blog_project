import os
from dotenv import load_dotenv
from flask_login import current_user
from apps.menu import render_menu

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


from apps import create_app, cache
from apps.models import *

app = create_app(os.getenv('FLASK_ENV') or 'default')


@app.context_processor
def render_menus_to_template():
    return {
        'menus': render_menu()
    }


@app.context_processor
def inject_user_to_template():
    return {
        'user': current_user._get_current_object()
    }


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Role': Role,
        'Profile': Profile,
    }


@app.cli.command()
def deploy():
    # Create admin role
    Role.create_admin_role()
    # Create user admin


@app.cli.command('clear_cache')
def clear_cache():
    with app.app_context():
        cache.clear()

