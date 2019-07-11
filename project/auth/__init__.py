from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user
from project import db
from project.models import User
from project.auth.forms import LoginForm, RegistrationForm, RequestPasswordResetForm, ResetPasswordForm
from project.auth.email import send_password_reset_email

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

@bp.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Successful registration. Please sign in.')
    return redirect(url_for('auth.login'))
  elif request.method == 'POST':
    flash('Invalid information.')
  return render_template('register.html', form=form)

@bp.route('/request_password_reset', methods=['GET', 'POST'])
def request_password_reset():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  form = RequestPasswordResetForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user:
      send_password_reset_email(user)
    flash('Check your email for the instructions to reset your password.')
    return redirect(url_for('auth.login'))
  return render_template('request_password_reset.html', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  user = User.verify_reset_password_token(token)
  if not user:
    return redirect(url_for('auth.login'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
    user.set_password(form.password.data)
    db.session.commit()
    flash('You password has been reset.')
    return redirect(url_for('auth.login'))
  return render_template('reset_password.html', form=form)
  