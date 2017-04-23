#!/bin/bash

python manage.py recreate_db
python manage.py setup_dev
python manage.py add_test_data
honcho start -f Local
