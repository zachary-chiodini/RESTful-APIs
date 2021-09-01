from requests import Response, Session

HOST = '127.0.0.1'
PORT = '5001'

DSSTOX_API_URL = 'http://{host}:{port}/api'\
    .format(host=HOST, port=PORT)


class DSSToxAPI:
    def __init__(self) -> None:
        self.session = Session()

    def connect(self) -> Response:
        response = self.session.get(
            '{url}/{path}'.format(url=DSSTOX_API_URL, path='connect')
        )
        return response

    def get_join(
            self, predecessor_generic_substance_id: int,
            successor_generic_substance_id: int
            ) -> Response:
        pass
