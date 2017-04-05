from .. import db
import datetime
import enum
from sqlalchemy import UniqueConstraint

class Campus(db.Model):
    __tablename__ = 'campuses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))

class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    zip_code = db.Column(db.String(30))
    address_line_1 = db.Column(db.String(30))
    address_line_2 = db.Column(db.String(30))
    address_line_3 = db.Column(db.String(30))
    campus_id = db.Column(db.Integer, db.ForeignKey('campuses.id'))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    contact_email = db.Column(db.String(64))
    contact_phone = db.Column(db.String(64))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))

class Equipment_Type(db.Model):
    __tablename__ = 'equipment_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(2044), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))

class Condition(enum.Enum):
    GOOD = "Crunchy apple"
    BAD = "Sweet banana"

class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(2044), unique=True)
    equipment_type_id = db.Column(db.Integer, db.ForeignKey('equipment_types.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    condition = db.Column(db.Enum(Condition))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))

class Equipment_Reservation(db.Model):
    __tablename__ = 'equipment_reservations'
    id = db.Column(db.Integer, primary_key=True)
    reserver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    start_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    end_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))

class Space_Type(db.Model):
    __tablename__ = 'space_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(2044), unique=True)
    description = db.Column(db.String(2044), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))

class Space(db.Model):
    __tablename__ = 'spaces'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(2044))
    capacity = db.Column(db.Integer)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    space_type_id = db.Column(db.Integer, db.ForeignKey('space_types.id'))
    condition = db.Column(db.Enum(Condition))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    UniqueConstraint('name', 'location_id', name='space_for_location')

class Ammenity_Type(db.Model):
    __tablename__ = 'ammenity_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(2044), unique=True)
    description = db.Column(db.String(2044))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))

class Space_Ammenity(db.Model):
    __tablename__ = 'space_ammenities'
    id = db.Column(db.Integer, primary_key=True)
    space_id = db.Column(db.Integer, db.ForeignKey('spaces.id'))
    ammenity_type_id = db.Column(db.Integer, db.ForeignKey('ammenity_types.id'))
    condition = db.Column(db.Enum(Condition))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    UniqueConstraint('space_id', 'ammenity_type_id', name='space_ammenity_index')


class Space_Reservation(db.Model):
    __tablename__ = 'space_reservations'
    id = db.Column(db.Integer, primary_key=True)
    space_id = db.Column(db.Integer, db.ForeignKey('spaces.id'))
    event_name = db.Column(db.String(2044))
    reserver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    end_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
