from pathlib import Path
from typing import Tuple, Iterator

import pandas as pd
from oaklib.cli import ontology_versions
from oaklib.datamodels.vocabulary import HAS_DEFINITION_CURIE, RDFS_LABEL, OWL_VERSION_IRI
from rdflib.plugins.shared.jsonld.keys import VERSION
from rdkit import Chem
from semsql.sqla.semsql import Statements, Edge, EntailedEdge
from sqlalchemy import select, Select, not_
from sqlalchemy.orm import Session
from sqlalchemy.orm.loading import instances
from sssom.constants import RDFS_SUBCLASS_OF

from c3p.datamodel import ChemicalStructure, ChemicalClass, Dataset

SMILES = "obo:chebi/smiles"

import re


def sanitize_smiles(smiles_string):
    """
    Sanitizes a SMILES string by:
    1. Removing whitespace
    2. Removing invalid characters
    3. Preserving valid SMILES characters including brackets, numbers, and symbols

    Args:
        smiles_string (str): Input SMILES string

    Returns:
        str: Sanitized SMILES string
    """
    # Remove whitespace
    smiles = smiles_string.strip()

    # Define valid SMILES characters
    # Includes:
    # - Atomic symbols (B, C, N, O, P, S, F, Cl, Br, I, etc.)
    # - Numbers and % for ring closures
    # - Special characters ([, ], (, ), =, #, /, \, @, +, -, ., *)
    # - Colons for aromatic bonds
    # - Commas for atom lists in brackets
    pattern = r'[^A-Za-z0-9\[\]\(\)=#/\\@+\-\.\*%:,]'

    # Remove invalid characters
    sanitized = re.sub(pattern, '', smiles)

    return sanitized

def eav_to_df(eav_df: pd.DataFrame, value_column='value') -> pd.DataFrame:
    """
    Convert an EAV DataFrame to a wide-format DataFrame.

    Example:

        >>> test_eav_df = pd.DataFrame({
        ...    'subject': ['a', 'a', 'b', 'b', 'b', 'c'],
        ...    'predicate': ['p1', 'p1', 'p1', 'p1', 'p2', 'p3'],
        ...    'value': ['v1', 'v2', 'v3', 'v4', 'v4', '']
        ... })
        >>> eav_to_df(test_eav_df)
        predicate subject        p1    p2    p3
        0               a  [v1, v2]  None  None
        1               b  [v3, v4]    v4  None
        2               c      None  None

    Args:
        eav_df:
        value_column:

    Returns:

    """
    # For predicates that have multiple values per subject,
    # aggregate them into lists
    unmasked_df = (eav_df.groupby(['subject', 'predicate'])[value_column]
                   .agg(list)
                   .unstack(fill_value=[])
                   .reset_index())

    # If we know some predicates should be single-valued,
    # we can unwrap them from lists
    single_value_mask = unmasked_df.apply(lambda x: x.map(len) <= 1)
    df = unmasked_df.mask(single_value_mask, unmasked_df.apply(lambda x: x.map(lambda y: y[0] if y else None)))

    return df

def db_to_dataframe(session: Session, prefix = "CHEBI") -> pd.DataFrame:
    """
    Convert a semsql database to a DataFrame

    Args:
        session:
        prefix:

    Returns:

    """
    def _filter(q: Select, tbl=Statements) -> Select:
        if prefix:
            q = q.where(tbl.subject.startswith(prefix))
        else:
            q = q.where(not_(tbl.subject.startswith("_:")))
        return q
    # Data triples
    q = select(Statements.subject,
                  Statements.predicate,
                  Statements.value).where(Statements.value != None)
    q = _filter(q)
    triples = pd.DataFrame(session.execute(q).all())
    v_df = eav_to_df(triples)
    # Object triples
    q = select(Statements.subject,
               Statements.predicate,
               Statements.object).where(Statements.object != None)
    q = q.where(not_(Statements.predicate == RDFS_SUBCLASS_OF))
    q = _filter(q)
    triples = pd.DataFrame(session.execute(q).all())
    o_df = eav_to_df(triples, value_column="object")
    # Edge triples
    q = select(Edge.subject,
               Edge.predicate,
               Edge.object).where(not_(Edge.object.startswith("_:")))
    q = _filter(q, Edge)
    triples = pd.DataFrame(session.execute(q).all())
    e_df = eav_to_df(triples, value_column="object")
    # Ancestor triples
    q = select(EntailedEdge.subject,
               EntailedEdge.object).where(EntailedEdge.predicate == RDFS_SUBCLASS_OF)
    q = q.where(not_(EntailedEdge.object.startswith("_:")))
    q = _filter(q, EntailedEdge)
    triples = pd.DataFrame(session.execute(q).all())
    triples['predicate'] = "entailed_subclass_of"
    a_df = eav_to_df(triples, value_column="object")
    df = v_df.merge(o_df, on='subject', how='outer').merge(e_df, on='subject', how='outer').merge(a_df, on='subject',
                                                                                                  how='outer')
    return df


