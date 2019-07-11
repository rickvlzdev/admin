from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, ValidationError, DataRequired, EqualTo
from project.models import User

class EditProfileForm(FlaskForm):
  username = StringField('username', validators=[DataRequired()])
  email = StringField('email', validators=[DataRequired(), Email()])
  first_name = StringField('first name', validators=[DataRequired()])
  last_name = StringField('last name', validators=[DataRequired()])
  submit = SubmitField('update profile')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user and (user.username != current_user.username):
      raise ValidationError('Please choose a different username.')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user and (user.email != current_user.email):
      raise ValidationError('Please choose a different email address.')

class ChangePasswordForm(FlaskForm):
  current_password = PasswordField('current password', validators=[DataRequired()])
  password = PasswordField('new password', validators=[DataRequired()])
  password_repeat = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('change password')

  def validate_current_password(self, current_password):
    if not current_user.check_password(current_password.data):
      raise ValidationError('Please enter your current password.')
