"""
Classifies: CHEBI:19168 17-oxo steroid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_17_oxo_steroid(smiles: str):
    """
    Determines if a molecule is a 17-oxo steroid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 17-oxo steroid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for steroid core (4 fused rings)
    ri = mol.GetRingInfo()
    if len(ri.AtomRings()) < 4:
        return False, "Does not contain minimum 4 rings required for steroid core"
    
    # Get SMARTS pattern for steroid core with C17 ketone
    # Pattern matches 4 fused rings with C=O at position 17
    steroid_pattern = Chem.MolFromSmarts('[#6]~1~[#6]~[#6]~[#6]~2~[#6]~[#6]~[#6]~[#6]~3~[#6]~[#6]~[#6]~4~[#6](=O)~[#6]~[#6]~[#6]~4~[#6]~3~[#6]~2~1')
    
    if mol.HasSubstructMatch(steroid_pattern):
        # Find the C=O group at position 17
        matches = mol.GetSubstructMatches(steroid_pattern)
        
        if len(matches) > 0:
            return True, "Contains steroid core with C=O at position 17"
            
    return False, "Does not match 17-oxo steroid pattern"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:19168',
                          'name': '17-oxo steroid',
                          'definition': 'Any  oxo steroid carrying the oxo '
                                        'group at position 17.',
                          'parents': ['CHEBI:35789', 'CHEBI:3992']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
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
    'num_false_positives': 0,
    'num_true_negatives': 183860,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999619290030294}