from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, BooleanField, SelectField, SubmitField, TextAreaField, validators

class reportForm(FlaskForm):
    lifestyle = SelectField('Lifestyle')
    outdoors = SelectField('Outdoors')
    sleep = SelectField('Sleep')
    submit = SubmitField('Generate Report')
