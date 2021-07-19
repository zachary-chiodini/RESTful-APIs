from flask_api import model
from flask_api.entity import Entity

substance_relationships = Entity(
    model.SubstanceRelationships, model.SubstanceRelationshipsSchema)
generic_substances = Entity(
    model.GenericSubstances, model.GenericSubstancesSchema)
compounds = Entity(model.Compounds, model.CompoundsSchema)
