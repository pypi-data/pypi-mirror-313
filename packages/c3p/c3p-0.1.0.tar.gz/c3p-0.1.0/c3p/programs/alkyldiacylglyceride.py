"""
Classifies: CHEBI:166986 alkyldiacylglyceride
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_alkyldiacylglyceride(smiles: str):
    """
    Determines if a molecule is an alkyldiacylglyceride - a triradylglycerol with 
    a single alkyl substituent and two acyl substituents.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an alkyldiacylglyceride, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for glycerol backbone
    glycerol_pattern = Chem.MolFromSmarts("[CH2]-[CH]-[CH2]")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "No glycerol backbone found"

    # Count O-substituents
    o_substituents = 0
    acyl_groups = 0
    alkyl_groups = 0

    # Patterns for substituents
    acyl_pattern = Chem.MolFromSmarts("O=C-O")  # For acyl groups
    alkyl_pattern = Chem.MolFromSmarts("CO")     # For alkyl groups (C-O single bond)

    # Find acyl groups
    acyl_matches = mol.GetSubstructMatches(acyl_pattern)
    acyl_groups = len(acyl_matches)

    # Find total O-substituents
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O':
            o_substituents += 1

    # Calculate alkyl groups (O atoms not part of acyl groups)
    alkyl_groups = o_substituents - (2 * acyl_groups)  # Each acyl group has 2 oxygens

    if acyl_groups == 2 and alkyl_groups == 1:
        return True, f"Alkyldiacylglyceride with {acyl_groups} acyl groups and {alkyl_groups} alkyl group"
    elif acyl_groups != 2:
        return False, f"Found {acyl_groups} acyl groups, requires exactly 2"
    elif alkyl_groups != 1:
        return False, f"Found {alkyl_groups} alkyl groups, requires exactly 1"
    else:
        return False, "Does not match alkyldiacylglyceride pattern"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:166986',
                          'name': 'alkyldiacylglyceride',
                          'definition': 'A triradylglycerol with a single '
                                        'alkyl substituent and two acyl '
                                        'substituents at unspecified '
                                        'positions.',
                          'parents': [   'CHEBI:24353',
                                         'CHEBI:33308',
                                         'CHEBI:47778',
                                         'CHEBI:64611',
                                         'CHEBI:76579']},
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
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 16717,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 0.5,
    'f1': 0.019417475728155338,
    'accuracy': 0.99399488673524}