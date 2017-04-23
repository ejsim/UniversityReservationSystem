from flask_wtf import Form
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from wtforms.fields import PasswordField, StringField, SubmitField, DateField, DateTimeField, IntegerField, HiddenField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length, NumberRange, Optional

from .. import db
from ..models import *

class SearchSpaceForm(Form):
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
    capacity = IntegerField('Capacity', [NumberRange(min=1, max=10000, message='Capacity not valid'), Optional()])
    ammenities = QuerySelectMultipleField(
        validators=[],
        get_label='name',
        blank_text=u'-- please choose --',
        allow_blank=True,
        query_factory=lambda: db.session.query(Ammenity_Type).order_by('name'),
        id='select_space_ammenities')
    start_time = DateTimeField(
        'Start Time*', format='%B %d, %Y %I:%M %p')
    end_time = DateTimeField(
        'End Time*', format='%B %d, %Y %I:%M %p')
    search = SubmitField('Search')

class ReserveSpaceForm(Form):
    start_time = HiddenField('Start Time')
    end_time = HiddenField('End Time')
    space_id = HiddenField('Space ID')
    event_name = StringField('Event Name', [InputRequired(), Length(min=1)])
    reserve = SubmitField('Reserve')

class SearchEquipmentForm(Form):
    campus = QuerySelectField(
        'Campus*',
        get_label='name',
        validators=[InputRequired()],
        query_factory=lambda: db.session.query(Campus).order_by('name'),
        id='select_campus')
    equipment_type = QuerySelectField(
        'Equipment Type*',
        get_label='name',
        validators=[InputRequired()],
        query_factory=lambda: db.session.query(Equipment_Type).order_by('name'),
        id='select_equipment_type')
    start_time = DateTimeField(
        'Start Time*', format='%B %d, %Y %I:%M %p')
    end_time = DateTimeField(
        'End Time*', format='%B %d, %Y %I:%M %p')
    search = SubmitField('Search')

class ReserveEquipmentForm(Form):
    start_time = HiddenField('Start Time')
    end_time = HiddenField('End Time')
    equipment_id = HiddenField('Space ID')
    reserve = SubmitField('Reserve')
