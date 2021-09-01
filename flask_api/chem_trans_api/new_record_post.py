import json
from typing import Dict, Union

from flask import Response, request
from indigo import Indigo
from indigo.inchi import IndigoInchi

from flask_api import model
from flask_api.config import db
from flask_api.responses import get_features_except_id, query_payload

indigo = Indigo()
indigo_inchi = IndigoInchi(indigo)


def get_substance_relationship_record(
        predecessor_generic_substance_id: int,
        successor_generic_substance_id: int
        ) -> Union[db.Model, None]:
    substance_relationship_record = \
        model.SubstanceRelationships.query\
            .join(model.SubstanceRelationshipTypes)\
            .filter(
                model.SubstanceRelationshipTypes.id
                == model.SubstanceRelationships
                    .fk_substance_relationship_type_id,
                model.SubstanceRelationships
                    .fk_generic_substance_id_predecessor
                == predecessor_generic_substance_id,
                model.SubstanceRelationships
                    .fk_generic_substance_id_successor
                == successor_generic_substance_id,
                model.SubstanceRelationshipTypes.name
                == 'transformation_product'
            )\
            .one_or_none()
    return substance_relationship_record


def create_and_post_new_substance_relationship(
        predecessor_generic_substance_id: int,
        successor_generic_substance_id: int
        ) -> Union[db.Model, None]:
    new_substance_relationship = {
        'fk_generic_substance_id_predecessor':
            predecessor_generic_substance_id,
        'fk_generic_substance_id_successor':
            successor_generic_substance_id,
        'relationship': 'Transformation Product',
        'fk_substance_relationship_type_id': 1,
        'source': 'Caroline Stevens',
        'qc_notes': None,
        'mixture_percentage': None,
        'percentage_type': None,
        'is_nearest_structure': 0,
        'is_nearest_casrn': 0,
        'created_by': 'zchiodini',
        'updated_by': 'zchiodini'
        }
    schema = model.SubstanceRelationshipsSchema()
    substance_relationship_record = schema.load(
        new_substance_relationship, session=db.session)
    db.session.add(substance_relationship_record)
    db.session.commit()
    return substance_relationship_record


def create_and_post_new_kinetics_record(
        substance_relationship_id: int,
        payload: Dict
        ) -> Union[db.Model, None]:
    new_kinetics_data = {}
    for column in get_features_except_id(
            model.Kinetics, skip=['fk_substance_relationship_id']
            ).keys():
        value = payload.get(column)
        new_kinetics_data[column] = value
    new_kinetics_data['fk_substance_relationship_id'] = \
        substance_relationship_id
    schema = model.KineticsSchema()
    kinetics_record = schema.load(
        new_kinetics_data, session=db.session)
    db.session.add(kinetics_record)
    db.session.commit()
    return kinetics_record


def get_kinetics_record(substance_relationship_id: int,
                        payload: Dict) -> Union[db.Model, None]:
    kinetics_data = {}
    for column in get_features_except_id(
            model.Kinetics, skip=['fk_substance_relationship_id']
            ).keys():
        value = payload.get(column)
        kinetics_data[column] = value
    kinetics_data['fk_substance_relationship_id'] = \
        substance_relationship_id
    kinetics_record = query_payload(model.Kinetics, kinetics_data)
    return kinetics_record


def get_citation_record(payload: Dict) -> Union[db.Model, None]:
    new_citation_data = {}
    for label in get_features_except_id(model.Citation).keys():
        value = payload.get(label)
        new_citation_data.update(label=value)
    citation_record = query_payload(
        model.Citation, new_citation_data)
    return citation_record


def create_and_post_new_citation_record(
        payload: Dict) -> Union[db.Model, None]:
    new_citation_data = {}
    for column in get_features_except_id(model.Citation).keys():
        value = payload.get(column)
        new_citation_data[column] = value
    schema = model.CitationSchema()
    citation_record = schema.load(
        new_citation_data, session=db.session)
    db.session.add(citation_record)
    db.session.commit()
    return citation_record


