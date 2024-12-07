"""
Classifies: CHEBI:24271 glucosamines
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect
from rdkit.Chem import rdDecomposition

def is_glucosamines(smiles: str):
    """
    Determines if a molecule is a glucosamine derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glucosamine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of basic pyranose ring
    matches = mol.GetSubstructMatches(Chem.MolFromSmarts('[C]-1-[C]-[C]-[C]-[C]-[C]-O-1'))
    if not matches:
        return False, "No pyranose ring found"

    # Check for amino group
    amino_matches = mol.GetSubstructMatches(Chem.MolFromSmarts('[NH2,NH][C]'))
    if not amino_matches:
        return False, "No amino group found"
        
    # Check for correct number of OH groups (typically 3-4 in glucosamines)
    oh_matches = len(mol.GetSubstructMatches(Chem.MolFromSmarts('[OH]')))
    if oh_matches < 2:
        return False, "Insufficient hydroxyl groups for glucosamine"

    # Check for primary alcohol (CH2OH) group
    ch2oh_matches = mol.GetSubstructMatches(Chem.MolFromSmarts('[CH2][OH]'))
    if not ch2oh_matches:
        return False, "No CH2OH group found"

    # Check stereochemistry if defined
    chiral_centers = Chem.FindMolChiralCenters(mol)
    if len(chiral_centers) < 4:
        return True, "Glucosamine derivative (stereochemistry not fully defined)"

    # For fully defined stereochemistry, we could add more specific checks here
    # but this would require handling multiple possible representations
    
    return True, "Glucosamine derivative"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24271',
                          'name': 'glucosamines',
                          'definition': 'Any  hexosamine that is glucose in '
                                        'which at least one of the hydroxy '
                                        'groups has been replaced by an amino '
                                        'group.',
                          'parents': ['CHEBI:24586']},
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
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}