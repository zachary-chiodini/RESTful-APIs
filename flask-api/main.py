import json
from os import path

from flask import Response

from config import connexion_app, app, connect_db, db

HOST = '0.0.0.0'
PORT = 5000
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
    # automatically connecting until an
    # account login system is developed
    connect()
    connexion_app.run(host=HOST, port=PORT, debug=True)
