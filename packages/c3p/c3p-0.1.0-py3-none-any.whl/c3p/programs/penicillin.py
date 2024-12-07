"""
Classifies: CHEBI:17334 penicillin
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_penicillin(smiles: str):
    """
    Determines if a molecule is a penicillin - containing the penam core structure with
    specific substituents at positions 2, 3 and 6.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a penicillin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for penam core with required substituents:
    # - Two methyl groups at position 2
    # - Carboxylate at position 3  
    # - Carboxamide at position 6
    penam_pattern = "[H][C@]12SC(C)(C)[C@@H](N1C(=O)[C@H]2NC(=O)[*])[C,c]([O,N,S])[!#1]"
    
    pattern_mol = Chem.MolFromSmarts(penam_pattern)
    if pattern_mol is None:
        return None, "Invalid SMARTS pattern"

    # Check if structure matches penam pattern
    matches = mol.GetSubstructMatches(pattern_mol)
    if not matches:
        return False, "Does not contain penam core structure with required substituents"

    # Additional checks could be added here for specific substituent patterns
    
    return True, "Contains penam core with required substituents at positions 2, 3 and 6"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17334',
                          'name': 'penicillin',
                          'definition': 'Any member of the group of '
                                        'substituted penams containing two '
                                        'methyl substituents at position 2, a '
                                        'carboxylate substituent at position 3 '
                                        'and a carboxamido group at position '
                                        '6.',
                          'parents': ['CHEBI:25865']},
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
    'num_true_negatives': 183873,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999673698464752}