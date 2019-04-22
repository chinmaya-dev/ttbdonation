from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField, IntegerField, RadioField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

class InputTextForm(FlaskForm):
  inputText = TextAreaField(validators=[DataRequired()])

class SearchForm(FlaskForm):
    q = StringField(('Search Stories & People'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)

class BoostForm(FlaskForm):
    action = SelectField('Select where to send people ', choices=[('Your Profile', 'Your Profile'), (
        'Your Website', 'Your Website'), ('Your StoreFront', 'Your StoreFront'), ('Your Direct Messages', 'Your Direct Messages')])
    target_audience = SelectField('Target Category', choices=[('Music', 'Music'), ('Peoples Corner', 'Peoples Corner'), (
        'Travel', 'Travel'), ('Design', 'Design'), ('Sports', 'Sports'), ('Others', 'others..')])
    amount = SelectField('Set average budget per day', choices=[('10', 'Basic(10 Rs/per day average)'), (
        '100', 'Advance(100 Rs/per day average)'),
        ('1000', 'Premium(1000 Rs/per day average)')])
    end_date = DateField(' Ending Date ')

    submit = SubmitField('Confirm')
