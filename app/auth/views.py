from flask import render_template, url_for, flash, redirect
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from .. models import Employee


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle request to the /register route
    Add an employee to the database through the registration form
    :return:
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        # Add employee to the database
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully registered, you may now log in')

        # Redirect to the log in page
        return redirect(url_for('auth.login'))

    # Load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle request to the /login route
    Load an employee through the login form
    :return:
    """
    form = LoginForm()
    # Check whether employee exists in the database and
    # whether the password matches the one in the database
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(form.password.data):
            # Login the user
            login_user(employee)
            # redirect to the appropriate dashboard page
            if employee.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))
        # When login details are incorrect
        else:
            flash('Invalid email or password')
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle the request to /logout route
    Log an employee out throught the logout link
    :return:
    """
    logout_user()
    flash('You have been successfully logged out')
    # Redirect to log in page
    return redirect(url_for('auth.login'))
