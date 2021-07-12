import connexion
from os import path, urandom
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sshtunnel import SSHTunnelForwarder
from typing import Dict

PATH = ''


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
            database='ro_prod_dsstox'
            )
    # This tests the database connection.
    connection = database.engine.connect()
    connection.close()
    return None


# This creates the connexion application instance.
connexion_app = connexion.App(
    __name__, specification_dir=path.join(PATH, 'openapi'))
# This gets the underlying flask app instance.
app = connexion_app.app
app.secret_key = urandom(16)
app.config['USERNAME'] = ''
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
