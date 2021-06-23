import json
import model
from config import db
from flask import Response, request
from responses import get_features_except_id, query_payload
from typing import Dict, Union


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
        'fk_relationship_type_id': 1,
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
    for label in get_features_except_id(
            model.Kinetics, skip=['fk_substance_relationship_id']
            ).keys():
        value = payload.get(label)
        new_kinetics_data.update(label=value)
    new_kinetics_data.update(
        fk_substance_relationship_id=substance_relationship_id)
    schema = model.SubstanceRelationshipsSchema()
    kinetics_record = schema.load(
        new_kinetics_data, session=db.session)
    db.session.add(kinetics_record)
    db.session.commit()
    return kinetics_record


def get_kinetics_record(substance_relationship_id: int,
                        payload: Dict) -> Union[db.Model, None]:
    new_kinetics_data = {}
    for label in get_features_except_id(
            model.Kinetics, skip=['fk_substance_relationship_id']
            ).keys():
        value = payload.get(label)
        new_kinetics_data.update(label=value)
    new_kinetics_data.update(
        fk_substance_relationship_id=substance_relationship_id)
    kinetics_record = query_payload(
        model.Kinetics, new_kinetics_data)
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
    for label in get_features_except_id(model.Citation).keys():
        value = payload.get(label)
        new_citation_data.update(label=value)
    schema = model.CitationSchema()
    citation_record = schema.load(
        new_citation_data, session=db.session)
    db.session.add(citation_record)
    db.session.commit()
    return citation_record


def get_kinetics_citation_mapping(
        kinetics_record_id: int,
        citation_record_id: int
        ) -> Union[db.Model, None]:
    kinetics_citation_mapping = model.kinetics_cited.query\
        .filter(
            model.kinetics_cited.fk_kinetics_id == kinetics_record_id,
            model.kinetics_cited.fk_citation_id == citation_record_id
            )\
        .one_or_none()
    return kinetics_citation_mapping


def get_generic_substance_record(
        dsstox_id: int) -> Union[db.Model, None]:
    generic_substance_record = model.GenericSubstances.query\
        .filter(model.GenericSubstances
                .dsstox_substance_id == dsstox_id)\
        .one_or_none()
    return generic_substance_record


def create_and_post_new_kinetics_citation_mapping(
        kinetics_record_id: int,
        citation_record_id: int
        ) -> Union[db.Model, None]:
    new_mapping_data = dict(
        fk_kineitcs_id=kinetics_record_id,
        fk_citation_id=citation_record_id
        )
    schema = model.kinetics_cited()
    new_mapping_record = schema.load(
        new_mapping_data, session=db.session)
    db.session.add(new_mapping_record)
    db.session.commit()
    return new_mapping_record


def post_and_map_authors(citation_id, payload: Dict) -> None:
    for author in payload.get('authors').split(','):
        first_name, middle_name, last_name = author.split()
        author_data = {'first_name': first_name,
                       'middle_name': middle_name,
                       'last_name': last_name}
        author_record = query_payload(model.Author, author_data)
        if author_record:
            author_citation_mapping = model.author_cited\
                .filter(
                    model.author_cited.fk_author_id == author_record.id,
                    model.author_cited.fk_citation_id == citation_id
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
        new_mapping_data = dict(
            fk_citation_id=citation_id,
            fk_author_id=author_record.id
            )
        schema = model.author_cited()
        new_mapping_record = schema.load(
            new_mapping_data, session=db.session)
        db.session.add(new_mapping_record)
        db.session.commit()
    return None


def get_substance_id(identifier: str) -> Union[str, None]:
    substance_id = model.SynonymMv\
        .query(model.SynonymMv.fk_generic_substance_id)\
        .filter(model.SynonymMv.identifier == identifier)\
        .order_by(model.SynonymMv.rank)\
        .first()
    return substance_id.fk_generic_substance_id


def get_substance_id_if_valid(
        chem_name: str, smiles: str
        ) -> Union[str, None]:
    substance_id_by_name = get_substance_id(chem_name)
    if substance_id_by_name:
        substance_id_by_smiles = get_substance_id(smiles)
        if substance_id_by_name == substance_id_by_smiles:
            return substance_id_by_name
    return None


def post_new_transformation_record() -> Response:
    payload = json.loads(request.get_json())
    predecessor_dsstox_id = payload.get('predecessor_dsstox_id')
    predecessor_dsstox_id = payload.get('predecessor_dsstox_id')
    successor_dsstox_id = payload.get('successor_dsstox_id')
    if predecessor_dsstox_id and successor_dsstox_id:
        predecessor_generic_substance_record = \
            get_generic_substance_record(predecessor_dsstox_id)
        successor_generic_substance_record = \
            get_generic_substance_record(successor_dsstox_id)
    else:
        response = Response('DSSTox Substance ID(s) not found.',
                            status=404)
        return response
    if (predecessor_generic_substance_record
            and successor_generic_substance_record):
        substance_relationship_record = \
            get_substance_relationship_record(
                predecessor_generic_substance_record.id,
                successor_generic_substance_record.id
                )
    else:
        response = Response('DSSTox Substance ID(s) not found.',
                            status=404)
        return response
    if not substance_relationship_record:
        substance_relationship_record = \
            create_and_post_new_substance_relationship(
                predecessor_generic_substance_record.id,
                successor_generic_substance_record.id
                )
    kinetics_record = get_kinetics_record(
        substance_relationship_record.id, payload)
    if not kinetics_record:
        kinetics_record = create_and_post_new_kinetics_record(
            substance_relationship_record.id, payload)
    citation_record = get_citation_record(payload)
    if not citation_record:
        citation_record = create_and_post_new_citation_record(payload)
        post_and_map_authors(citation_record.id, payload)
    kinetics_citation_mapping = get_kinetics_citation_mapping(
        kinetics_record.id, citation_record.id)
    if not kinetics_citation_mapping:
        create_and_post_new_kinetics_citation_mapping(
            kinetics_record.id, citation_record.id)
    else:
        response = Response('Record already exists.', status=409)
        return response
    response = Response('Record successfully posted.', status=200)
    return response
