"""
Classifies: CHEBI:20706 6-aminopurines
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_6_aminopurines(smiles: str):
    """
    Determines if a molecule contains 6-aminopurine (adenine) as part of its structure.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains 6-aminopurine, False otherwise
        str: Reason for classification
    """
    # Check for valid SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # SMARTS pattern for 6-aminopurine (adenine) core structure
    # Matches fused 5-6 ring system with nitrogen at position 6
    adenine_pattern = Chem.MolFromSmarts('c1nc(N)nc2[nH]cnc12')
    
    if mol.HasSubstructMatch(adenine_pattern):
        return True, "Contains 6-aminopurine (adenine) core structure"
    
    return False, "Does not contain 6-aminopurine structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:20706',
                          'name': '6-aminopurines',
                          'definition': 'Any compound having 6-aminopurine '
                                        '(adenine) as part of its structure.',
                          'parents': ['CHEBI:22527']},
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
    'num_true_positives': 0,
    'num_false_positives': 17,
    'num_true_negatives': 183076,
    'num_false_negatives': 84,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9994486207329523}