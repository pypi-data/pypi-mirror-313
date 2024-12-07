"""
Classifies: CHEBI:25481 naphthoquinone
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdDecomposition

def is_naphthoquinone(smiles: str):
    """
    Determines if a molecule is a naphthoquinone.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a naphthoquinone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for naphthalene core
    naphthalene_pattern = Chem.MolFromSmarts('c1ccc2ccccc2c1')
    if not mol.HasSubstructMatch(naphthalene_pattern):
        return False, "No naphthalene core found"
    
    # Check for two ketone groups
    ketone_pattern = Chem.MolFromSmarts('C(=O)')
    ketone_matches = mol.GetSubstructMatches(ketone_pattern)
    if len(ketone_matches) < 2:
        return False, "Less than 2 ketone groups found"

    # Check specifically for 1,4-naphthoquinone pattern
    naphthoquinone_pattern = Chem.MolFromSmarts('O=C1C=CC(=O)c2ccccc21')
    naphthoquinone_pattern2 = Chem.MolFromSmarts('O=C1C(=O)c2ccccc2C=C1')
    
    if not (mol.HasSubstructMatch(naphthoquinone_pattern) or mol.HasSubstructMatch(naphthoquinone_pattern2)):
        # Check for other naphthoquinone patterns with substituents
        nq_pattern3 = Chem.MolFromSmarts('O=C1C(*)C(*)C(=O)c2ccccc21')
        nq_pattern4 = Chem.MolFromSmarts('O=C1C(*)=C(*)C(=O)c2ccccc21')
        if not (mol.HasSubstructMatch(nq_pattern3) or mol.HasSubstructMatch(nq_pattern4)):
            return False, "No naphthoquinone core structure found"

    # Get number of substituents
    substituents = []
    core_atoms = set()
    for match in mol.GetSubstructMatches(naphthalene_pattern):
        core_atoms.update(match)
    
    for atom in mol.GetAtoms():
        if atom.GetIdx() not in core_atoms and atom.GetSymbol() != 'H':
            substituents.append(atom.GetSymbol())

    return True, f"Naphthoquinone with {len(set(substituents))} types of substituents"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25481',
                          'name': 'naphthoquinone',
                          'definition': 'A polycyclic aromatic ketone '
                                        'metabolite of naphthalene.',
                          'parents': ['CHEBI:36141']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': None,
    'attempt': 0,
    'success': False,
    'best': True,
    'error': "cannot import name 'rdDecomposition' from 'rdkit.Chem' "
             '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}