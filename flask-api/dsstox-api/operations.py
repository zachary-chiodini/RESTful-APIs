from ..shared import model
from ..shared.entity import Entity

substance_relationships = Entity(
    model.SubstanceRelationships, model.SubstanceRelationshipsSchema)
generic_substances = Entity(
    model.GenericSubstances, model.GenericSubstancesSchema)
compounds = Entity(model.Compounds, model.CompoundsSchema)
