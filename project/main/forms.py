from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import Email, ValidationError, DataRequired, \
                               EqualTo, Length, Regexp
from project.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                           Regexp("^[a-zA-Z0-9_.-]+$",
                                  message=("Username must only have letters"
                                           " , numbers, underscores, periods,"
                                           " or hyphens.")),
                           Length(min=8, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email(),
                        Length(max=50)])
    first_name = StringField('First name')
    last_name = StringField('Last name')
    about_me = TextAreaField('About me', validators=[Length(max=500)])
    submit = SubmitField('Update profile')

    def __init__(self, original_username, original_email, original_about_me,
                 *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please choose a different username.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError(('Please choose a different'
                                       'email address.'))


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('current password',
                                     validators=[DataRequired()])
    password = PasswordField('new password', validators=[DataRequired(),
                             Length(min=8, max=128, message=('Field must be at'
                                    ' least 8 characters long.'))])
    password_repeat = PasswordField('confirm password', validators=[
                                    DataRequired(),
                                    EqualTo('password')])
    submit = SubmitField('change password')

    def __init__(self, current_user, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.current_user = current_user

    def validate_current_password(self, current_password):
        if not self.current_user.check_password(current_password.data):
            raise ValidationError('Incorrect password.')
