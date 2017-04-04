from flask import abort, flash, redirect, render_template, url_for, request, jsonify
from flask_login import current_user, login_required
from flask_rq import get_queue
from . import reserve
from .. import db
from ..models import *
from .forms import *
import sys

@reserve.route('/space', methods=['GET', 'POST'])
def space():
    form = ReserveSpaceForm()
    if form.validate_on_submit():
        pass
    return render_template('reserve/space.html', form=form)

@reserve.route('/_get_spaces/')
def _get_spaces():
    location = request.args.get('location', '01', type=str)
    print(location, file=sys.stderr)
    spaces = [(row.id, row.name) for row in db.session.query(Space).filter_by(location_id=location)]
    print(spaces, file=sys.stderr)
    return jsonify(spaces)
