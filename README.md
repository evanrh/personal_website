# Evan's Personal Website Template
_Large portions of this website's code are derived from the [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) by Miguel Grinberg_

## Dependencies
All dependencies can be resolved by running

```
pip3 install -r requirements.txt
```

* [flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* [flask-migrate](https://flask-migrate.readthedocs.io/en/latest/)
* [flask-login](https://flask-login.readthedocs.io/en/latest/)

## Setup
### Layout of .env
**Required Variables**

* DB_URI: URI to a SQL database 
    * Ex: `DB_URI="sqlite:///example.db"`
* SECRET_KEY: a string to cryptographically sign objects
    * Ex: `SECRET_KEY="p4ssw0rd"`
* FLASK_APP: leave this set to resume.py

### Database Configuration
Prior to running the site, you will need to have a functioning database, preferably with a user to login with. Below, are instructions for getting a SQLite database set up for use with this project

You will also need to create a migration repository from the flask shell using the command below:
```
flask db init
```

### Initial Startup
In order to be able to log in, you will need to have a registered user created to login with. As this is meant to be a personal website blog, there are no visible links to a signup page or a login page. You will have to create a user using the method shown below.

```
$ flask shell
>>> u = User(username='example')
>>> u.set_password('SooperS3cr3t')
>>> db.session.add(u)
>>> db.session.commit()
```
After running this block with your info, you should be able to login at `/login`