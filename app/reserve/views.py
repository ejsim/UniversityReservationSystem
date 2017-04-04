from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from flask_rq import get_queue
from . import reserve
from .. import db
from ..models import *
from .forms import *

@reserve.route('/space', methods=['GET', 'POST'])
def space():
    form = ReserveSpaceForm()
    if form.validate_on_submit():

        reservation = Space_Reservation(
            space_id=1,
            event_name=form.event_name.data,
            reserver_id=current_user.id)
        db.session.add(reservation)
        db.session.commit()
        flash('Your Space Has Been Reserved!',
              'warning')
    return render_template('reserve/space.html', form=form)
