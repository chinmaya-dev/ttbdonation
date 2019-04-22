from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, RadioField, IntegerField, SelectField, FloatField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_ckeditor import CKEditorField
from app.models import User, Address, Occupation, Links, Intrest, Achievement, Travel, Special_event,  Update, UpdateComment, Media, Sports




class UpdateAccountRoleForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = StringField('About you')
    #role_in_brand = SelectField('Your Designation', choices=[('Brand Manager', 'Brand Manager'), ('Brand Strategiest', ' Brand Strategiest'), ('Marketing Manager', 'Marketing Manager'), (' Media Aegency', ' Media Aegency'), ('Executive Officer', 'Executive Officer'),  ('Others', 'Others')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    web_url = StringField('Website URL')
    language = StringField('Language', validators=[DataRequired()])
    category = SelectField('please choose a category in order to continue', choices=[('Music', 'Music'), ('Peoples Corner', 'Peoples Corner'), (
        'Travel', 'Travel'), ('Design', 'Design'), ('Sports', 'Sports'), ('Adventure Sports', 'Adventure Sports'), ('Others', 'others..')], validators=[DataRequired()])
    gender = SelectField('Gender', choices=[
                         ('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], validators=[DataRequired()])
    contact_number = IntegerField("Phone Number", validators=[DataRequired()])
    education_level = SelectField('Your education level', choices=[('High school', 'High School'), (
        'Under Graduation', 'Under Graduation'), ('Post Graduation', 'Post Graduation'), ('Diploma', 'Diploma'), ('Ph.D', 'Ph.D')], validators=[DataRequired()])
    date_of_birth = DateField(
        'Date of Birth', format="%Y-%m-%d", validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != User.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_username(self, email):
        if email.data != User.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')

class UpdateAccountForm(FlaskForm):
    is_role = SelectField('Your role', choices=[(
        'Creators', 'Creators'), ('Brand', 'Brand'), ('Mentor', 'Mentor')], validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = StringField('About you', validators=[DataRequired()])
    #role_in_brand = SelectField('Your Designation', choices=[('Brand Manager', 'Brand Manager'), ('Brand Strategiest', ' Brand Strategiest'), ('Marketing Manager', 'Marketing Manager'), (' Media Aegency', ' Media Aegency'), ('Executive Officer', 'Executive Officer'),  ('Others', 'Others')])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')    
    web_url = StringField('Website URL')
    language = StringField('Language')
    category = SelectField('please choose a category in order to continue', choices=[('Music', 'Music'), ('Peoples Corner', 'Peoples Corner'), (
        'Travel', 'Travel'), ('Design', 'Design'), ('Sports', 'Sports'), ('Adventure Sports', 'Adventure Sports'), ('Others', 'others..')])
    gender = SelectField('Gender', choices = [('Male','Male'), ('Female','Female'), ('Neutral','Neutral')])
    contact_number = IntegerField("Phone Number", validators=[DataRequired()])
    education_level = SelectField('Your education level', choices = [('High school', 'High School'), ('Under Graduation', 'Under Graduation'), ('Post Graduation', 'Post Graduation'), ('Diploma', 'Diploma'), ('Ph.D', 'Ph.D')])
    date_of_birth = DateField('Date of Birth', format="%Y-%m-%d")
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != User.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_username(self, email):
        if email.data != User.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class UpdateBrandRoleForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = StringField('About you')
    company_name = StringField('Company Name', validators=[DataRequired()])
    brand_name = StringField('Brand Name', validators=[DataRequired()])
    web_url = StringField('Website URL', validators=[DataRequired()])
    available_for_sponsorship = SelectField('Available for Sponsorship', choices=[('Yes', 'Yes'), ('No', 'No')])
    contact_number = IntegerField("Phone Number", validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != User.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_username(self, email):
        if email.data != User.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class UpdateBrandAccountForm(FlaskForm):
    is_role = SelectField('Your role', choices=[(
        'Creators', 'Creators'), ('Brand', 'Brand'), ('Mentor', 'Mentor')], validators=[DataRequired()])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = StringField('About you', validators=[DataRequired()])
    company_name = StringField('Company Name')
    brand_name = StringField('Brand Name')
    web_url = StringField('Website URL')
    available_for_sponsorship = SelectField('Available for Sponsorship', choices=[('Yes', 'Yes'), ('No', 'No')])
    contact_number = IntegerField("Phone Number", validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != User.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_username(self, email):
        if email.data != User.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')


class SportsForm(FlaskForm):
    level_of_playing = SelectField('Level', choices = [('District','District'),('State','State'),('National','National'),('International','International')])
    current_team = StringField('Current team')
    tournament = StringField('Tournament Participated')
    submit = SubmitField('Update')


class AddressForm(FlaskForm):
    street = StringField('Street Address')
    city = StringField('City')
    zip_code = StringField('Zip Code')
    country = StringField('Country')
    submit = SubmitField('Update')

class OccupationForm(FlaskForm):
    occupation_name = StringField('occupation name')
    occupation_company = StringField(' occupation company ')
    occupation_start_date = DateField('Start Date', format="%Y-%m-%d")
    occupation_end_date = DateField('End Date', format="%Y-%m-%d")
    submit = SubmitField('Update')


class LinksForm(FlaskForm):
    facebook_id = StringField('link Facebook')
    twitter_id = StringField('Link Twitter')
    instagram_id = StringField(' Link Instagram ')
    snapchat_id = StringField(' Link Snapchat ')
    submit = SubmitField('Update')

class BrandBriefForm(FlaskForm):
    business_description = StringField('Business Description')
    brand_psychology = StringField(' Brand Psychology ')
    current_market_perception = StringField(' Current Market Perception ')
    brand_goals = StringField('Brand Goals')
    submit = SubmitField('Update')

class IntrestForm(FlaskForm):
    intrest_type = StringField('Intrest name')
    submit = SubmitField('Update')

class AchievementForm(FlaskForm):
    medal_count = StringField('medal')
    timestamp = DateField(' Date', format="%Y-%m-%d")
    submit = SubmitField('Update')

class EventsForm(FlaskForm):
    event_name = StringField('Event Name')
    event_type = SelectField('Type', choices=[('Public', 'Public'), ('Private', 'Private')])
    event_description = CKEditorField('Description')
    event_location = StringField('location')
    event_links = StringField('Related links')
    event_category = SelectField('Category', choices=[('Beauty & Fashion', 'Beauty & Fashion'), ('Gaming & Apps', 'Gaming & Apps'), (
        'Health & Fitness', 'Health & Fitness'), ('Tech', 'Tech'), ('Entertainment', 'Entertainment'), ('Others', 'Others')])
    picture = FileField('Upload pictures', validators=[FileAllowed(['jpg', 'png'])])
    event_start_date = DateField(' Start Date', format="%Y-%m-%d")
    event_end_date = DateField(' End Date', format="%Y-%m-%d")
    event_frequency = SelectField('Frequency', choices=[('Once', 'Once'), ('Daily', 'Daily'), (
        'Once in a week', 'Once in a week'), ('Once in a month', 'Once in a month'), ('Once in a Year', 'Once in a Year'), ('After every 4 Years', 'After 4 Years')])
    submit = SubmitField('Post')

class TravelForm(FlaskForm):
    place = StringField('location')
    start_date = DateField(' Start Date', format="%Y-%m-%d")
    end_date = DateField(' End Date', format="%Y-%m-%d")
    submit = SubmitField('Update')

class Special_eventForm(FlaskForm):
    life_event = StringField('Discription')
    life_event_start_date = DateField(' Start Date', format="%Y-%m-%d")
    life_event_end_date = DateField(' End Date', format="%Y-%m-%d")
    submit = SubmitField('Update')


class SocialDashForm(FlaskForm):
    likes = IntegerField('Likes')
    views = IntegerField('Views')
    share = IntegerField('Share')
    comment = IntegerField('Comment')
    category = StringField('Category')
    engagments = FloatField('engagments')
    submit = SubmitField('Update')

class MediaForm(FlaskForm):
    image = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    media_format = SelectField('Media type ', choices = [('image', 'image')])
    submit = SubmitField('upload')

class BioForm(FlaskForm):
    goal = TextAreaField("What's your goal in life")
    hurdles = TextAreaField("Hurdles You are facing")
    rank = SelectField('How Do You rank yourself out of 10 ?', choices=[('1', '1'), ('2', '2'), (
        '3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])
    accomplished = SelectField('How much of your goal have you accomplished ?', choices=[('10%', '10'), ('20%', '20'), (
        '30%', '30'), ('40%', '40'), ('50%', '50'), ('60%', '60'), ('70%', '70'), ('80%', '80'), ('90%', '90'), ('100%', '100')])
    fear = TextAreaField("What are your biggest fear in the life ?")
    finance = SelectField('Do you need financial support', choices=[('Yes', 'Yes'), ('No', 'No')])
    market = SelectField('Marketing support ?', choices=[('Yes', 'Yes'), ('No', 'No')])
    other = TextAreaField("Any other kind of support ?")
    motivate = TextAreaField("What keeps you motivated ?")
    submit = SubmitField('Submit')
class UpdateForm(FlaskForm):
    update_text = StringField('Write something here ...', validators=[DataRequired()])
    picture = FileField("", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("")

class UpdateCommentForm(FlaskForm):
    body = StringField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')


class FAQForm(FlaskForm):
    que = StringField(
        'Generally Asked Questions about Your Project ?', validators=[DataRequired()])
    ans = StringField("it's solution", validators=[DataRequired()])
    submit = SubmitField('Submit')
