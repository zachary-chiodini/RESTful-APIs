import json
from typing import Dict, List, Optional, Tuple, Union

from flask import jsonify, Response, request

from flask_api import model
from flask_api.config import db, ma


def get_features_except_id(
        entity: db.Model, skip: List[str] = []
        ) -> Dict[str, db.Column]:
    features = dict(entity.__table__.columns.items())
    for label in skip:
        del features[label]
    if 'id' in features:
        del features['id']
    return features


def query_payload(
        entity: db.Model, payload: Dict
        ) -> Union[db.Model, None]:
    filters = []
    for label, column in get_features_except_id(entity).items():
        value = payload.get(label)
        filters.append(column == value)
    return entity.query.filter(*filters).one_or_none()


def entity_get_response(
        entity: db.Model,
        schema: ma.SQLAlchemyAutoSchema
        ) -> Response:
    select_all = entity.query.limit(1000).all()
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
        response = Response('Record already exists.', status=409)
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
        response = Response('Record not found.', status=404)
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


def record_id_patch_response(
        primary_key: int,
        entity: db.Model,
        schema: ma.SQLAlchemyAutoSchema
        ) -> Response:
    record_to_update = entity.query \
        .filter(entity.id == primary_key) \
        .one_or_none()
    if not record_to_update:
        response = Response('Record not found.', status=404)
        return response
    payload = json.loads(request.get_json())
    for feature in get_features_except_id(entity):
        if feature not in payload:
            payload[feature] = getattr(record_to_update, feature)
    existing_record = query_payload(entity, payload)
    if existing_record:
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
        response = Response('Record not found.', status=404)
        return response
    db.session.delete(record_to_delete)
    db.session.commit()
    response = Response('Record deleted.', status=200)
    return response


def entity_search_response(
        entity: db.Model,
        schema: ma.SQLAlchemyAutoSchema
        ) -> Response:
    parameters = request.args.to_dict()
    filters = []
    for label, column in get_features_except_id(entity).items():
        if label in parameters:
            value = parameters.get(label)
            filters.append(column == value)
            del parameters[label]
    if not filters or parameters:
        response = Response('The URL parameter(s) are incorrect '
                            'or not specified.', status=400)
        return response
    query = entity.query.filter(*filters).limit(1000).all()
    entity_schema = schema(many=True)
    response = jsonify(entity_schema.dump(query))
    response.status_code = 200
    return response


def reformat_joined_query(
        entities: List[db.Model],
        query: List[Tuple[db.Model]]
        ) -> List[Dict[str, db.Model]]:
    reformatted_query = []
    for tuple_ in query:
        for entity, record in zip(entities, tuple_):
            reformatted_query.append({entity.__tablename__: record})
    return reformatted_query


def entity_inner_join_response(
        main_entity: db.Model,
        secondary_entity: str,
        one_or_none: Optional[bool] = False
        ) -> Response:
    main_schema = getattr(model, main_entity.__name__ + 'Schema')
    for class_ in dir(model):
        model_object = getattr(model, class_)
        if getattr(model_object, '__tablename__', None) == secondary_entity:
            secondary_entity = model_object
            break
    # params: {'tablename.column': 'value'}
    parameters = request.args.to_dict()
    filters = []
    if parameters:
        model_features = {
            main_entity.__name__: get_features_except_id(main_entity),
            secondary_entity.__name__: get_features_except_id(secondary_entity)
            }
        for table_column, value in parameters:
            model_name, column_name = table_column.split('.')
            if column_name in model_features[model_name]:
                column_object = model_features[model_name][column_name]
                filters.append(column_object == value)
    if one_or_none:
        query = main_entity.query.join(secondary_entity)\
            .filter(*filters).one_or_none()
        entity_schema = main_schema()
    else:
        query = main_entity.query.join(secondary_entity) \
            .filter(*filters).limit(1000).all()
        entity_schema = main_schema(many=True)
    response = jsonify(entity_schema.dump(query))
    response.status_code = 200
    return response


def entity_inner_join_response2(
        main_entity: db.Model, *args: str
        ) -> Response:
    entities = [main_entity]
    schemas = [getattr(model, main_entity.__name__ + 'Schema')]
    for class_ in dir(model):
        obj = getattr(model, class_)
        if getattr(obj, '__tablename__', None) in args:
            entities.append(obj)
            schemas.append(getattr(model, obj.__name__ + 'Schema'))
    query = db.session.query(*entities)
    for other_entity in entities[1:]:
        query = query.join(other_entity)
    query = query.limit(1000).all()
    query = reformat_joined_query(entities, query)
    DynamicSchema = ma.Schema.from_dict({
        entity.__tablename__: ma.Nested(schema, dump_only=True)
        for entity, schema in zip(entities, schemas)
        })
    dynamic_schema = DynamicSchema(many=True)
    response = jsonify(dynamic_schema.dump(query))
    return response
