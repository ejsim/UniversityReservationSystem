from flask import abort, flash, redirect, render_template, url_for, request, jsonify
from flask_login import current_user, login_required
from flask_rq import get_queue
from sqlalchemy import *
import datetime
from . import reserve
from .. import db
from ..models import *
from .forms import *
import sys
import json

def datetimeconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def make_sql(campus, space_type, start_time, end_time, capacity=None, ammenities=None):
    sql = """SELECT s.*, l.name AS location_name, CONCAT(l.name, ' ', s.name) AS full_name, c.name AS campus_name
    FROM spaces s
    JOIN locations l ON s.location_id = l.id
    JOIN campuses c ON l.campus_id = c.id
    WHERE """
    if capacity!=None:
        sql += "s.capacity > " + str(capacity) + " AND "
    sql += "s.space_type_id = {} AND c.id = {} AND ".format(space_type, campus)
    sql += "(SELECT COUNT(sr.id) FROM space_reservations sr WHERE sr.space_id=s.id AND (sr.start_time <= (TIMESTAMP '{}')) AND (sr.end_time >= (TIMESTAMP '{}')))=0".format(end_time, start_time)
    if ammenities != None and len(ammenities)>0:
        sql += " AND (SELECT COUNT(sa.id)FROM unnest(ARRAY[" + (','.join(list(map((lambda a: str(a.id)), ammenities)))) +"]) am_id "
        sql += "LEFT JOIN space_ammenities sa ON sa.ammenity_type_id=am_id "
        sql += "WHERE sa.space_id = s.id) = " + str(len(ammenities))
    sql += ";"
    print(sql, file=sys.stderr)
    return text(sql)

@reserve.route('/space', methods=['GET', 'POST'])
@login_required
def space():
    search_form = SearchSpaceForm()
    reserve_form = ReserveSpaceForm()
    if reserve_form.validate_on_submit():
        sr = Space_Reservation(event_name=reserve_form.event_name.data, space_id=reserve_form.space_id.data, reserver_id=current_user.id, start_time=datetime.datetime.strptime(reserve_form.start_time.data, "%B %d, %Y %I:%M %p").date(), end_time=datetime.datetime.strptime(reserve_form.end_time.data, "%B %d, %Y %I:%M %p").date(), created_by=current_user.id, last_updated_by=current_user.id)
        db.session.add(sr)
        db.session.commit()
        print("Reservation Added", file=sys.stderr)
        return redirect(url_for('account.manage'))
    if search_form.is_submitted():
        if not search_form.validate():
            return render_template('reserve/space.html', search_form=search_form, reserve_form=reserve_form)
        sql = make_sql(str(search_form.campus.data.id), str(search_form.space_type.data.id), str(search_form.start_time.data), str(search_form.end_time.data), search_form.capacity.data, search_form.ammenities.data)
        print(search_form.ammenities.data, file=sys.stderr)
        response = db.engine.execute(sql)
        print("THIS IS A THING", file=sys.stderr)
        print(response, file=sys.stderr)
        available_spaces = []
        for space in response:
            available_spaces.append(dict(zip(space.keys(), space)))
        print(json.dumps(available_spaces, default = datetimeconverter), file=sys.stderr)
        return render_template('reserve/space.html', search_form=search_form, reserve_form=reserve_form, available_spaces=available_spaces)
    return render_template('reserve/space.html', search_form=search_form, reserve_form=reserve_form)
