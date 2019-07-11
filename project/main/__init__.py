from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from project.main.forms import EditProfileForm, ChangePasswordForm
from project import db

bp = Blueprint('main', __name__, template_folder='./templates')

@bp.route('/')
@login_required
def index():
  return render_template('index.html')
  
@bp.route('/profile')
@login_required
def profile():
  return render_template('profile.html')

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
  form = EditProfileForm()
  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.email = form.email.data
    current_user.first_name = form.first_name.data
    current_user.last_name = form.last_name.data
    db.session.commit()
    flash('Profile updated.')
  return render_template('edit_profile.html', form=form)

@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
  form = ChangePasswordForm()
  if form.validate_on_submit():
    current_user.set_password(form.password.data)
    db.session.commit()
    flash('Successfully changed password.')
  return render_template('change_password.html', form = form)
