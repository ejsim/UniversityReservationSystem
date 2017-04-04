from flask_wtf import Form
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from wtforms.fields import PasswordField, StringField, SubmitField, DateField, DateTimeField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length, NumberRange

from .. import db
from ..models import *

class ReserveSpaceForm(Form):
    campus = QuerySelectField(
        'Campus*',
        get_label='name',
        validators=[InputRequired()],
        query_factory=lambda: db.session.query(Campus).order_by('name'),
        id='select_campus')
    space_type = QuerySelectField(
        'Space Type*',
        get_label='name',
        validators=[InputRequired()],
        query_factory=lambda: db.session.query(Space_Type).order_by('name'),
        id='select_space_type')
    capacity = StringField('Capacity', [NumberRange(min=1, max=10000, message='Capacity not valid')])
    ammenities = QuerySelectMultipleField(
        'Ammmenities',
        validators=[],
        get_label='name',
        query_factory=lambda: db.session.query(Ammenity_Type).order_by('name'),
        id='select_space_ammenities')
    start_time = DateTimeField(
        'Start Time', format='%H:%M')
    end_time = DateTimeField(
        'End Time', format='%H:%M')
    search = SubmitField('Search')
