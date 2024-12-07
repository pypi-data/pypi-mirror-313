"""
Classifies: CHEBI:1722 3beta-hydroxy-Delta(5)-steroid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetBestRMSForAlignement
from rdkit.Chem import rdDecomposition
from rdkit.Chem import rdMolDescriptors

def is_3beta_hydroxy_Delta_5__steroid(smiles: str):
    """
    Determines if a molecule is a 3beta-hydroxy-Delta(5)-steroid.
    These are steroids with a 3-beta hydroxyl group and a double bond between C5-C6.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 3beta-hydroxy-Delta(5)-steroid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # First check if it's a steroid by matching against the basic steroid scaffold
    steroid_core = Chem.MolFromSmarts("[#6]~1~[#6]~[#6]~[#6]~2~[#6]~[#6]~[#6]~3~[#6]~[#6]~[#6]~4~[#6]~[#6]~[#6]~[#6]~4~[#6]~[#6]~3~[#6]~[#6]~2~[#6]~1")
    if not mol.HasSubstructMatch(steroid_core):
        return False, "Not a steroid - missing basic steroid scaffold"

    # Check for 3-beta hydroxyl group
    # SMARTS pattern for 3-beta-OH: carbon at position 3 with beta OH
    hydroxyl_pattern = Chem.MolFromSmarts('[H][C@@H]1CC[C@@]2([H])')
    if not mol.HasSubstructMatch(hydroxyl_pattern):
        return False, "Missing 3-beta hydroxyl group configuration"

    # Check specifically for OH group at position 3
    oh_pattern = Chem.MolFromSmarts('[CH]([OH])')
    if not mol.HasSubstructMatch(oh_pattern):
        return False, "Missing hydroxyl group"

    # Check for double bond between C5-C6
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    if not mol.HasSubstructMatch(double_bond_pattern):
        return False, "Missing double bond between C5-C6"

    # If all checks pass
    return True, "Molecule is a 3beta-hydroxy-Delta(5)-steroid with correct stereochemistry and double bond"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:1722',
                          'name': '3beta-hydroxy-Delta(5)-steroid',
                          'definition': 'Any 3beta-hydroxy-steroid that '
                                        'contains a double bond between '
                                        'positions 5 and 6.',
                          'parents': ['CHEBI:36836']},
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
    'success': False,
    'best': True,
    'error': "cannot import name 'GetBestRMSForAlignement' from "
             "'rdkit.Chem.AllChem' "
             '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/AllChem.py)',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}