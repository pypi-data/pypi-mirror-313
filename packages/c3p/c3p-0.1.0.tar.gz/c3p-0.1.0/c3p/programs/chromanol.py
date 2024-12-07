"""
Classifies: CHEBI:23229 chromanol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_chromanol(smiles: str):
    """
    Determines if a molecule is a chromanol (chromane with one or more hydroxy groups).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a chromanol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # First check if molecule contains chromane core structure
    # SMARTS pattern for chromane: O1CCCc2ccccc12
    chromane_pattern = Chem.MolFromSmarts('O1CCCc2ccccc12')
    if not mol.HasSubstructMatch(chromane_pattern):
        return False, "No chromane core structure found"
    
    # Check for presence of hydroxyl groups
    # SMARTS pattern for hydroxyl group: [OH]
    hydroxyl_pattern = Chem.MolFromSmarts('[OH]')
    hydroxy_matches = mol.GetSubstructMatches(hydroxyl_pattern)
    
    if not hydroxy_matches:
        return False, "No hydroxyl groups found"
        
    # Get number of hydroxyl groups
    num_hydroxy = len(hydroxy_matches)
    
    # Check if hydroxyl groups are attached to the chromane core
    chromane_matches = mol.GetSubstructMatches(chromane_pattern)
    chromane_atoms = set()
    for match in chromane_matches:
        chromane_atoms.update(match)
        
    hydroxy_on_core = False
    for hydroxy_match in hydroxy_matches:
        # Get atom the OH is attached to
        oh_atom = mol.GetAtomWithIdx(hydroxy_match[0])
        for neighbor in oh_atom.GetNeighbors():
            if neighbor.GetIdx() in chromane_atoms:
                hydroxy_on_core = True
                break
                
    if not hydroxy_on_core:
        return False, "No hydroxyl groups attached to chromane core"
        
    position_desc = "chromanol with {} hydroxyl group{}".format(
        num_hydroxy, 's' if num_hydroxy > 1 else '')
        
    return True, position_desc


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23229',
                          'name': 'chromanol',
                          'definition': 'Any member of the class of chromanes '
                                        'that is chromane substituted by one '
                                        'or more hydroxy groups.',
                          'parents': ['CHEBI:23230', 'CHEBI:33822']},
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
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 8553,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 1.0,
    'f1': 0.07407407407407407,
    'accuracy': 0.9884486542682223}