"""
Classifies: CHEBI:16366 anthocyanidin cation
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_anthocyanidin_cation(smiles: str):
    """
    Determines if a molecule is an anthocyanidin cation.
    
    Args:
        smiles (str): SMILES string of the molecule
    
    Returns:
        bool: True if molecule is an anthocyanidin cation, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for presence of O+ (oxonium ion)
    has_oxonium = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == 1:
            has_oxonium = True
            break
            
    if not has_oxonium:
        return False, "Missing oxonium ion (O+)"

    # Check for flavylium core structure
    flavylium_pattern = Chem.MolFromSmarts('[O+]=C1C=CC2=CC=CC=C2O1')
    if not mol.HasSubstructMatch(flavylium_pattern):
        return False, "Missing flavylium core structure"
        
    # Check for phenyl substituent at position 2
    phenyl_pattern = Chem.MolFromSmarts('[O+]=C1C=CC2=CC=CC=C2O1-[c]1[c][c][c][c][c]1')
    if not mol.HasSubstructMatch(phenyl_pattern):
        return False, "Missing phenyl substituent at position 2"
        
    # Check for at least one hydroxyl group
    oh_pattern = Chem.MolFromSmarts('O[H]')
    if not mol.HasSubstructMatch(oh_pattern):
        return False, "Missing hydroxyl group(s)"

    return True, "Contains flavylium core with phenyl substituent and hydroxyl group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16366',
                          'name': 'anthocyanidin cation',
                          'definition': 'Any organic cation that is an aglycon '
                                        'of anthocyanin cation; they are '
                                        'oxygenated derivatives of flavylium '
                                        '(2-phenylchromenylium).',
                          'parents': ['CHEBI:25697', 'CHEBI:47916']},
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
    'num_true_negatives': 183754,
    'num_false_negatives': 18,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.999902052543369}