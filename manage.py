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
    campus = Campus(name='Tufts', city='Medford', state='MA')
    db.session.add(campus)
    db.session.commit()


    space_type = Space_Type(name='classroom', description='A room for students to congregate')
    db.session.add(space_type)
    db.session.commit()


    location1 = Location(name='Halligan Hall', city='Medford', state='MA', zip_code='02144', address_line_1='161 College Ave', campus_id=1)
    location2 = Location(name='Tisch Library', city='Medford', state='MA', zip_code='02144', address_line_1='35 Professors Row', campus_id=1)
    db.session.add(location1)
    db.session.add(location2)
    db.session.commit()


    space1 = Space(name='102', capacity=15, space_type_id=1, location_id=1)
    space2 = Space(name='116', capacity=4, space_type_id=1, location_id=2)
    db.session.add(space1)
    db.session.add(space2)
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
