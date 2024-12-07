"""
Classifies: CHEBI:25240 methoxyflavanone
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMolFrags

def is_methoxyflavanone(smiles: str):
    """
    Determines if a molecule is a methoxyflavanone (flavanone with methoxy substituents).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a methoxyflavanone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for flavanone core structure using SMARTS pattern
    # Matches the basic flavanone skeleton with O1-C-C-C(=O)-c2c-c-c-c-c2-1
    flavanone_pattern = Chem.MolFromSmarts('O1-C-C-C(=O)-c2c-c-c-c-c2-1')
    if not mol.HasSubstructMatch(flavanone_pattern):
        return False, "No flavanone core structure found"

    # Check for methoxy groups (-OCH3)
    methoxy_pattern = Chem.MolFromSmarts('OC')
    methoxy_matches = mol.GetSubstructMatches(methoxy_pattern)
    
    if not methoxy_matches:
        return False, "No methoxy groups found"

    # Verify methoxy groups by checking that the carbon is actually CH3
    valid_methoxy = 0
    for match in methoxy_matches:
        o_atom = mol.GetAtomWithIdx(match[0])
        c_atom = mol.GetAtomWithIdx(match[1])
        
        # Check if carbon has exactly 3 hydrogens (i.e., is CH3)
        if c_atom.GetTotalNumHs() == 3:
            valid_methoxy += 1

    if valid_methoxy == 0:
        return False, "No valid methoxy groups found"

    return True, f"Methoxyflavanone with {valid_methoxy} methoxy group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25240',
                          'name': 'methoxyflavanone',
                          'definition': 'A member of the class of flavanones '
                                        'that consists of flavanone with one '
                                        'or more methoxy substituents.',
                          'parents': ['CHEBI:28863', 'CHEBI:35618']},
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
    'num_false_positives': 0,
    'num_true_negatives': 183869,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999673691366417}