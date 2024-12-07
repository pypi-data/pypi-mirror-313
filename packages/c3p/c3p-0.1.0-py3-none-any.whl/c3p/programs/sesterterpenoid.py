"""
Classifies: CHEBI:26660 sesterterpenoid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_sesterterpenoid(smiles: str):
    """
    Determines if a molecule is a sesterterpenoid (C25 terpenoid).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a sesterterpenoid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Count number of carbons
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    
    # Sesterterpenoids typically have 25 carbons, but can have fewer due to modifications
    # Allow range of 20-25 carbons to account for modifications/rearrangements
    if num_carbons < 20 or num_carbons > 25:
        return False, f"Carbon count ({num_carbons}) outside typical range for sesterterpenoids (20-25)"

    # Check for typical terpenoid features:
    # - Multiple rings
    # - Presence of methyl groups
    # - Presence of oxygen-containing groups
    
    ring_info = mol.GetRingInfo()
    if ring_info.NumRings() < 1:
        return False, "No rings found - sesterterpenoids typically contain ring systems"

    # Count methyl groups
    methyl_pattern = Chem.MolFromSmarts('[CH3]')
    methyl_matches = mol.GetSubstructMatches(methyl_pattern)
    if len(methyl_matches) < 2:
        return False, "Too few methyl groups for a sesterterpenoid"

    # Check for oxygen-containing functional groups
    o_pattern = Chem.MolFromSmarts('[O]')
    o_matches = mol.GetSubstructMatches(o_pattern)
    
    if len(o_matches) == 0:
        return False, "No oxygen-containing groups found - unusual for sesterterpenoids"

    # If we've made it here, likely a sesterterpenoid
    return True, f"Matches sesterterpenoid pattern with {num_carbons} carbons, {len(methyl_matches)} methyl groups, {ring_info.NumRings()} rings"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26660',
                          'name': 'sesterterpenoid',
                          'definition': 'Any terpenoid derived from a '
                                        'sesterterpene. The term includes '
                                        'compounds in which the C25 skeleton '
                                        'of the parent sesterterpene has been '
                                        'rearranged or modified by the removal '
                                        'of one or more skeletal atoms '
                                        '(generally methyl groups). Sometimes '
                                        'sesterterpenoids are erroneously '
                                        'referred to as sesterpenoids.',
                          'parents': ['CHEBI:26873']},
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
    'num_true_positives': 14,
    'num_false_positives': 100,
    'num_true_negatives': 783,
    'num_false_negatives': 19,
    'num_negatives': None,
    'precision': 0.12280701754385964,
    'recall': 0.42424242424242425,
    'f1': 0.19047619047619047,
    'accuracy': 0.8700873362445415}