# ideal-roommate

## Instructions for usage

1. login to mysql server and run the schema.sql
1. run the following `pip install` commands
    * `pip install flask`
    * `pip install mysql.connector`
1. modify sql login credentials in Line 17 of `__init__.py` as needed
1. in root folder, run `export FLASK_APP=.` for mac and `set FLASK_APP=.` for windows
1. to start, execute `flask run` and go to http://127.0.0.1:5000

## Overview of files

1. `__init__.py` contains initialising configurations for the app, mostly will not need to touch
1. `auth.py` contains routings and logic for the authentication-related portions of the app
1. `main.py` contains routings and logic for the rest of the app
1. `animal.py` holds the class for the Animal, which is the main entity, equivalent of User, as well as the currAnimal variable, which holds currently logged-in user.
1. everything inside `static/` is the images saved when uploaded using the app
1. everything inside `templates/` are the html files, where you can see places with python code contained in `{{` and `}}`
