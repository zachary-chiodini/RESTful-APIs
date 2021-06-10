import model
from config import db, ma
from flask import Response
from responses import (
    entity_post_response, entity_get_response,
    record_id_get_response, record_id_put_response,
    record_id_patch_response, record_id_delete_response,
    entity_search_response
    )


class Entity:
    """
    This class contains all the methods that can
    be performed on a database entity by the API
    """
    def __init__(self, entity: db.Model,
                 schema: ma.SQLAlchemyAutoSchema):
        self.entity = entity
        self.schema = schema

    def get(self) -> Response:
        return entity_get_response(self.entity, self.schema)

    def post(self) -> Response:
        return entity_post_response(self.entity, self.schema)

    def search(self) -> Response:
        return entity_search_response(self.entity, self.schema)

    def get_record(self, primary_key: int) -> Response:
        return record_id_get_response(primary_key, self.entity, self.schema)

    def put(self, primary_key: int) -> Response:
        return record_id_put_response(primary_key, self.entity, self.schema)

    def patch(self, primary_key: int) -> Response:
        return record_id_patch_response(primary_key, self.entity, self.schema)

    def delete(self, primary_key) -> Response:
        return record_id_delete_response(primary_key, self.entity)


kinetics = Entity(model.Kinetics, model.KineticsSchema)
substance_relationships = Entity(
    model.SubstanceRelationships, model.SubstanceRelationshipsSchema)
generic_substances = Entity(
    model.GenericSubstances, model.GenericSubstancesSchema)
author = Entity(model.Author, model.AuthorSchema)
citation = Entity(model.Citation, model.CitationSchema)
