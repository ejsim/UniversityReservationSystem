import flask_restless
import sys
from .. import app, db
from .. models import *

print("Init api", file=sys.stderr)


manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Location, methods=['GET', 'POST', 'DELETE'])
