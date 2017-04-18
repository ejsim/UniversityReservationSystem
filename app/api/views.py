from flask import render_template
from ..models import EditableHTML

from . import api


@api.route('/')
def index():
    return render_template('api/index.html')