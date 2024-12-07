"""
Classifies: CHEBI:145217 epoxy steroid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_epoxy_steroid(smiles: str):
    """
    Determines if a molecule is an epoxy steroid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an epoxy steroid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Look for epoxy group
    epoxy_pattern = Chem.MolFromSmarts('[C,c]1O[C,c]1')
    has_epoxy = len(mol.GetSubstructMatches(epoxy_pattern)) > 0
    
    if not has_epoxy:
        return False, "No epoxy group found"
        
    # Check for steroid core using SMARTS patterns
    # Pattern for steroid skeleton with flexible ring sizes
    steroid_pattern = Chem.MolFromSmarts('[CH2,CH]1[CH2,CH][CH2,CH][C,c]2[CH2,CH][CH2,CH][C,c]3[C,c]4[CH2,CH][CH2,CH][CH2,CH][C,c]4[CH2,CH][CH2,CH][C,c]3[C,c]2[CH2,CH]1')
    
    if not mol.HasSubstructMatch(steroid_pattern):
        return False, "Does not contain steroid core structure"
        
    # Check number of rings
    ring_info = mol.GetRingInfo()
    if len(ring_info.AtomRings()) < 4:
        return False, "Does not have minimum number of rings for steroid structure"
        
    # If we get here, molecule has both steroid core and epoxy group
    n_epoxy = len(mol.GetSubstructMatches(epoxy_pattern))
    return True, f"Contains steroid core structure and {n_epoxy} epoxy group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:145217',
                          'name': 'epoxy steroid',
                          'definition': 'Any steroid whose structure includes '
                                        'an epoxy group.',
                          'parents': ['CHEBI:32955', 'CHEBI:35341']},
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
    'num_true_positives': 1,
    'num_false_positives': 17,
    'num_true_negatives': 183873,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.05555555555555555,
    'recall': 0.25,
    'f1': 0.0909090909090909,
    'accuracy': 0.9998912416935843}