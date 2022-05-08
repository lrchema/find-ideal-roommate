from flask import Flask
import mysql.connector

def create_app():
    app = Flask(__name__)

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    app.config['curruser_info'] = None
    return app

def dbconn():
    hostname = 'us-cdbr-east-05.cleardb.net'
    username = 'be1667b5870ad1'
    password = '7d6f2294'
    database = 'heroku_a03101e85242a98'
    return mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
    