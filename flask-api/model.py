from datetime import datetime
from flask import url_for
from config import db, ma


class Kinetics(db.Model):
    __tablename__ = 'kinetics'
    id = db.Column(
        db.Integer, primary_key=True,
        autoincrement=True, nullable=False
        )
    fk_substance_relationship_id = db.Column(
        db.Integer, db.ForeignKey('substance_relationships.id'),
        nullable=False
        )
    pH = db.Column(db.Float)
    pH_min = db.Column(db.Float)
    pH_max = db.Column(db.Float)
    half_life = db.Column(db.Float)
    half_life_min = db.Column(db.Float)
    half_life_max = db.Column(db.Float)
    half_life_units = db.Column(db.String)
    rate = db.Column(db.Float)
    rate_min = db.Column(db.Float)
    rate_max = db.Column(db.Float)
    rate_units = db.Column(db.String)
    reaction = db.Column(db.String)
    temp_C = db.Column(db.Float)
    activation_kcal_per_mol = db.Column(db.Float)
    comments = db.Column(db.String)


class KineticsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Kinetics
        load_instance = True

    uri = ma.Function(
        lambda obj:
        url_for('/api.operations_kinetics_get_record',
                primary_key=obj.id, _external=True)
        )


class SubstanceRelationships(db.Model):
    __tablename__ = 'substance_relationships'
    id = db.Column(
        db.Integer, primary_key=True,
        autoincrement=True, nullable=False
        )
    fk_generic_substance_id_predecessor = db.Column(
        db.Integer, db.ForeignKey('generic_substances.id'),
        nullable=False
        )
    fk_generic_substance_id_successor = db.Column(
        db.Integer, db.ForeignKey('generic_substances.id')
        )
    relationship = db.Column(db.String)
    fk_substance_relationship_type_id = db.Column(db.Integer)
    source = db.Column(db.String)
    qc_notes = db.Column(db.String)
    mixture_percentage = db.Column(db.Float)
    percentage_type = db.Column(db.String)
    is_nearest_structure = db.Column(db.Integer)
    is_nearest_casrn = db.Column(db.Integer)
    created_by = db.Column(db.String, nullable=False)
    updated_by = db.Column(db.String, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow,
        onupdate=datetime.utcnow, nullable=False
        )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow,
        onupdate=datetime.utcnow, nullable=False
        )
    # unidirectional
    kinetic_data = db.relationship('Kinetics')


class SubstanceRelationshipsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SubstanceRelationships
        load_instance = True
    uri = ma.Function(
        lambda obj:
        url_for('/api.operations_substance_relationships_get_record',
                primary_key=obj.id, _external=True)
            )


class GenericSubstances(db.Model):
    __tablename__ = 'generic_substances'
    id = db.Column(
        db.Integer, primary_key=True,
        autoincrement=True, nullable=False
        )
    fk_qc_level_id = db.Column(db.Integer)
    dsstox_substance_id = db.Column(db.String)
    casrn = db.Column(db.String)
    preferred_name = db.Column(db.String)
    substance_type = db.Column(db.String)
    qc_notes = db.Column(db.String)
    qc_notes_private = db.Column(db.String)
    source = db.Column(db.String)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow,
        onupdate=datetime.utcnow, nullable=False
        )
    updated_by = db.Column(
        db.DateTime, default=datetime.utcnow,
        onupdate=datetime.utcnow, nullable=False
        )
    # unidirectional
    predecessor_relationship = db.relationship(
        'SubstanceRelationships',
        foreign_keys=[
            SubstanceRelationships
                .fk_generic_substance_id_predecessor
            ]
        )
    successor_relationship = db.relationship(
        'SubstanceRelationships',
        foreign_keys=[
            SubstanceRelationships
                .fk_generic_substance_id_successor
            ]
        )


class GenericSubstancesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GenericSubstances
        load_instance = True
    uri = ma.Function(
        lambda obj:
        url_for('/api.operations_generic_substances_get_record',
                primary_key=obj.id, _external=True)
        )


author_cited = db.Table(
    'author_cited',
    db.Column(
        'fk_citation_id', db.Integer, db.ForeignKey('citation.id'),
        primary_key=True
        ),
    db.Column(
        'fk_author_id', db.Integer, db.ForeignKey('author.id'),
        primary_key=True
        )
    )

kinetics_cited = db.Table(
    'kinetics_cited',
    db.Column(
        'fk_citation_id', db.Integer, db.ForeignKey('citation.id'),
        primary_key=True
        ),
    db.Column(
        'fk_kinetics_id', db.Integer, db.ForeignKey('kinetics.id'),
        primary_key=True
        )
    )


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(
        db.Integer, primary_key=True,
        autoincrement=True, nullable=False
        )
    first_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    last_name = db.Column(db.String)


class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Author
        load_instance = True
    uri = ma.Function(
        lambda obj:
        url_for('/api.operations_author_get_record',
                primary_key=obj.id, _external=True)
        )


class Citation(db.Model):
    __tablename__ = 'citation'
    id = db.Column(
        db.Integer, primary_key=True,
        autoincrement=True, nullable=False
        )
    doi = db.Column(db.String)
    url = db.Column(db.String)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    volume = db.Column(db.Integer)
    issue = db.Column(db.String)
    pages = db.Column(db.String)
    title = db.Column(db.String)
    pdf = db.Column(db.LargeBinary)
    author = db.relationship(
        'Author',
        secondary=author_cited,
        lazy='subquery',
        backref=db.backref('citation', lazy=True)
        )
    kinetics = db.relationship(
        'Kinetics',
        secondary=kinetics_cited,
        lazy='subquery',
        backref=db.backref('citation', lazy=True)
        )


class CitationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Citation
        load_instance = True
    uri = ma.Function(
        lambda obj:
        url_for('/api.operations_citation_get_record',
                primary_key=obj.id, _external=True)
        )
