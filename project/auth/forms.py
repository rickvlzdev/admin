from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, \
                               ValidationError, Regexp, Length
from project.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField(
      'Username', validators=[
        DataRequired(),
        Regexp(
          "^[a-zA-Z0-9_.-]+$",
          message=("Username must only have letters"
                   " , numbers, underscores, periods, "
                   " or hyphens.")),
        Length(min=8, max=15)])
    email = StringField(
      'Email', validators=[
        DataRequired(),
        Email(), Length(max=50)])
    password = PasswordField(
      'Password', validators=[
        DataRequired(),
        Length(min=8, max=128,
               message='Field must be at least 8 characters long.')])
    password_repeat = PasswordField(
      'Confirm password', validators=[
        DataRequired(),
        EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use another username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use another email address.')


class RequestPasswordResetForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
      'Password', validators=[
        DataRequired(),
        Length(min=8, max=128,
               message='Field must be at least 8 characters long.')])
    password_repeat = PasswordField('Confirm password',
                                    validators=[DataRequired(),
                                                EqualTo('password')])
    submit = SubmitField('Reset password')
