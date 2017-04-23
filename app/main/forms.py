from flask_wtf import Form
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import PasswordField, StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from .. import db
from ..models import Role, User

class CancelReservationForm(Form):
    id = StringField('Space ID')
    type = StringField('Reservation Type')
    cancel = SubmitField('Cancel')
