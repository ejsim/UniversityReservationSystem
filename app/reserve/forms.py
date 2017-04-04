from flask_wtf import Form
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import PasswordField, StringField, SubmitField, DateTimeField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from .. import db
from ..models import *

class ReserveSpaceForm(Form):
    event_name = StringField(
        'Event Name', validators=[InputRequired(), Length(1, 2003)])
    location = QuerySelectField(
        'Location',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Location).order_by('name'))
    space = QuerySelectField(
        'Space',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Space).order_by('name'))
    start_time = DateTimeField(
        'Start Time', format='%H:%M')
    end_time = DateTimeField(
        'End Time', format='%H:%M')
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
