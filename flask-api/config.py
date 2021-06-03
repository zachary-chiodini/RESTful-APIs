# import connexion
from os import urandom
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# from flask_login import LoginManager
from sshtunnel import SSHTunnelForwarder
from typing import Dict


def url_encoded(s: str) -> str:
    url_encoding = {
        '!': '%21', '#': '%23', '$': '%24', '&': '%26', "'": '%27',
        '(': '%28', ')': '%29', '*': '%2A', '+': '%2B', ',': '%2C',
        '/': '%2F', ':': '%3A', ';': '%3B', '=': '%3D', '?': '%3F',
        '@': '%40', '[': '%5B', ']': '%5D'
        }
    # This applies the percent-encoding.
    s = s.replace('%', '%25')
    # This applies the remaining character encodings.
    for special_char, encoding in url_encoding.items():
        s = s.replace(special_char, encoding)
    return s


def connect_db(application: Flask,
               database: SQLAlchemy, login_info: Dict) -> None:
    ssh_tunnel = SSHTunnelForwarder(
        ssh_address_or_host=login_info['ssh host address'],
        ssh_username=login_info['ssh username'],
        ssh_password=login_info['ssh password'],
        remote_bind_address=(login_info['remote bind address'], 3306)
        )
    ssh_tunnel.start()
    application.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql://{sql_usr}:{sql_pswd}@127.0.0.1:{port}/{database}'\
        .format(
            sql_usr=login_info['sql username'],
            sql_pswd=url_encoded(login_info['sql password']),
            port=ssh_tunnel.local_bind_port,
            database=login_info['database']
            )
    # This tests the database connection.
    connection = database.engine.connect()
    connection.close()
    return None


# This creates the connexion application instance.
app = Flask(__name__)
# This gets the underlying flask app instance.

app.secret_key = urandom(16)
app.config['USERNAME'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
# lm = LoginManager(app)
