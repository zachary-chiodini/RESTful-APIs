import json
from os import path

from flask import Response

from flask_api.config import connexion_app, app, connect_db, db

HOST = '127.0.0.1'
PORT = '5001'
PATH = ''

connexion_app.add_api('swagger.yaml')


@connexion_app.route('/api/connect/', methods=['GET'])
def connect() -> Response:
    try:
        with open(path.join(PATH, 'config.json')) as file:
            login_info = json.load(file)
        connect_db(app, db, login_info)
    except Exception as e:
        response = Response(str(e), status=500)
        return response
    response = Response('Connected to {}'.format(db.engine),
                        status=200)
    return response


@connexion_app.route('/')
def home():
    return ''


if __name__ == '__main__':
    connexion_app.run(host=HOST, port=PORT, debug=True)
