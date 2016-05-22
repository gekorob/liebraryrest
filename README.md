# LiebraryREST

Liebrary rest is a demo project made only for educational purposes. The Flask and Flask-SQLAlchemy aims to provide several (but not all) REST services to manage a fake library with books, authors and users.
The application doesn't provide creational services (like inserting new books, authors or even users) a part from the booking service.

### What is not
It's not a real project with all services needed and it's not, obviously, a production ready project.

### Requirements
This project uses python3 and is not *retro-compatible* with python 2.7.
All requirements are specified in the requirements folder, divided by the environment in which you want to work in.
The *requirements.txt* in the project root folder requires the *prod.txt* with all you need for production mode use.

If you want to test and develop I suggest you to do

```
pip install -r requirements/dev.txt
```

as if you want only to test you need

```
pip install -r requirements/test.txt
```

### Quick start
To start working quickly in this project you need to clone it

```
git clone https://github.com/gekorob/liebraryrest.git
```

and to install *dev* requirements into your *venv*:

```
pip install -r requirements/dev.txt
```
This project is using sqlite3 with migrations committed and ready for you.
In particular the second revision in the migrations folder is used to seed your db.
So if you want to use this migrations you can just do as follow:

```
python manage.py db upgrade
```

This will create a *dev.db* in the root of your project with some data.
At this point you can start the web server, on your *localhost* at the port *5000*, using

```
python manage.py server
```

If you want to alter the host address or the port (e.g.: to serve from your virtual machine using the ip provided and a particular port) you can use options

```
python manage.py server -h 0.0.0.0 -p 8080
```

The *manage.py* utility allows you also to view the allowed *urls*

```
python manage.py urls
```

### Environments
To change the environment in which your application has to run on, you can use the *LIEBRARYREST_ENV* environment variable that allows you to switch in the *prod* or *dev*.

```
LIEBRARYREST_ENV=prod python manage.py db upgrade
LIEBRARYREST_ENV=prod python manage.py server
```
These two lines above set up the *prod.db* and start the webserver in production environment.

### Other DBMS
You can use other DBMS modifying the *liebraryrest/settings.py* db urls configuration and setting up your own migrations:

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
