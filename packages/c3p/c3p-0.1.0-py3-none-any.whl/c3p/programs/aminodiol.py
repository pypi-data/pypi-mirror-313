"""
Classifies: CHEBI:22501 aminodiol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_aminodiol(smiles: str):
    """
    Determines if a molecule is an aminodiol (contains one amino group and two hydroxy groups).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an aminodiol, False otherwise
        str: Reason for classification
    """
    # Create RDKit molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Count number of OH groups
    oh_pattern = Chem.MolFromSmarts('[OH]')
    oh_matches = mol.GetSubstructMatches(oh_pattern)
    num_oh = len(oh_matches)
    
    # Count number of NH2/NH groups 
    nh2_pattern = Chem.MolFromSmarts('[NH2]')
    nh_pattern = Chem.MolFromSmarts('[NH]')
    
    nh2_matches = mol.GetSubstructMatches(nh2_pattern)
    nh_matches = mol.GetSubstructMatches(nh_pattern)
    num_nh = len(nh2_matches) + len(nh_matches)

    if num_oh < 2:
        return False, f"Only {num_oh} hydroxy groups found, needs 2"
        
    if num_nh < 1:
        return False, "No amino groups found"
        
    if num_oh == 2 and num_nh >= 1:
        return True, f"Contains {num_oh} hydroxy groups and {num_nh} amino groups"
        
    return False, f"Contains {num_oh} hydroxy groups and {num_nh} amino groups - not matching aminodiol pattern"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22501',
                          'name': 'aminodiol',
                          'definition': 'An amino alcohol having two hydroxy '
                                        'functional groups.',
                          'parents': ['CHEBI:22478', 'CHEBI:23824']},
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
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 1407,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.9337748344370861}