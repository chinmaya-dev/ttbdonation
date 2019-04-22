from flask import request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, IntegerField, SelectField, RadioField, TextField
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class AmountForm(FlaskForm):
  amount = IntegerField('Amount in $',validators=[DataRequired()])
  submit = SubmitField('Donate')

class DonationReasonForm(FlaskForm):
    category = SelectField('Category', choices=[('Art & Culture', 'Art & Culture'), ('Travel for a cause', 'Travel for a cause'), (
        'Sports', 'Sports'), ('Design & Technology', 'Design & Technology'), ('Environment', 'Environment'), ('Defence', 'Defence')])
    title = StringField('Title', validators=[DataRequired()])
    description =  CKEditorField('please give detailed description about your crowdfunding campaign', validators=[DataRequired()])
    short = TextField(
        'please give short description about your crowdfunding campaign', validators=[DataRequired()])
    picture = FileField('Upload pictures', validators=[FileAllowed(['jpg', 'png'])])
    goal = StringField('Goal', validators=[DataRequired()])
    target_amount = IntegerField('Recommended  Amount', validators=[DataRequired()])
    amount_prefilled = IntegerField('Amount prefilled', validators=[DataRequired()])
    end_method = SelectField('Determine how you want complete your campaigns ', choices=[('After goal achieve', 'After goal achieve'), ('After end date', 'After end date')])
    link = StringField('Place YouTube or relevant content link', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DonationCommentForm(FlaskForm):
    body = StringField('Ask a question / Reply ', validators=[DataRequired()])

    submit = SubmitField('Submit')


class DonationUpdateForm(FlaskForm):
    body = StringField('Broadcast an update', validators=[DataRequired()])

    submit = SubmitField('Submit')
