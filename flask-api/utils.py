import json
from config import db, ma
from flask import jsonify, Response, request
from typing import Dict, List, Union
from sqlalchemy.orm.attributes import InstrumentedAttribute


def get_features(entity: db.Model) -> Dict:
    features = {}
    instantiated = entity()
    for attr, value in entity.__dict__.items():
        if (isinstance(value, InstrumentedAttribute)
                and getattr(instantiated, attr) is None
                and attr != 'id'):
            features[attr] = value
    return features


def query_payload(
        entity: db.Model,
        payload: Dict
        ) -> Union[List, None]:
    filters = []
    for label, column in get_features(entity).items():
        value = payload.get(label)
        filters.append(column == value)
    return entity.query.filter(*filters).one_or_none()


def entity_get_response(
        entity: db.Model,
        schema: ma.SQLAlchemyAutoSchema
        ) -> Response:
    select_all = entity.query.all()
    entity_schema = schema(many=True)
    response = jsonify(entity_schema.dump(select_all))
    response.status_code = 200
    return response


def entity_post_response(
        entity: db.Model,
        schema: ma.SQLAlchemyAutoSchema
        ) -> Response:
    payload = json.loads(request.get_json())
    record_already_exists = query_payload(entity, payload)
    if record_already_exists:
        response = Response('Record already exists.', status=409)
        return response
    entity_schema = schema()
    new_record = entity_schema.load(payload, session=db.session)
    db.session.add(new_record)
    db.session.commit()
    response = jsonify(entity_schema.dump(new_record))
    response.status_code = 201
    return response


def entity_get_or_post_response(
        entity: db.Model,
        schema: ma.SQLAlchemyAutoSchema
        ) -> Response:
    if request.method == 'GET':
        return entity_get_response(entity, schema)
    if request.method == 'POST':
        return entity_post_response(entity, schema)
    response = Response('Method not allowed.', status=405)
    return response


def record_id_get_response(
        primary_key: int,
        entity: db.Model,
        schema: ma.SQLAlchemyAutoSchema
        ) -> Response:
    record = entity.query\
        .filter(entity.id == primary_key) \
        .one_or_none()
    if not record:
        response = Response('Record id not found.', status=404)
        return response
    entity_schema = schema()
    response = jsonify(entity_schema.dump(record))
    response.status_code = 200
    return response


def record_id_put_response(
        primary_key: int,
        entity: db.Model,
        schema: ma.SQLAlchemyAutoSchema
        ) -> Response:
    record_to_update = entity.query\
        .filter(entity.id == primary_key)\
        .one_or_none()
    if not record_to_update:
        return entity_post_response(entity, schema)
    payload = json.loads(request.get_json())
    existing_record = query_payload(entity, payload)
    if existing_record and existing_record.id != primary_key:
        response = Response('Record already exists.', status=409)
        return response
    entity_schema = schema()
    updated_record = entity_schema.load(payload, session=db.session)
    updated_record.id = record_to_update.id
    db.session.merge(updated_record)
    db.session.commit()
    response = jsonify(entity_schema.dump(updated_record))
    response.status_code = 200
    return response


def record_id_delete_response(
        primary_key: int,
        entity: db.Model
        ) -> Response:
    record_to_delete = entity.query\
        .filter(entity.id == primary_key)\
        .one_or_none()
    if not record_to_delete:
        response = Response('Record id not found.', status=404)
        return response
    db.session.delete(record_to_delete)
    db.session.commit()
    response = Response('Record deleted.', status=200)
    return response


def record_id_response(
        primary_key: int,
        entity: db.Model,
        schema: ma.SQLAlchemyAutoSchema
        ) -> Response:
    if request.method == 'GET':
        return record_id_get_response(primary_key, entity, schema)
    if request.method == 'PUT':
        return record_id_put_response(primary_key, entity, schema)
    if request.method == 'DELETE':
        return record_id_delete_response(primary_key, entity)
    response = Response('Method not allowed.', status=405)
    return response
