from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User
from .. import db, bcrypt





class SignUpForm(FlaskForm):
    username = StringField(('Username'),
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    tandc = BooleanField('Accept our terms and condition', validators=[DataRequired()] )
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class WelcomeForm(FlaskForm):
    is_role = SelectField('How would you like to join us ?', choices = [('Creators','Creators'),('Brand','Brand'), ('Mentor','Mentor')], validators=[DataRequired()])
    submit = SubmitField('Next')

class WTKForm(FlaskForm):
    issues = StringField('what are your current issues ?')
    support = StringField('What kind of support you are looking for ?')
    submit = SubmitField('Next')

class ProtagonistCatForm(FlaskForm):
    category = SelectField('please choose a category in order to continue', choices = [('Music', 'Music'),('Peoples Corner', 'Peoples Corner'),('Travel','Travel'),('Design','Design'),('Sports','Sports'),('Adventure Sports','Adventure Sports'),('Others','others..')])
    submit = SubmitField('Next')

class ProtagonistSubCatMusicForm(FlaskForm):
    sub_category = RadioField('please select a sub category', choices = [('Alternative Music','Alternative Music'),('Blues','Blues'),('Classical Music','Classical Music'),('Country Music','Country Music'),(' Electronic',' Electronic'),('Hip Hop','Hip Hop'),('Rap','Rap'),('Jazz','Jazz'),('Pop','Pop'),('R&B','R&B'),('Latin','Latin'),('Rock','Rock')])
    submit = SubmitField('done')

class ProtagonistSubCatSportsForm(FlaskForm):
    sub_category = RadioField('please select a sub category', choices = [('Archery','Archery'),('Athletics','Athletics'),('Badminton','Badminton'),('Canoe','Canoe'),('Cycling','Cycling'),('Dartchery','Dartchery'),('Equestrian','Equestrian'),('Football','Football'),('Goalball','Goalball'),('Ice Sledge Racing','Ice Sledge Racing'),('Alpine skiing','Alpine skiing'),('Biathlon','Biathlon')])
    submit = SubmitField('done')

class ProtagonistSubCatASportsForm(FlaskForm):
    sub_category = RadioField('please select a sub category', choices = [('Archery','Archery'),('Athletics','Athletics'),('Badminton','Badminton'),('Canoe','Canoe'),('Cycling','Cycling'),('Dartchery','Dartchery'),('Equestrian','Equestrian'),('Football','Football'),('Goalball','Goalball'),('Ice Sledge Racing','Ice Sledge Racing'),('Alpine skiing','Alpine skiing'),('Biathlon','Biathlon')])
    submit = SubmitField('done')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('continue')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email. You must register first.')
class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')
    
    def validate_email(self, password):
        user = User.query.filter_by(password=password.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
