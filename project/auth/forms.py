from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from project.models import User

class LoginForm(FlaskForm):
  username = StringField('username', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired()])
  remember_me = BooleanField('remember me')
  submit = SubmitField('sign in')

class RegistrationForm(FlaskForm):
  username = StringField('username', validators=[DataRequired()])
  email = StringField('email', validators=[DataRequired(), Email()])
  password = PasswordField('password', validators=[DataRequired()])
  password_repeat = PasswordField('repeat password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('register')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      raise ValidationError('Please use a different username.')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
      raise ValidationError('Please use a different email.')

class RequestPasswordResetForm(FlaskForm):
  email = StringField('email', validators=[DataRequired(), Email()])
  submit = SubmitField('send email')

class ResetPasswordForm(FlaskForm):
  password = PasswordField('password', validators=[DataRequired()])
  password_repeat = PasswordField('repeat password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('reset password')