def get_transformation_citation_mapping(
        relationship_record_id: int,
        kinetics_record_id: int,
        citation_record_id: int
        ) -> Union[db.Model, None]:
    transformation_citation_mapping = db.session.query(model.transformation_cited)\
        .filter(
        model.transformation_cited.c
        .fk_substance_relationship_id == relationship_record_id,
        model.transformation_cited.c.fk_kinetics_id == kinetics_record_id,
        model.transformation_cited.c.fk_citation_id == citation_record_id
            )\
        .one_or_none()
    return transformation_citation_mapping


def get_generic_substance_record_by_substance_id(
        generic_substance_id: str
        ) -> Union[db.Model, None]:
    generic_substance_record = model.GenericSubstances.query\
        .filter(model.GenericSubstances.id == generic_substance_id)\
        .one_or_none()
    return generic_substance_record


def get_generic_substance_record_by_dsstox_id(
        dsstox_id: str
        ) -> Union[db.Model, None]:
    generic_substance_record = model.GenericSubstances.query\
        .filter(model.GenericSubstances.dsstox_substance_id == dsstox_id)\
        .one_or_none()
    return generic_substance_record


def create_and_post_new_transformation_citation_mapping(
        relationship_record_id: int,
        kinetics_record_id: int,
        citation_record_id: int
        ) -> Union[db.Model, None]:
    new_mapping_record = model.transformation_cited.insert().values(
        fk_substance_relationship_id=relationship_record_id,
        fk_kinetics_id=kinetics_record_id,
        fk_citation_id=citation_record_id
        )
    db.engine.execute(new_mapping_record)
    db.session.commit()
    return new_mapping_record


def post_and_map_authors(citation_id, payload: Dict) -> None:
    for author in payload.get('authors').split(','):
        author = author.strip()
        if not author:
            first_name, middle_name, last_name = None, None, None
        elif author.count(' ') == 1:
            middle_name = None
            first_name, last_name = author.split()
        elif author.count(' ') == 2:
            first_name, middle_name, last_name = author.split()
        else:
            first_name, middle_name = None, None
            last_name = author
        author_data = {'first_name': first_name,
                       'middle_name': middle_name,
                       'last_name': last_name}
        author_record = query_payload(model.Author, author_data)
        if author_record:
            author_citation_mapping = db.session.query(model.author_cited)\
                .filter(
                model.author_cited.c.fk_author_id == author_record.id,
                model.author_cited.c.fk_citation_id == citation_id
                    )
            if author_citation_mapping:
                # record already exists
                continue
        else:
            # insert new author
            schema = model.AuthorSchema()
            author_record = schema.load(
                author_data, session=db.session)
            db.session.add(author_record)
            db.session.commit()
        # insert new author-citation mapping
        new_mapping_record = model.author_cited.insert().values(
            fk_citation_id=citation_id, fk_author_id=author_record.id
            )
        db.engine.execute(new_mapping_record)
        db.session.commit()
    return None


def get_generic_substance_id(identifier: str) -> Union[str, None]:
    substance_id = model.SynonymMv.query\
        .filter(model.SynonymMv.identifier == identifier)\
        .order_by(model.SynonymMv.rank)\
        .first()
    return substance_id.fk_generic_substance_id


