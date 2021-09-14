from os import path, urandom
from typing import Dict

import connexion
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


HOST = 'v2626umcth819.rtord.epa.gov'
PORT = '5000'
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
    application.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql://{sql_usr}:{sql_pswd}@{host}:{port}/{database}'\
        .format(
            sql_usr=login_info['sql username'],
            sql_pswd=url_encoded(login_info['sql password']),
            host=HOST,
            port=PORT,
            database=login_info['database']
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
CORS(app)  # add CORS support
app.secret_key = urandom(16)
app.config['USERNAME'] = ''
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
