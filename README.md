# University Reservation System 

An application that allows the creation of room reservations based on desired attributes.

## Setting up

##### Clone the repo

```
$ git clone git@github.com:tuftsdev/comp120-s2017-team7.git
```

##### Initialize a virtualenv

Note: if you don't have python3 installed, install it via 

```
$ brew install python3
```

Run the following commands to initialize your virtualenv;

```
$ python3 -m venv ./venv
$ source ./venv/bin/activate
```

##### Add Environment Variables 

Not sure yet if this section is true or not...Ask Max

Create a file called `config.env` that contains environment variables in the following syntax: `ENVIRONMENT_VARIABLE=value`. For example,
the mailing environment variables can be set as the following. We recommend using Sendgrid for a mailing SMTP server. But anything else will work as well.

```
MAIL_USERNAME=SendgridUsername
MAIL_PASSWORD=SendgridPassword
SECRET_KEY=SuperRandomStringToBeUsedForEncryption
```

Other Key value pairs:

* `ADMIN_EMAIL`: set to the default email for your first admin account (default is `flask-base-admin@example.com`)
* `ADMIN_PASSWORD`: set to the default password for your first admin account (default is `password`)
* `DATABASE_URL`: set to a postgresql database url (default is `data-dev.sqlite`)
* `REDISTOGO_URL`: set to Redis To Go URL or any redis server url (default is `http://localhost:6379`)
* `RAYGUN_APIKEY`: api key for raygun (default is `None`)
* `FLASK_CONFIG`: can be `development`, `production`, `default`, `heroku`, `unix`, or `testing`. Most of the time you will use `development` or `production`. 


**Note: do not include the `config.env` file in any commits. This should remain private.**

##### Install the dependencies

```
$ pip install -r requirements.txt
```

##### Other dependencies for running locally

You need to [Redis](http://redis.io/), and [Sass](http://sass-lang.com/). Chances are, these commands will work:


**Sass:**

```
$ gem install sass
```

Note: If you don't have write permissions, try this;

```
$ sudo gem install sass
```

**Redis:**

_Mac (using [homebrew](http://brew.sh/)):_

```
$ brew install redis
```

_Linux:_

```
$ sudo apt-get install redis-server
```

You will also need to install **PostgresQL**

_Mac (using homebrew):_

```
$ brew install postgresql
```

_Linux (based on this [issue](https://github.com/hack4impact/flask-base/issues/96)):_

```
$ sudo apt-get install libpq-dev
```


##### Create the database

Start your Postgres database and create the database

```
$ pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
$ psql
$ create database urs_flask;
```

Run a migration to initialize the tables in the database urs_flask

```
$ python manage.py recreate_db
```

##### Other setup (e.g. creating roles in database)

```
$ python manage.py setup_dev
```

Note that this will create an admin user with email and password specified by the `ADMIN_EMAIL` and `ADMIN_PASSWORD` config variables. If not specified, they are both `flask-base-admin@example.com` and `password` respectively.

##### [Optional] Add fake data to the database

```
$ python manage.py add_test_data
```

## Running the app

```
$ source env/bin/activate
$ honcho start -f Local
```

For Windows users having issues with binding to a redis port locally, refer to [this issue](https://github.com/hack4impact/flask-base/issues/132).

The default port of this application is http://127.0.0.1:5000/

