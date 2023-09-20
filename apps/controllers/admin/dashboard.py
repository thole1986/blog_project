from flask import render_template
from . import admin
from apps.decorators import role_required
from apps.models.user import User


@admin.route('/admin/', methods=['GET'])
@role_required(['Admin'])
def admin_dashboard():
    total_user = User.objects().count()

    return render_template('admin/dashboard.html',
                           total_user=total_user,
                           )
