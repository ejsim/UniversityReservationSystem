from flask import flash, redirect, render_template, request, url_for
from flask_login import (current_user, login_required, login_user,
                         logout_user)
from flask_rq import get_queue
from sqlalchemy import *
from . import main
from .. import db
from ..email import send_email
from ..models import *
from .forms import (CancelReservationForm)
import sys


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Display a user's account information."""

    if not current_user.is_authenticated:
        return redirect(url_for("account.login"))

    cancel_reservation_form = CancelReservationForm()

    if cancel_reservation_form.validate_on_submit():
        cancel_id = int(cancel_reservation_form.id.data)
        if cancel_reservation_form.type.data == "space":
            print("SR ID: " + str(cancel_id), file=sys.stderr)
            sr = Space_Reservation.query.filter_by(id=cancel_id).first()
            db.session.delete(sr)
            db.session.commit()
            flash('Your Space Reservation has been cancelled')
        elif cancel_reservation_form.type.data == "equipment":
            print("ER ID: " + str(cancel_id), file=sys.stderr)
            er = Equipment_Reservation.query.filter_by(id=cancel_id).first()
            db.session.delete(er)
            db.session.commit()
            flash('Your Equipment Reservation has been cancelled')

    space_sql = '''SELECT sr.*, s.name AS space_name, l.name AS location_name, c.name AS campus_name
    FROM space_reservations sr
    JOIN spaces s ON s.id=sr.space_id
    JOIN locations l ON s.location_id = l.id
    JOIN campuses c ON l.campus_id = c.id
    WHERE sr.reserver_id=''' + str(current_user.id) + ";"

    sr_response = db.engine.execute(text(space_sql))
    space_reservations = []
    for sr in sr_response:
        space_reservations.append(dict(zip(sr.keys(), sr)))

    equipment_sql = '''SELECT er.*, e.name AS equipment_name, et.name AS equipment_type_name, l.name AS location_name, c.name AS campus_name
    FROM equipment_reservations er
    JOIN equipment e ON e.id=er.equipment_id
    JOIN equipment_types et ON e.equipment_type_id = et.id
    JOIN locations l ON e.location_id = l.id
    JOIN campuses c ON l.campus_id = c.id
    WHERE er.reserver_id=''' + str(current_user.id) + ";"

    er_response = db.engine.execute(text(equipment_sql))
    equipment_reservations = []
    for er in er_response:
        equipment_reservations.append(dict(zip(er.keys(), er)))

    return render_template('main/index.html', user=current_user, space_reservations=space_reservations, equipment_reservations=equipment_reservations, cancel_reservation_form=cancel_reservation_form)
