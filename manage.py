#!/usr/bin/env python
import os
import subprocess
from config import Config

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from redis import Redis
from rq import Connection, Queue, Worker
import flask_restless
from app import create_app, db
from app.models import *


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def add_test_data():
    db.drop_all()
    db.create_all()
    setup_general()
    campus = Campus(name='Tufts Medford/Somerville', city='Medford', state='MA')
    db.session.add(campus)
    db.session.commit()


    space_type1 = Space_Type(name='Classroom', description='A room where teaching occurs')
    space_type2 = Space_Type(name='Study Room', description='A room where studying occurs')
    db.session.add(space_type1)
    db.session.add(space_type2)
    db.session.commit()

    ammenity1 = Ammenity_Type(name='Projector')
    ammenity2 = Ammenity_Type(name='Whiteboard')
    ammenity3 = Ammenity_Type(name='Lawn')
    db.session.add_all([ammenity1, ammenity2, ammenity3])

    location1 = Location(name='Halligan Hall', city='Medford', state='MA', zip_code='02144', address_line_1='161 College Ave', campus_id=1)
    location2 = Location(name='Tisch Library', city='Medford', state='MA', zip_code='02144', address_line_1='35 Professors Row', campus_id=1)
    db.session.add_all([location1, location2])
    db.session.commit()


    space1 = Space(name='102', capacity=15, space_type_id=1, location_id=1)
    space2 = Space(name='116', capacity=4, space_type_id=1, location_id=2)
    space3 = Space(name='Kitchen', capacity=15, space_type_id=1, location_id=1)
    db.session.add_all([space1, space2, space3])
    db.session.commit()

    space_ammenity1 = Space_Ammenity(space_id = db.session.query(Space).order_by('name')[0].id, ammenity_type_id=db.session.query(Ammenity_Type).order_by('name')[0].id)
    space_ammenity2 = Space_Ammenity(space_id = db.session.query(Space).order_by('name')[1].id, ammenity_type_id=db.session.query(Ammenity_Type).order_by('name')[1].id)
    space_ammenity3 = Space_Ammenity(space_id = db.session.query(Space).order_by('name')[2].id, ammenity_type_id=db.session.query(Ammenity_Type).order_by('name')[2].id)
    db.session.add_all([space_ammenity1, space_ammenity2, space_ammenity3])
    db.session.commit()




@manager.option(
    '-n',
    '--number-users',
    default=10,
    type=int,
    help='Number of each model type to create',
    dest='number_users')
def add_fake_data(number_users):
    """
    Adds fake data to the database.
    """
    User.generate_fake(count=number_users)


@manager.command
def setup_dev():
    """Runs the set-up needed for local development."""
    setup_general()


@manager.command
def setup_prod():
    """Runs the set-up needed for production."""
    setup_general()


def setup_general():
    """Runs the set-up needed for both local development and production.
       Also sets up first admin user."""
    Role.insert_roles()
    admin_query = Role.query.filter_by(name='Administrator')
    if admin_query.first() is not None:
        if User.query.filter_by(email=Config.ADMIN_EMAIL).first() is None:
            user = User(
                first_name='Admin',
                last_name='Account',
                password=Config.ADMIN_PASSWORD,
                confirmed=True,
                email=Config.ADMIN_EMAIL)
            db.session.add(user)
            db.session.commit()
            print('Added administrator {}'.format(user.full_name()))


@manager.command
def run_worker():
    """Initializes a slim rq task queue."""
    listen = ['default']
    conn = Redis(
        host=app.config['RQ_DEFAULT_HOST'],
        port=app.config['RQ_DEFAULT_PORT'],
        db=0,
        password=app.config['RQ_DEFAULT_PASSWORD'])

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()


@manager.command
def format():
    """Runs the yapf and isort formatters over the project."""
    isort = 'isort -rc *.py app/'
    yapf = 'yapf -r -i *.py app/'

    print('Running {}'.format(isort))
    subprocess.call(isort, shell=True)

    print('Running {}'.format(yapf))
    subprocess.call(yapf, shell=True)


if __name__ == '__main__':
    manager.run()
