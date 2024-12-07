"""
Classifies: CHEBI:23990 ethyl ester
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_ethyl_ester(smiles: str):
    """
    Determines if a molecule contains an ethyl ester group.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains ethyl ester, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for ethyl ester: C-C-O-C(=O)-
    ethyl_ester_pattern = Chem.MolFromSmarts('CCO[C;H0](=O)')
    
    if mol.HasSubstructMatch(ethyl_ester_pattern):
        # Find all matches
        matches = mol.GetSubstructMatches(ethyl_ester_pattern)
        
        # Count number of ethyl ester groups
        num_matches = len(matches)
        
        if num_matches == 1:
            return True, "Contains 1 ethyl ester group"
        else:
            return True, f"Contains {num_matches} ethyl ester groups"
            
    return False, "No ethyl ester group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23990',
                          'name': 'ethyl ester',
                          'definition': 'Any carboxylic ester resulting from '
                                        'the formal condensation of the '
                                        'carboxy group of a carboxylic acid '
                                        'with ethanol.',
                          'parents': ['CHEBI:33308']},
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
    'num_true_positives': 20,
    'num_false_positives': 100,
    'num_true_negatives': 591,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.16666666666666666,
    'recall': 1.0,
    'f1': 0.2857142857142857,
    'accuracy': 0.8593530239099859}