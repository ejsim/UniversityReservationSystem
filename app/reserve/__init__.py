from flask import Blueprint

main = Blueprint('reserve', __name__)

from . import views, errors  # noqa
