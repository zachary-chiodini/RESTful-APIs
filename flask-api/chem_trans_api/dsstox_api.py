from os import path
from requests import Response, Session

HOST = ''
PORT = ''

DSSTOX_API_URL = 'http://{host}:{port}/api/'\
    .format(host=HOST, port=PORT)


class DSSToxAPI:
    def __init__(self) -> None:
        self.session = Session()

    def connect(self) -> Response:
        response = self.session.get(path.join(DSSTOX_API_URL, 'connect'))
        return response

    def get_substance_relationship_record(
            self, predecessor_generic_substance_id: int,
            successor_generic_substance_id: int
            ) -> Response:
        pass
