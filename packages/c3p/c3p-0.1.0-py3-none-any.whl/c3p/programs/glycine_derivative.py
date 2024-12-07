"""
Classifies: CHEBI:24373 glycine derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_glycine_derivative(smiles: str):
    """
    Determines if a molecule is a glycine derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glycine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Look for glycine substructure patterns
    patterns = [
        ("[NX3;H2,H1;!$(NC=O)][CH2]C(=O)[OH]", "unmodified glycine"),
        ("[NX3;H1;$(NC=O)][CH2]C(=O)[OH]", "N-acylated glycine"),
        ("[NX3;H2,H1][CH2]C(=O)[O;!$(OH)]", "glycine ester"),
        ("[NX3;H2,H1][CH2]C(=O)[NX3]", "glycine amide"),
        ("[NX3;H0,H1][CH2]C(=O)[OH]", "N-substituted glycine"),
        ("[NX3;H2,H1][CH2]C(=O)[!OH]", "modified carboxy glycine"),
        ("[NX3][CH][C](=O)[OH]", "alpha-substituted glycine")
    ]

    for pattern, reason in patterns:
        patt = Chem.MolFromSmarts(pattern)
        if patt is not None and mol.HasSubstructMatch(patt):
            return True, f"Contains {reason}"

    return False, "No glycine-like substructure found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24373',
                          'name': 'glycine derivative',
                          'definition': 'A proteinogenic amino acid derivative '
                                        'resulting from reaction of glycine at '
                                        'the amino group or the carboxy group, '
                                        'or from the replacement of any '
                                        'hydrogen of glycine by a heteroatom.',
                          'parents': ['CHEBI:83811']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Python argument types in\n'
               '    Mol.HasSubstructMatch(Mol, NoneType)\n'
               'did not match C++ signature:\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle '
               'query, RDKit::SubstructMatchParameters params=True)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
               'RDKit::SubstructMatchParameters params)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle '
               'query, bool recursionPossible=True, bool useChirality=False, '
               'bool useQueryQueryMatches=False)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
               'bool recursionPossible=True, bool useChirality=False, bool '
               'useQueryQueryMatches=False)',
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 24,
    'num_false_positives': 100,
    'num_true_negatives': 981,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.1935483870967742,
    'recall': 0.8571428571428571,
    'f1': 0.3157894736842105,
    'accuracy': 0.9062218214607755}