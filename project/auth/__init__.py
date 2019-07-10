from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user
from project.auth.forms import LoginForm
from project.models import User

bp = Blueprint('auth', __name__, template_folder='./templates')

@bp.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password.')
      return render_template('login.html', form=form)
    login_user(user, remember=form.remember_me.data)
    return redirect(url_for('main.index'))
  return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('auth.login'))