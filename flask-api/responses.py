import json
from config import db, ma
from flask import jsonify, Response, request
from sqlalchemy.orm.attributes import InstrumentedAttribute
from typing import Dict, Optional, Union


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
        entity: db.Model, payload: Dict
        ) -> Union[db.Model, None]:
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
        schema: ma.SQLAlchemyAutoSchema,
        primary_key: Optional[int] = None
        ) -> Response:
    payload = json.loads(request.get_json())
    record_already_exists = query_payload(entity, payload)
    if record_already_exists:
        response = Response('Record already exists', status=409)
        return response
    entity_schema = schema()
    new_record = entity_schema.load(payload, session=db.session)
    # The primary key is only specified when the
    # put method does not find a record to update.
    if primary_key and request.method == 'PUT':
        new_record.id = primary_key
    db.session.add(new_record)
    db.session.commit()
    response = jsonify(entity_schema.dump(new_record))
    response.status_code = 201
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
        response = Response('Record not found', status=404)
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
        return entity_post_response(entity, schema, primary_key)
    payload = json.loads(request.get_json())
    existing_record = query_payload(entity, payload)
    if existing_record and existing_record.id != primary_key:
        response = Response('Record already exists', status=409)
        return response
    entity_schema = schema()
    updated_record = entity_schema.load(payload, session=db.session)
    updated_record.id = record_to_update.id
    db.session.merge(updated_record)
    db.session.commit()
    response = jsonify(entity_schema.dump(updated_record))
    response.status_code = 200
    return response


def record_id_patch_response(
        primary_key: int,
        entity: db.Model,
        schema: ma.SQLAlchemyAutoSchema
        ) -> Response:
    record_to_update = entity.query \
        .filter(entity.id == primary_key) \
        .one_or_none()
    if not record_to_update:
        response = Response('Record not found', status=404)
        return response
    payload = json.loads(request.get_json())
    for feature in get_features(entity).keys():
        if feature not in payload:
            payload[feature] = getattr(record_to_update, feature)
    existing_record = query_payload(entity, payload)
    if existing_record:
        response = Response('Record already exists', status=409)
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
