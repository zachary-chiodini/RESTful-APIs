from flask import url_for
from config import db, ma


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
    fk_substance_relationship_type_id = db.Column(
        db.Integer, db.ForeignKey('substance_relationship_types.id'),
        nullable=False
        )
    source = db.Column(db.String)
    qc_notes = db.Column(db.String)
    mixture_percentage = db.Column(db.Float)
    percentage_type = db.Column(db.String)
    is_nearest_structure = db.Column(db.Integer)
    is_nearest_casrn = db.Column(db.Integer)
    created_by = db.Column(db.String)
    updated_by = db.Column(db.String)


class SubstanceRelationshipsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SubstanceRelationships
        load_instance = True
        include_fk = True
    uri = ma.Function(
        lambda obj:
        url_for('/api.operations_substance_relationships_get_record',
                primary_key=obj.id, _external=True)
        )


class SubstanceRelationshipTypes(db.Model):
    __tablename__ = 'substance_relationship_types'
    id = db.Column(
        db.Integer, primary_key=True,
        autoincrement=True, nullable=False
        )
    name = db.Column(db.String)
    label_forward = db.Column(db.String)
    short_description_forward = db.Column(db.String)
    long_description_forward = db.Column(db.String)
    label_backward = db.Column(db.String)
    short_description_backward = db.Column(db.String)
    long_description_backward = db.Column(db.String)
    created_by = db.Column(db.String)
    updated_by = db.Column(db.String)
    created_at = db.Column(db.String)
    updated_at = db.Column(db.String)
    # unidirectional
    substance_relationship_data = \
        db.relationship('SubstanceRelationships')


class SubstanceRelationshipTypesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SubstanceRelationshipTypes
        load_instance = True


class SynonymMv(db.Model):
    __tablename__ = 'synonym_mv'
    id = db.Column(
        db.Integer, primary_key=True,
        autoincrement=True, nullable=False
        )
    fk_generic_substance_id = db.Column(
        db.Integer, db.ForeignKey('generic_substances.id'),
        nullable=True
        )
    identifier = db.Column(db.String)
    synonym_type = db.Column(db.String)
    rank = db.Column(db.Integer)


class SynonymMvSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SynonymMv
        load_instance = True
        include_fk = True


generic_substance_compounds = db.Table(
    'generic_substance_compounds',
    db.Column('id', db.Integer, primary_key=True,
              autoincrement=True, nullable=False),
    db.Column(
        'fk_generic_substance_id', db.Integer,
        db.ForeignKey('generic_substances.id'),
        nullable=False
        ),
    db.Column(
        'fk_compound_id', db.Integer, db.ForeignKey('compounds.id'),
        nullable=False
        ),
    db.Column('relationship', db.String),
    db.Column('source', db.String),
    db.Column('created_by', db.String),
    db.Column('updated_by', db.String),
    db.Column('created_at', db.String),
    db.Column('updated_at', db.String)
    )


class Compounds(db.Model):
    __tablename__ = 'compounds'
    id = db.Column(
        db.Integer, primary_key=True,
        autoincrement=True, nullable=False
        )
    dsstox_compound_id = db.Column(db.String)
    chiral_stereo = db.Column(db.String)
    chemical_type = db.Column(db.String)
    organic_form = db.Column(db.String)
    mrv_file = db.Column(db.String)
    mol_file = db.Column(db.String)
    mol_file_3d = db.Column(db.String)
    smiles = db.Column(db.String)
    inchi = db.Column(db.String)
    jchem_inchi_key = db.Column(db.String)
    indigo_inchi_key = db.Column(db.String)
    acd_iupac_name = db.Column(db.String)
    acd_index_name = db.Column(db.String)
    mol_formula = db.Column(db.String)
    mol_weight = db.Column(db.Float)
    monoisotopic_mass = db.Column(db.Float)
    fragment_count = db.Column(db.Integer)
    has_defined_isotope = db.Column(db.Integer)
    radical_count = db.Column(db.Integer)
    pubchem_cid = db.Column(db.Integer)
    chemspider_id = db.Column(db.Integer)
    chebi_id = db.Column(db.Integer)
    created_by = db.Column(db.String)
    updated_by = db.Column(db.String)
    created_at = db.Column(db.String)
    updated_at = db.Column(db.String)
    mol_image_png = db.Column(db.LargeBinary)


class CompoundsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Compounds
        load_instance = True
    uri = ma.Function(
        lambda obj:
        url_for('/api.operations_compounds_get_record',
                primary_key=obj.id, _external=True)
        )


class GenericSubstances(db.Model):
    __tablename__ = 'generic_substances'
    id = db.Column(
        db.Integer, primary_key=True,
        autoincrement=True, nullable=False
        )
    fk_qc_level_id = db.Column(
        db.Integer, db.ForeignKey('qc_levels.id'),
        nullable=False
        )
    dsstox_substance_id = db.Column(db.String)
    casrn = db.Column(db.String)
    preferred_name = db.Column(db.String)
    substance_type = db.Column(db.String)
    qc_notes = db.Column(db.String)
    qc_notes_private = db.Column(db.String)
    source = db.Column(db.String)
    created_by = db.Column(db.String)
    updated_by = db.Column(db.String)
    created_at = db.Column(db.String)
    updated_at = db.Column(db.String)
    structure = db.relationship(
        'Compounds',
        secondary=generic_substance_compounds,
        lazy='subquery',
        backref=db.backref('generic_substances', lazy=True)
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
    synonym_mv = db.relationship(
        'SynonymMv',
        foreign_keys=[
            SynonymMv.fk_generic_substance_id
            ]
        )


class GenericSubstancesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GenericSubstances
        load_instance = True
        include_fk = True
    uri = ma.Function(
        lambda obj:
        url_for('/api.operations_generic_substances_get_record',
                primary_key=obj.id, _external=True)
        )


class QCLevels(db.Model):
    __tablename__ = 'qc_levels'
    id = db.Column(
        db.Integer, primary_key=True,
        autoincrement=True, nullable=False
        )
    name = db.Column(db.String)
    label = db.Column(db.String)
    description = db.Column(db.String)
    created_by = db.Column(db.String)
    updated_by = db.Column(db.String)
    created_at = db.Column(db.String)
    updated_at = db.Column(db.String)
    # unidirectional
    relationship = db.relationship('GenericSubstances')


class QCLevelsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = QCLevels
        load_instance = True
