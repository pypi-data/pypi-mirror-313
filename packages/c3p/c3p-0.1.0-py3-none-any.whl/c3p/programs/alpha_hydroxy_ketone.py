"""
Classifies: CHEBI:139588 alpha-hydroxy ketone
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_alpha_hydroxy_ketone(smiles: str):
    """
    Determines if a molecule contains an alpha-hydroxy ketone group.
    An alpha-hydroxy ketone has a hydroxy group adjacent to a ketone.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains alpha-hydroxy ketone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for alpha-hydroxy ketone
    # [OH1] matches hydroxyl group
    # [CH,CH2] matches carbon with 1 or 2 hydrogens
    # C(=O) matches ketone carbonyl
    pattern = Chem.MolFromSmarts('[OH1]-[CH,CH2]-C(=O)')
    
    # Alternative pattern for alpha-hydroxy ketone where carbon has other substituents
    pattern2 = Chem.MolFromSmarts('[OH1]-[C]-C(=O)')

    matches = mol.GetSubstructMatches(pattern)
    matches2 = mol.GetSubstructMatches(pattern2)
    
    all_matches = matches + matches2
    
    if len(all_matches) > 0:
        return True, f"Contains {len(all_matches)} alpha-hydroxy ketone group(s)"
    else:
        return False, "No alpha-hydroxy ketone group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139588',
                          'name': 'alpha-hydroxy ketone',
                          'definition': 'An alpha-oxyketone that has a hydroxy '
                                        'group as the alpha-oxy moiety.',
                          'parents': ['CHEBI:30879', 'CHEBI:52396']},
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
    'num_true_positives': 50,
    'num_false_positives': 100,
    'num_true_negatives': 1210,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.3333333333333333,
    'recall': 0.9803921568627451,
    'f1': 0.4975124378109452,
    'accuracy': 0.925789860396767}