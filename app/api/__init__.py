from flask import Blueprint

import flask_restless
from flask_sqlalchemy import SQLAlchemy

api = Blueprint('api', __name__)

from . import views, errors  # noqa



print("Creating API")