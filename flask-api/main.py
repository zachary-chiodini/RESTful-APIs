import json
import model
from flask import Response
from config import app, connect_db, db
from utils import entity_get_or_post_response, record_id_response

HOST = '127.0.0.1'
PORT = '5000'


@app.route('/kinetics/', methods=['GET', 'POST'])
def kinetics() -> Response:
    return entity_get_or_post_response(
        model.Kinetics, model.KineticsSchema)


@app.route('/kinetics_record/<kinetics_id>/',
           methods=['GET', 'PUT', 'DELETE'])
def kinetics_record(kinetics_id) -> Response:
    return record_id_response(
        kinetics_id, model.Kinetics, model.KineticsSchema)


@app.route('/substance_relationships/', methods=['GET', 'POST'])
def substance_relationships() -> Response:
    return entity_get_or_post_response(
        model.SubstanceRelationships, model.SubstanceRelationships)


@app.route('/substance_relationships_record/<relationships_id>/',
           methods=['GET', 'PUT', 'DELETE'])
def substance_relationships_record(relationships_id) -> Response:
    return record_id_response(
        relationships_id, model.Kinetics, model.KineticsSchema)


@app.route('/generic_substances/', methods=['GET', 'POST'])
def generic_substances() -> Response:
    return entity_get_or_post_response(
        model.GenericSubstances, model.GenericSubstancesSchema)


@app.route('/generic_substances_record/<substances_id>',
           methods=['GET', 'PUT', 'DELETE'])
def generic_substances_record(substances_id) -> Response:
    return record_id_response(
        substances_id, model.GenericSubstances,
        model.GenericSubstancesSchema)


@app.route('/author/', methods=['GET', 'POST'])
def author() -> Response:
    return entity_get_or_post_response(
        model.Author, model.AuthorSchema)


@app.route('/author_record/<author_id>/',
           methods=['GET', 'PUT', 'DELETE'])
def author_record(author_id) -> Response:
    return record_id_response(
        author_id, model.Author, model.AuthorSchema)


@app.route('/citation/', methods=['GET', 'POST'])
def citation() -> Response:
    return entity_get_or_post_response(
        model.Citation, model.CitationSchema)


@app.route('/citation_record/<citation_id>',
           methods=['GET', 'PUT', 'DELETE'])
def citation_record(citation_id) -> Response:
    return record_id_response(
        citation_id, model.Citation, model.CitationSchema)


@app.route('/connect/', methods=['GET'])
def connect() -> Response:
    try:
        with open('flask-api//config.json') as file:
            login_info = json.load(file)
        connect_db(app, db, login_info)
    except Exception as e:
        response = Response(str(e), status=500)
        return response
    response = Response('Connected to {}'.format(db.engine),
                        status=200)
    return response


@app.route('/')
def home():
    return ''


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
