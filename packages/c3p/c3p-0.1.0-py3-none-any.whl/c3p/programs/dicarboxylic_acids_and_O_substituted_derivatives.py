"""
Classifies: CHEBI:131927 dicarboxylic acids and O-substituted derivatives
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_dicarboxylic_acids_and_O_substituted_derivatives(smiles: str):
    """
    Determines if a molecule is a dicarboxylic acid or O-substituted derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a dicarboxylic acid or derivative, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all carboxylic acid and ester groups
    carboxyl_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    ester_pattern = Chem.MolFromSmarts('C(=O)O[C,H]')
    
    carboxyl_matches = mol.GetSubstructMatches(carboxyl_pattern)
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    
    # Count total number of carboxyl/ester groups
    total_carboxyl = len(carboxyl_matches) + len(ester_matches)
    
    if total_carboxyl < 2:
        return False, "Does not contain at least 2 carboxyl/ester groups"
        
    # Check if carboxyl/ester groups are on different carbons
    carboxyl_carbons = set()
    for match in carboxyl_matches:
        carboxyl_carbons.add(match[0])
    for match in ester_matches:
        carboxyl_carbons.add(match[0])
        
    if len(carboxyl_carbons) < 2:
        return False, "Carboxyl/ester groups are on same carbon"
        
    # Success - classify based on type
    if len(carboxyl_matches) == 2:
        return True, "Dicarboxylic acid"
    elif len(ester_matches) == 2:
        return True, "Diester derivative"
    else:
        return True, "Mixed carboxylic acid/ester derivative"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131927',
                          'name': 'dicarboxylic acids and O-substituted '
                                  'derivatives',
                          'definition': 'A class of carbonyl compound '
                                        'encompassing dicarboxylic acids and '
                                        'any derivatives obtained by '
                                        'substitution of either one or both of '
                                        'the carboxy hydrogens.',
                          'parents': ['CHEBI:36586']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: cannot import name 'rdDecomposition' from "
               "'rdkit.Chem' "
               '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 90,
    'num_false_positives': 100,
    'num_true_negatives': 706,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.47368421052631576,
    'recall': 0.989010989010989,
    'f1': 0.6405693950177936,
    'accuracy': 0.887402452619844}