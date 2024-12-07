"""
Classifies: CHEBI:24730 hydroxynitrile
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroxynitrile(smiles: str):
    """
    Determines if a molecule is a hydroxynitrile (contains both a nitrile group and a hydroxy group).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydroxynitrile, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for nitrile group (C#N)
    nitrile_pattern = Chem.MolFromSmarts('[C]#N')
    has_nitrile = mol.HasSubstructMatch(nitrile_pattern)

    # Check for hydroxy group (OH)
    hydroxy_pattern = Chem.MolFromSmarts('[OH]')
    has_hydroxy = mol.HasSubstructMatch(hydroxy_pattern)

    if has_nitrile and has_hydroxy:
        # Count occurrences
        nitrile_count = len(mol.GetSubstructMatches(nitrile_pattern))
        hydroxy_count = len(mol.GetSubstructMatches(hydroxy_pattern))
        
        return True, f"Contains {nitrile_count} nitrile group(s) and {hydroxy_count} hydroxy group(s)"
    elif not has_nitrile and not has_hydroxy:
        return False, "Missing both nitrile and hydroxy groups"
    elif not has_nitrile:
        return False, "Missing nitrile group"
    else:
        return False, "Missing hydroxy group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24730',
                          'name': 'hydroxynitrile',
                          'definition': 'Any nitrile compound which also '
                                        'contains a hydroxy group.',
                          'parents': ['CHEBI:18379']},
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
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 19083,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 1.0,
    'f1': 0.07407407407407407,
    'accuracy': 0.9947881378016366}