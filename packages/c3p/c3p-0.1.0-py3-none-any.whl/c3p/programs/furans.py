"""
Classifies: CHEBI:24129 furans
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_furans(smiles: str):
    """
    Determines if a molecule contains at least one furan ring.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains a furan ring, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for presence of furan ring using SMARTS pattern
    # Furan pattern: 5-membered aromatic ring with O and 4 carbons
    furan_pattern = Chem.MolFromSmarts('o1cccc1')
    
    # Alternative pattern for non-aromatic furan rings
    nonaromatic_furan = Chem.MolFromSmarts('O1CCCC1')
    
    matches = mol.GetSubstructMatches(furan_pattern)
    nonaromatic_matches = mol.GetSubstructMatches(nonaromatic_furan)
    
    if len(matches) > 0:
        if len(matches) == 1:
            return True, "Contains 1 aromatic furan ring"
        else:
            return True, f"Contains {len(matches)} aromatic furan rings"
            
    if len(nonaromatic_matches) > 0:
        if len(nonaromatic_matches) == 1:
            return True, "Contains 1 non-aromatic furan ring"
        else:
            return True, f"Contains {len(nonaromatic_matches)} non-aromatic furan rings"
            
    return False, "No furan rings found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24129',
                          'name': 'furans',
                          'definition': 'Compounds containing at least one '
                                        'furan ring.',
                          'parents': ['CHEBI:25693', 'CHEBI:38104']},
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
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 48,
    'num_false_positives': 100,
    'num_true_negatives': 1145,
    'num_false_negatives': 49,
    'num_negatives': None,
    'precision': 0.32432432432432434,
    'recall': 0.4948453608247423,
    'f1': 0.39183673469387753,
    'accuracy': 0.8889716840536512}