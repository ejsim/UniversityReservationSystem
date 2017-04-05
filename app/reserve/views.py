from flask import abort, flash, redirect, render_template, url_for, request, jsonify
from flask_login import current_user, login_required
from flask_rq import get_queue
from sqlalchemy import text
from . import reserve
from .. import db
from ..models import *
from .forms import *
import sys

@reserve.route('/space', methods=['GET', 'POST'])
@login_required
def space():
    form = ReserveSpaceForm()
    if form.validate_on_submit():
        find_spaces_placeholder = """SELECT s.*, l.name, c.name
        FROM spaces s
        JOIN locations l ON s.location_id = l.id
        JOIN campuses c ON l.campus_id = c.id
        WHERE s.capacity > 5 AND s.space_type_id = {} AND c.id = {}
        AND (SELECT COUNT(sr.id) FROM space_reservations sr WHERE sr.space_id=s.id AND (sr.start_time <= (TIMESTAMP '{}')) AND (sr.end_time >= (TIMESTAMP '{}')))=0
        AND (SELECT COUNT(sa.id)
        FROM unnest(ARRAY[{}]) am_id
        LEFT JOIN space_ammenities sa ON sa.ammenity_type_id=am_id
        WHERE sa.space_id = s.id) = {};"""

        find_spaces = text(find_spaces_placeholder.format(str(form.space_type.data.id), str(form.campus.data.id), str(form.end_time.data), str(form.start_time.data), ','.join(list(map((lambda a: str(a.id)), form.ammenities.data))),  str(len(form.ammenities.data))))
        available_spaces = db.engine.execute(find_spaces)
        for row in available_spaces:
            print(row['id'], file=sys.stderr)
    return render_template('reserve/space.html', form=form)

@reserve.route('/_get_spaces/')
def _get_spaces():
    location = request.args.get('location', '01', type=str)
    print(location, file=sys.stderr)
    spaces = [(row.id, row.name) for row in db.session.query(Space).filter_by(location_id=location)]
    print(spaces, file=sys.stderr)
    return jsonify(spaces)
