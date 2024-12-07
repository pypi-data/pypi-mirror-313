"""
Classifies: CHEBI:190712 epoxy monocarboxylic acid anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_epoxy_monocarboxylic_acid_anion(smiles: str):
    """
    Determines if a molecule is an epoxy monocarboxylic acid anion.
    Must contain exactly one carboxylate anion group and at least one epoxy group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an epoxy monocarboxylic acid anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylate anion group C(=O)[O-]
    carboxylate_pattern = Chem.MolFromSmarts('C(=O)[O-]')
    carboxylate_matches = mol.GetSubstructMatches(carboxylate_pattern)
    
    if len(carboxylate_matches) == 0:
        return False, "No carboxylate anion group found"
    elif len(carboxylate_matches) > 1:
        return False, "Multiple carboxylate anion groups found"

    # Check for epoxy group
    epoxy_pattern = Chem.MolFromSmarts('C1OC1')
    epoxy_matches = mol.GetSubstructMatches(epoxy_pattern)
    
    if len(epoxy_matches) == 0:
        return False, "No epoxy group found"
    
    num_epoxy = len(epoxy_matches)
    
    return True, f"Found 1 carboxylate anion group and {num_epoxy} epoxy group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:190712',
                          'name': 'epoxy monocarboxylic acid anion',
                          'definition': 'Any monocarboxylic acid anion '
                                        'containing at least one epoxy group.',
                          'parents': ['CHEBI:32955', 'CHEBI:35757']},
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
    'num_true_positives': 3,
    'num_false_positives': 88,
    'num_true_negatives': 183810,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.03296703296703297,
    'recall': 1.0,
    'f1': 0.06382978723404255,
    'accuracy': 0.9995214816667664}