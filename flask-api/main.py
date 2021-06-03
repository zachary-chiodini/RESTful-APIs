import model
from flask import Response
from config import app, connect_db, db
from utils import entity_get_or_post_response, record_id_response

HOST = '127.0.0.1'
PORT = '5000'


@app.kinetics('/kinetics/')
def kinetics() -> Response:
    return entity_get_or_post_response(
        model.Kinetics, model.KineticsSchema,
        fk_substance_relationships_id=model.Kinetics.fk_substance_relationships_id,
        pH=model.Kinetics.pH,
        pH_min=model.Kinetics.pH_min,
        pH_max=model.Kinetics.pH_max,
        half_life=model.Kinetics.half_life,
        half_life_min=model.Kinetics.half_life_min,
        half_life_max=model.Kinetics.half_life_max,
        half_life_units=model.Kinetics.half_life_units,
        rate=model.Kinetics.rate,
        rate_min=model.Kinetics.rate_min,
        rate_max=model.Kinetics.rate_max,
        rate_units=model.Kinetics.rate_units,
        reaction=model.Kinetics.reaction,
        temp_C=model.Kinetics.temp_C,
        activation_kcal_per_mol=model.Kinetics.activation_kcal_per_mol,
        comments=model.Kinetics.comments
        )


@app.route('/kinetics_record/<kinetics_id>/')
def kinetics_record(kinetics_id) -> Response:
    return record_id_response(
        model.Kinetics, model.KineticsSchema,
        fk_substance_relationships_id=model.Kinetics.fk_substance_relationships_id,
        pH=model.Kinetics.pH,
        pH_min=model.Kinetics.pH_min,
        pH_max=model.Kinetics.pH_max,
        half_life=model.Kinetics.half_life,
        half_life_min=model.Kinetics.half_life_min,
        half_life_max=model.Kinetics.half_life_max,
        half_life_units=model.Kinetics.half_life_units,
        rate=model.Kinetics.rate,
        rate_min=model.Kinetics.rate_min,
        rate_max=model.Kinetics.rate_max,
        rate_units=model.Kinetics.rate_units,
        reaction=model.Kinetics.reaction,
        temp_C=model.Kinetics.temp_C,
        activation_kcal_per_mol=model.Kinetics.activation_kcal_per_mol,
        comments=model.Kinetics.comments
        )

@app.route('/substance_relationships/')
def substance_relationships() -> Response:
    return entity_get_or_post_response(
        model.SubstanceRelationships, model.SubstanceRelationships,
        fk_generic_substance_id_predecessor=model.SubstanceRelationships
            .fk_generic_substance_id_predecessor,
        fk_generic_substance_id_successor=model.SubstanceRelationships
            .fk_generic_substance_id_successor,
        relationship=model.SubstanceRelationships.relationship,
        fk_substance_relationship_type_id=model.SubstanceRelationships
            .fk_substance_relationship_type_id,
        source=model.SubstanceRelationships.source,
        qc_notes=model.SubstanceRelationships.qc_notes,
        mixture_percentage=model.SubstanceRelationships.mixture_percentage,
        percentage_type=model.SubstanceRelationships.percentage_type,
        is_nearest_structure=model.SubstanceRelationships.is_nearest_structure,

        )


@app.route('/author/')
def author() -> Response:
    return entity_get_or_post_response(
        model.Author, model.AuthorSchema,
        first_name=model.Author.first_name,
        middle_name=model.Author.middle_name,
        last_name=model.Author.last_name
        )


@app.route('/author_record/<author_id>/')
def author_record(author_id) -> Response:
    return record_id_response(
        model.Author, model.AuthorSchema,
        first_name=model.Author.first_name,
        middle_name=model.Author.middle_name,
        last_name=model.Author.last_name
        )


@app.route('/connect/', methods=['GET'])
def connect() -> Response:
    try:
        with open('flask-api//config.json') as file:
            login_info = json.load(file)
        connect_db(app, db, login_info)
    except Exception as e:
        response = Response(str(e), status=404)
        return response
    response = Response('Connected to {}'.format(db.engine),
                        status=200)
    return response


@app.route('/')
def home():
    return ''


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