def get_ontology_version(session: Session):
    q = select(Statements.object).where(Statements.predicate == OWL_VERSION_IRI)
    versions = session.execute(q).all()
    if len(versions) != 1:
        raise ValueError(f"Expected one version, got {len(versions)}")
    v = versions[0][0]
    # include ontology
    ont = "chebi"
    if "chemessence" in v:
        ont = "chemessence"
    return ont + v.split("/")[-2]

def create_benchmark(df: pd.DataFrame, session: Session, min_members=50, max_members=5000) -> Dataset:
    v = get_ontology_version(session)
    structure_df = df[df[SMILES].notnull()]
    defined_df = df[df[HAS_DEFINITION_CURIE].notnull()]
    cc_map = {}
    for _, row in defined_df.iterrows():
        parents = row[RDFS_SUBCLASS_OF]
        if parents and not isinstance(parents, list):
            if isinstance(parents, str):
                parents = [parents]
            else:
                parents = []
        cc = ChemicalClass(id=row["subject"], name=row[RDFS_LABEL], definition=row[HAS_DEFINITION_CURIE],
                           parents=parents,
                           instances=[], negative_instances=[])
        cc_map[cc.id] = cc
    s_map = {}
    for _, row in structure_df.iterrows():
        smiles_str = row[SMILES]
        #smiles_str_sanitized = sanitize_smiles(smiles_str)
        #if smiles_str_sanitized != smiles_str:
        #    raise ValueError(f"Invalid SMILES string: {smiles_str} != {smiles_str_sanitized}")
        structure = ChemicalStructure(name=row[RDFS_LABEL], smiles=smiles_str)
        s_map[row[SMILES]] = structure
        for a in row["entailed_subclass_of"]:
            if a == row["subject"]:
                continue
            if a in cc_map:
                cc = cc_map[a]
                cc.instances.append(structure)
                if len(cc.instances) > max_members:
                    del cc_map[a]
    ccs = [v for v in cc_map.values() if len(v.instances) >= min_members]
    if False:
        # TODO: calculate negatives later as we want to include all
        for cc in ccs:
            negative_smiles = []
            positive_smiles = [s.smiles for s in cc.instances]
            num_positive = len(positive_smiles)
            negative_candidates = list(set(s_map.keys()).difference(positive_smiles))
            parents = cc.parents
            for p in parents:
                if p in cc_map:
                    for i in cc_map[p].instances:
                        s = i.smiles
                        if s not in positive_smiles:
                            negative_smiles.append(s)
            negative_smiles = negative_smiles[:num_positive]
            if len(negative_smiles) < num_positive:
                import random
                random.shuffle(negative_candidates)
                negative_smiles.extend(negative_candidates[:num_positive - len(negative_smiles)])
            cc.negative_instances = [s_map[s] for s in negative_smiles]
    return Dataset(
        ontology_version=v,
        min_members=min_members,
        max_members=max_members,
        classes=ccs,
        structures=list(s_map.values()),
    )

def validate_dataset(dataset: Dataset) -> Iterator[Tuple[ChemicalStructure, str]]:
    """
    Validate a dataset

    Args:
        dataset:

    Returns:

    """
    for s in dataset.structures:
        smiles_str = s.smiles
        smiles_str_sanitized = sanitize_smiles(smiles_str)
        if smiles_str_sanitized != smiles_str:
            yield s, smiles_str_sanitized
        _mol = Chem.MolFromSmiles(smiles_str)

def create_and_save_benchmark(*args, **kwargs) -> Dataset:
    benchmark = create_benchmark(*args, **kwargs)
    benchmarks_dir = Path("inputs")
    benchmarks_dir.mkdir(exist_ok=True)
    path = f"{benchmarks_dir / benchmark.name}.json"
    with open(path, "w") as f:
        f.write(benchmark.model_dump_json(indent=2))
    return benchmark