def post_new_transformation_record() -> Response:
    payload = json.loads(request.get_json())
    predecessor_dsstox_id = payload.get('predecessor_dsstox_id')
    record_already_exists = True
    if predecessor_dsstox_id:
        predecessor_generic_substance_record = \
            get_generic_substance_record_by_dsstox_id(predecessor_dsstox_id)
        if not predecessor_generic_substance_record:
            response = Response('DSSTox Substance ID(s) not found.',
                                status=404)
            return response
    else:
        predecessor_name = payload.get('predecessor_name')
        if not predecessor_name:
            response = Response('DSSTox Substance ID(s) not found.',
                                status=404)
            return response
        substance_id_by_name = get_generic_substance_id(predecessor_name)
        if not substance_id_by_name:
            response = Response('DSSTox Substance ID(s) not found.',
                                status=404)
            return response
        predecessor_smiles = payload.get('predecessor_smiles')
        if not predecessor_smiles:
            predecessor_generic_substance_record = \
                get_generic_substance_record_by_substance_id(
                    substance_id_by_name)
        else:
            inchi = indigo_inchi.getInchi(
                indigo.loadMolecule(predecessor_smiles))
            inchi_key = indigo_inchi.getInchiKey(inchi)
            substance_id_by_smiles = get_generic_substance_id(inchi_key)
            if substance_id_by_name != substance_id_by_smiles:
                response = Response('DSSTox Substance ID(s) not found.',
                                    status=404)
                return response
            predecessor_generic_substance_record = \
                get_generic_substance_record_by_substance_id(
                    substance_id_by_name)
    if not predecessor_generic_substance_record:
        response = Response('DSSTox Substance ID(s) not found.',
                            status=404)
        return response
    successor_dsstox_id = payload.get('successor_dsstox_id')
    if successor_dsstox_id:
        successor_generic_substance_record = \
            get_generic_substance_record_by_dsstox_id(successor_dsstox_id)
        if not successor_generic_substance_record:
            response = Response('DSSTox Substance ID(s) not found.',
                                status=404)
            return response
    else:
        successor_name = payload.get('successor_name')
        if successor_name:
            substance_id_by_name = get_generic_substance_id(successor_name)
            if not substance_id_by_name:
                response = Response('DSSTox Substance ID(s) not found.',
                                    status=404)
                return response
            successor_smiles = payload.get('successor_smiles')
            if not successor_smiles:
                successor_generic_substance_record = \
                    get_generic_substance_record_by_substance_id(
                        substance_id_by_name)
            else:
                inchi = indigo_inchi.getInchi(
                    indigo.loadMolecule(successor_smiles))
                inchi_key = indigo_inchi.getInchiKey(inchi)
                substance_id_by_smiles = get_generic_substance_id(inchi_key)
                if substance_id_by_name != substance_id_by_smiles:
                    response = Response('DSSTox Substance ID(s) not found.',
                                        status=404)
                    return response
                successor_generic_substance_record = \
                    get_generic_substance_record_by_substance_id(
                        substance_id_by_name)
        else:
            # Null record
            successor_generic_substance_record = model.GenericSubstances()
    if not successor_generic_substance_record:
        response = Response('DSSTox Substance ID(s) not found.',
                            status=404)
        return response
    substance_relationship_record = \
        get_substance_relationship_record(
            predecessor_generic_substance_record.id,
            successor_generic_substance_record.id
            )
    if not substance_relationship_record:
        record_already_exists = False
        substance_relationship_record = \
            create_and_post_new_substance_relationship(
                predecessor_generic_substance_record.id,
                successor_generic_substance_record.id
                )
    kinetic_data = [
        'pH', 'pH_min', 'pH_max', 'half_life', 'half_life_min',
        'half_life_max', 'half_life_units', 'rate', 'rate_min',
        'rate_max', 'rate_units', 'reaction', 'temp_C',
        'activation_kcal_per_mol'
        ]
    if not any([payload.get(column) for column in kinetic_data]):
        # Null record
        kinetics_record = model.Kinetics()
    else:
        kinetics_record = get_kinetics_record(
            substance_relationship_record.id, payload)
    if not kinetics_record:
        record_already_exists = False
        kinetics_record = create_and_post_new_kinetics_record(
            substance_relationship_record.id, payload)
    citation_record = get_citation_record(payload)
    if not citation_record:
        record_already_exists = False
        citation_record = create_and_post_new_citation_record(payload)
        post_and_map_authors(citation_record.id, payload)
    kinetics_citation_mapping = get_transformation_citation_mapping(
        substance_relationship_record.id,
        kinetics_record.id,
        citation_record.id
        )
    if not kinetics_citation_mapping:
        record_already_exists = False
        create_and_post_new_transformation_citation_mapping(
            substance_relationship_record.id,
            kinetics_record.id,
            citation_record.id
            )
    if record_already_exists:
        response = Response('Record already exists.', status=409)
        return response
    response = Response('Record successfully posted.', status=200)
    return response
