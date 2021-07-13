from flask import url_for

from flask_api.config import db, ma


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
        include_fk = True
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
    # unidirectional
    kinetic_data = db.relationship('Kinetics')


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


author_cited = db.Table(
    'author_cited',
    db.Column('id', db.Integer, primary_key=True,
              autoincrement=True, nullable=False),
    db.Column(
        'fk_citation_id', db.Integer, db.ForeignKey('citation.id'),
        nullable=False
        ),
    db.Column(
        'fk_author_id', db.Integer, db.ForeignKey('author.id'),
        nullable=False
        )
    )


transformation_cited = db.Table(
    'transformation_cited',
    db.Column('id', db.Integer, primary_key=True,
              autoincrement=True, nullable=False),
    db.Column(
        'fk_substance_relationship_id', db.Integer,
        db.ForeignKey('substance_relationships.id'),
        nullable=False
        ),
    db.Column(
        'fk_kinetics_id', db.Integer, db.ForeignKey('kinetics.id'),
        nullable=True
        ),
    db.Column(
        'fk_citation_id', db.Integer, db.ForeignKey('citation.id'),
        nullable=False
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
    publisher = db.Column(db.String)
    volume = db.Column(db.Integer)
    issue = db.Column(db.String)
    pages = db.Column(db.String)
    title = db.Column(db.String)
    journal = db.Column(db.String)
    pdf = db.Column(db.LargeBinary)
    author = db.relationship(
        'Author',
        secondary=author_cited,
        lazy='subquery',
        backref=db.backref('citation', lazy=True)
        )
    kinetics = db.relationship(
        'Kinetics',
        secondary=transformation_cited,
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


class TransformationView(db.Model):
    """
    SELECT
        PRED.dsstox_substance_id AS 'Predecessor DSSTox ID',
        PRED.preferred_name AS 'Predecessor Preferred Name',
        PRED.casrn AS 'Predecessor CASRN',
        PRED.smiles AS 'Predecessor SMILES',
        PRED.substance_type AS 'Predecessor Type',
        PRED.label AS 'Predecessor Name:SMILES:CASRN QC Level',
        SUCC.dsstox_substance_id AS 'Successor DSSTox ID',
        SUCC.preferred_name AS 'Successor Preferred Name',
        SUCC.smiles AS 'Successor SMILES',
        SUCC.casrn AS 'Successor CASRN',
        SUCC.substance_type AS 'Successor Type',
        SUCC.label AS 'Successor Name:SMILES:CASRN QC Level',
        SR.relationship AS 'Relationship',
        K.pH,
        K.pH_min AS 'Minimum pH',
        K.pH_max as 'Maximum pH',
        K.half_life AS 'Half-life',
        K.half_life_min AS 'Minimum Half-life',
        K.half_life_max AS 'Maximum Half-life',
        K.half_life_units AS 'Half-life Units',
        K.rate AS 'Rate Constant',
        K.rate_min AS 'Minimum Rate Constant',
        K.rate_max AS 'Maximum Rate Constant',
        K.rate_units AS 'Rate Constant Units',
        K.activation_kcal_per_mol AS 'Activation Energy (kcal/mol)',
        K.temp_C AS 'Temperature Centigrade',
        K.reaction AS 'Reaction',
        K.comments AS 'Comments',
        GROUP_CONCAT(
            CASE
                WHEN CONCAT_WS(' ', A.first_name, A.middle_name, A.last_name) = ' '
                THEN NULL
                ELSE CONCAT_WS(' ', A.first_name, A.middle_name, A.last_name)
            END
            ORDER BY A.last_name
            SEPARATOR ', '
            ) AS 'Authors',
        C.year AS 'Year',
        C.month AS 'Month',
        C.day AS 'Day',
        C.publisher AS 'Publisher',
        C.title AS 'Title',
        C.journal AS 'Journal',
        C.volume AS 'Volume',
        C.issue AS 'Issue',
        C.pages AS 'Pages',
        C.doi AS 'DOI',
        c.url AS 'URL',
        C.pdf AS 'PDF Blob'
    FROM
        sbox_zchiodini_dsstox.substance_relationships SR
        INNER JOIN sbox_zchiodini_dsstox.substance_relationship_types SRT
            ON SR.fk_substance_relationship_type_id = SRT.id
        INNER JOIN ( -- predecessor substance
            SELECT
                GSP.id,
                GSP.dsstox_substance_id,
                GSP.preferred_name,
                GSP.casrn,
                CP.smiles,
                GSP.substance_type,
                QCP.label
            FROM
                sbox_zchiodini_dsstox.generic_substances GSP
                INNER JOIN sbox_zchiodini_dsstox.qc_levels QCP
                    ON GSP.fk_qc_level_id = QCP.id
                LEFT JOIN sbox_zchiodini_dsstox.generic_substance_compounds GSCP
                    ON GSCP.fk_generic_substance_id = GSP.id
                LEFT JOIN sbox_zchiodini_dsstox.compounds CP
                    ON GSCP.fk_compound_id = CP.id
            )
        AS PRED
            ON SR.fk_generic_substance_id_predecessor = PRED.id
        LEFT JOIN ( -- successor substance
            SELECT
                GSS.id,
                GSS.dsstox_substance_id,
                GSS.preferred_name,
                GSS.casrn,
                CS.smiles,
                GSS.substance_type,
                QCS.label
            FROM
                sbox_zchiodini_dsstox.generic_substances GSS
                INNER JOIN sbox_zchiodini_dsstox.qc_levels QCS
                    ON GSS.fk_qc_level_id = QCS.id
                LEFT JOIN sbox_zchiodini_dsstox.generic_substance_compounds GSCS
                    ON GSCS.fk_generic_substance_id = GSS.id
                LEFT JOIN sbox_zchiodini_dsstox.compounds CS
                    ON GSCS.fk_compound_id = CS.id
            )
        AS SUCC
            ON SR.fk_generic_substance_id_successor = SUCC.id
        LEFT JOIN kinetics K
            ON K.fk_substance_relationship_id = SR.id
        INNER JOIN transformation_cited TC
            ON TC.fk_substance_relationship_id = SR.id
        INNER JOIN citation C
            ON TC.fk_citation_id = C.id
        LEFT JOIN author_cited AC
            ON AC.fk_citation_id = C.id
        LEFT JOIN author A
            ON AC.fk_author_id = A.id
    WHERE
        SRT.name = 'transformation_product'
    GROUP BY
        PRED.dsstox_substance_id,
        PRED.preferred_name,
        PRED.smiles,
        PRED.casrn,
        PRED.substance_type,
        PRED.label,
        SUCC.dsstox_substance_id,
        SUCC.preferred_name,
        SUCC.smiles,
        SUCC.casrn,
        SUCC.substance_type,
        SUCC.label,
        SR.relationship,
        K.pH,
        K.pH_min,
        K.pH_max,
        K.half_life,
        K.half_life_min,
        K.half_life_max,
        K.half_life_units,
        K.rate,
        K.rate_min,
        K.rate_max,
        K.rate_units,
        K.activation_kcal_per_mol,
        K.temp_C,
        K.reaction,
        K.comments,
        C.month,
        C.day,
        C.year,
        C.publisher,
        C.title,
        C.journal,
        C.volume,
        C.issue,
        C.pages,
        C.doi,
        C.url,
        C.pdf
    ;
    """
    __tablename__ = 'transformation_view'
    predecessor_dsstox_id = db.Column(
        'Predecessor DSSTox ID', db.String, primary_key=True)
    predecessor_preferred_name = db.Column(
        'Predecessor Preferred Name', db.String, primary_key=True)
    predecessor_smiles = db.Column(
        'Predecessor SMILES', db.String, primary_key=True)
    predecessor_casrn = db.Column(
        'Predecessor CASRN', db.String, primary_key=True)
    predecessor_type = db.Column(
        'Predecessor Type', db.String, primary_key=True)
    predecessor_qc_level = db.Column(
        'Predecessor Name:SMILES:CASRN QC Level', db.String, primary_key=True)
    successor_dsstox_id = db.Column(
        'Successor DSSTox ID', db.String, primary_key=True)
    successor_preferred_name = db.Column(
        'Successor Preferred Name', db.String, primary_key=True)
    successor_smiles = db.Column(
        'Successor SMILES', db.String, primary_key=True)
    successor_casrn = db.Column(
        'Successor CASRN', db.String, primary_key=True)
    successor_type = db.Column(
        'Successor Type', db.String, primary_key=True)
    successor_qc_level = db.Column(
        'Successor Name:SMILES:CASRN QC Level', db.String, primary_key=True)
    relationship = db.Column(
        'Relationship', db.String, primary_key=True)
    pH = db.Column(db.Float, primary_key=True)
    pH_min = db.Column('Minimum pH', db.Float, primary_key=True)
    pH_max = db.Column('Maximum pH', db.Float, primary_key=True)
    half_life = db.Column('Half-life', db.Float, primary_key=True)
    half_life_min = db.Column(
        'Minimum Half-life', db.Float, primary_key=True)
    half_life_max = db.Column(
        'Maximum Half-life', db.Float, primary_key=True)
    half_life_units = db.Column(
        'Half-life Units', db.String, primary_key=True)
    rate = db.Column(
        'Rate Constant', db.Float, primary_key=True)
    rate_min = db.Column(
        'Minimum Rate Constant', db.Float, primary_key=True)
    rate_max = db.Column(
        'Maximum Rate Constant', db.Float, primary_key=True)
    rate_units = db.Column(
        'Rate Constant Units', db.String, primary_key=True)
    activation_kcal_per_mol = db.Column(
        'Activation Energy (kcal/mol)', db.Float, primary_key=True)
    temp_C = db.Column(
        'Temperature Centigrade', db.Float, primary_key=True)
    reaction = db.Column(
        'Reaction', db.String, primary_key=True)
    comments = db.Column('Comments', db.String, primary_key=True)
    authors = db.Column('Authors', db.String, primary_key=True)
    year = db.Column('Year', db.Integer, primary_key=True)
    month = db.Column('Month', db.Integer, primary_key=True)
    day = db.Column('Day', db.Integer, primary_key=True)
    publisher = db.Column('Publisher', db.String, primary_key=True)
    title = db.Column('Title', db.String, primary_key=True)
    journal = db.Column('Journal', db.String, primary_key=True)
    volume = db.Column('Volume', db.Integer, primary_key=True)
    issue = db.Column('Issue', db.String, primary_key=True)
    pages = db.Column('Pages', db.String, primary_key=True)
    doi = db.Column('DOI', db.String, primary_key=True)
    url = db.Column('URL', db.String, primary_key=True)
    pdf = db.Column('PDF Blob', db.LargeBinary, primary_key=True)


class TransformationViewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TransformationView
        load_instance = True
