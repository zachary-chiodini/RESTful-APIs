import model
from entity import View, Entity

transformation_view = View(
    model.TransformationView, model.TransformationViewSchema)
kinetics = Entity(model.Kinetics, model.KineticsSchema)
author = Entity(model.Author, model.AuthorSchema)
citation = Entity(model.Citation, model.CitationSchema)
