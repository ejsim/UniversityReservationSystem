from flask import abort, flash, redirect, render_template, url_for, request, jsonify
from flask_login import current_user, login_required
from flask_rq import get_queue
from sqlalchemy import *
from . import reserve
from .. import db
from ..models import *
from .forms import *
import sys

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
    form = ReserveSpaceForm()

    if form.is_submitted():
        if not form.validate():
            return render_template('reserve/space.html', form=form)
        sql = make_sql(str(form.campus.data.id), str(form.space_type.data.id), str(form.start_time.data), str(form.end_time.data), form.capacity.data, form.ammenities.data)
        print(form.ammenities.data, file=sys.stderr)
        response = db.engine.execute(sql)
        available_spaces = []
        for space in response:
            available_spaces.append(dict(zip(space.keys(), space)))
        #print(available_spaces, file=sys.stderr)
        return render_template('reserve/space.html', form=form, available_spaces=available_spaces)
    return render_template('reserve/space.html', form=form)
