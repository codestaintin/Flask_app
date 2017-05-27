from flask import abort, render_template
from flask_login import current_user, login_required
from .import home
from ..models import Employee


@home.route('/')
def homepage():
    """
    Render the home page on the / route
    :return:
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Return the dashboard page on the /dashboard
    :return:
    """
    return render_template('home/dashboard.html', title="Dashboard")


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Prevent none admin from accessing this page
    if not current_user.is_admin:
        abort(403)
    return render_template('home/admin_dashboard.html', title="Dashboard")

