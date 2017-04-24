#!/usr/bin/env python
import os
import subprocess
from config import Config

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from redis import Redis
from rq import Connection, Queue, Worker
import flask_restless
import flask_sqlalchemy
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

    campus1 = Campus(name='Tufts Medford/Somerville', city='Medford', state='MA')
    campus2 = Campus(name='Tufts Grafton', city='Grafton', state='MA')
    db.session.add_all([campus1, campus2])
    db.session.commit()

    space_types = ['Performance Hall', 'Lecture Hall', 'Dorm Room', 'Dorm Common Room', 'Conference Room', 'Athletic Field', 'Outdoor Area']

    for s in space_types:
        db.session.add(Space_Type(name=s))
    space_type1 = Space_Type(name='Classroom', description='A room where teaching occurs')
    space_type2 = Space_Type(name='Study Room', description='A room where studying occurs')
    db.session.add_all([space_type1, space_type2])
    db.session.commit()

    ammenities = ['Projector', 'Whiteboard', 'Lawn', 'Table', 'Chairs', 'Light', 'Hescott', 'Chow']
    for a in ammenities:
        db.session.add(Ammenity_Type(name=a))
    db.session.commit()

    location1 = Location(name='Halligan Hall', city='Medford', state='MA', zip_code='02144', address_line_1='161 College Ave', campus_id=1)
    location2 = Location(name='Tisch Library', city='Medford', state='MA', zip_code='02144', address_line_1='35 Professors Row', campus_id=1)
    location3 = Location(name='Eaton Hall', city='Medford', state='MA', zip_code='02144', address_line_1='19 Professors Row', campus_id=1)
    location4 = Location(name='Olin Hall', city='Medford', state='MA', zip_code='02144', address_line_1='2 Professors Row', campus_id=1)
    location5 = Location(name="President's Lawn", city='Medford', state='MA', zip_code='02144', address_line_1='4 Professors Row', campus_id=1)
    location6 = Location(name='Tennis Courts', city='Medford', state='MA', zip_code='02144', address_line_1='26 Curtis Ave', campus_id=1)

    db.session.add_all([location1, location2, location3, location4, location5, location6])
    db.session.commit()

    #Space Types
    # 1: Performance Hall
    # 2: Lecture Hall
    # 3: Dorm Room
    # 4: Dorm Common Room
    # 5: Conference Room
    # 6: Athletic fields
    # 7: Outdoor Area
    # 8: Classroom
    # 9: Study Room

    #Halligan id=1
    space1 = Space(name='102', capacity=15, space_type_id=8, location_id=1, min_role=Permission.FACULTY)
    space2 = Space(name='211', capacity=15, space_type_id=8, location_id=1, min_role=Permission.FACULTY)
    space3 = Space(name='Kitchen', capacity=15, space_type_id=5, location_id=1, min_role=Permission.STUDENT)
    db.session.add_all([space1, space2, space3])

    #Tisch id=2
    space1 = Space(name='113a', capacity=15, space_type_id=9, location_id=2, min_role=Permission.PUBLIC)
    space2 = Space(name='Downstairs Computer Lab', capacity=15, space_type_id=8, location_id=2, min_role=Permission.FACULTY)
    space3 = Space(name='112b', capacity=15, space_type_id=9, location_id=2, min_role=Permission.PUBLIC)
    db.session.add_all([space1, space2, space3])

    #Eaton id=3
    space1 = Space(name='Computer Lab', capacity=15, space_type_id=8, location_id=3, min_role=Permission.ORG_LEADER)
    space2 = Space(name='105', capacity=15, space_type_id=8, location_id=3, min_role=Permission.FACULTY)
    space3 = Space(name='210', capacity=15, space_type_id=8, location_id=3, min_role=Permission.FACULTY)
    db.session.add_all([space1, space2, space3])

    #Olin id=4
    space1 = Space(name='102', capacity=15, space_type_id=8, location_id=4, min_role=Permission.FACULTY)
    space2 = Space(name='Downstairs Lobby', capacity=15, space_type_id=5, location_id=4, min_role=Permission.STUDENT)
    space3 = Space(name='212', capacity=15, space_type_id=5, location_id=4, min_role=Permission.ORG_LEADER)
    db.session.add_all([space1, space2, space3])

    #Pres-Lawn id=5
    space1 = Space(name='Outside of President House', capacity=15, space_type_id=7, location_id=5, min_role=Permission.ORGANIZER)
    space2 = Space(name='The Lighting Ceremony Spot', capacity=15, space_type_id=7, location_id=5, min_role=Permission.ORGANIZER)
    space3 = Space(name='Spring Fling Space', capacity=15, space_type_id=7, location_id=5, min_role=Permission.ORGANIZER)
    db.session.add_all([space1, space2, space3])

    #Tennis Courts id=6
    space1 = Space(name='Court 1', space_type_id=6, location_id=6, min_role=Permission.PUBLIC)
    space2 = Space(name='Court 2', space_type_id=6, location_id=6, min_role=Permission.PUBLIC)
    space3 = Space(name='Court 3', space_type_id=6, location_id=6, min_role=Permission.PUBLIC)
    db.session.add_all([space1, space2, space3])

    db.session.commit()

    # WhiteBoards
    space_ammenity1 = Space_Ammenity(space_id = 1, ammenity_type_id=2)
    space_ammenity2 = Space_Ammenity(space_id = 2, ammenity_type_id=2)
    space_ammenity3 = Space_Ammenity(space_id = 7, ammenity_type_id=2)
    space_ammenity4 = Space_Ammenity(space_id = 8, ammenity_type_id=2)
    space_ammenity5 = Space_Ammenity(space_id = 9, ammenity_type_id=2)
    space_ammenity6 = Space_Ammenity(space_id = 10, ammenity_type_id=2)

    space_ammenity7 = Space_Ammenity(space_id = 1, ammenity_type_id=3)
    space_ammenity8 = Space_Ammenity(space_id = 1, ammenity_type_id=4)
    space_ammenity9 = Space_Ammenity(space_id = 1, ammenity_type_id=5)
    space_ammenity10 = Space_Ammenity(space_id = 2, ammenity_type_id=6)
    space_ammenity11 = Space_Ammenity(space_id = 2, ammenity_type_id=7)
    space_ammenity12 = Space_Ammenity(space_id = 3, ammenity_type_id=8)


    db.session.add_all([space_ammenity1, space_ammenity2, space_ammenity3, space_ammenity4, space_ammenity5, space_ammenity6, space_ammenity7, space_ammenity8, space_ammenity9, space_ammenity10, space_ammenity11, space_ammenity12])
    db.session.commit()

    et1 = Equipment_Type(name="iPad")
    et2 = Equipment_Type(name="Macbook")
    et3 = Equipment_Type(name="Baseball Bat")
    et4 = Equipment_Type(name="DSLR")
    et5 = Equipment_Type(name="Van")

    db.session.add_all([et1, et2, et3, et4, et5])
    db.session.commit()

<<<<<<< HEAD
    e1 = Equipment(equipment_type_id=1, name="1", location_id=2, min_role=Permission.STUDENT)
    e2 = Equipment(equipment_type_id=1, name="2", location_id=2, min_role=Permission.STUDENT)
    e3 = Equipment(equipment_type_id=1, name="3", location_id=2, min_role=Permission.STUDENT)
    e4 = Equipment(equipment_type_id=1, name="4", location_id=2, min_role=Permission.STUDENT)
    e5 = Equipment(equipment_type_id=1, name="5", location_id=2, min_role=Permission.STUDENT)
=======
    e1 = Equipment(equipment_type_id=1, name="1", location_id=2)
    e2 = Equipment(equipment_type_id=1, name="2", location_id=2)
    e3 = Equipment(equipment_type_id=1, name="3", location_id=2)
    e4 = Equipment(equipment_type_id=1, name="4", location_id=2)
    e5 = Equipment(equipment_type_id=1, name="5", location_id=2)
>>>>>>> fb1df167e61fd6b47be817b7bc3cb549bf5a1912

    db.session.add_all([e1, e2, e3, e4, e5])
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
    add_fake_data(10)
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
