"""
Classifies: CHEBI:26658 sesquiterpenoid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_sesquiterpenoid(smiles: str):
    """
    Determines if a molecule is a sesquiterpenoid based on:
    - Having a C15 skeleton (or slightly modified)
    - Being derived from a sesquiterpene
    - Having rearrangements/modifications of the skeleton
    
    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a sesquiterpenoid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count carbons
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    
    # Basic sesquiterpenoid should have around 15 carbons (allowing some modifications)
    if num_carbons < 12 or num_carbons > 18:
        return False, f"Carbon count ({num_carbons}) outside typical range for sesquiterpenoids (12-18)"

    # Check for presence of rings
    ring_info = mol.GetRingInfo()
    if not ring_info.NumRings():
        return False, "No rings found - sesquiterpenoids typically have ring structures"

    # Look for typical functional groups found in sesquiterpenoids
    has_oxygen = any(atom.GetSymbol() == 'O' for atom in mol.GetAtoms())
    
    # Calculate molecular weight
    mol_weight = Descriptors.ExactMolWt(mol)
    if mol_weight < 200 or mol_weight > 400:
        return False, f"Molecular weight ({mol_weight:.1f}) outside typical range for sesquiterpenoids"

    # Check for presence of typical sesquiterpenoid substructures
    sesquiterpene_patterns = [
        "[C]1[C][C][C]2[C][C][C][C][C]2[C]1", # Decalin skeleton
        "[C]1[C][C][C]2[C][C][C][C]2[C]1",    # Bicyclic skeleton
        "[C]1[C][C][C][C][C]1",                # 6-membered ring
        "[C]1[C][C][C][C]1"                    # 5-membered ring
    ]
    
    matches_pattern = False
    for pattern in sesquiterpene_patterns:
        if mol.HasSubstructMatch(Chem.MolFromSmarts(pattern)):
            matches_pattern = True
            break
            
    if not matches_pattern:
        return False, "Does not match typical sesquiterpenoid structural patterns"

    # If we get here, molecule has characteristics consistent with sesquiterpenoids
    features = []
    if has_oxygen:
        features.append("oxygenated")
    if ring_info.NumRings() > 1:
        features.append("polycyclic")
        
    return True, f"Matches sesquiterpenoid characteristics: {', '.join(features)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26658',
                          'name': 'sesquiterpenoid',
                          'definition': 'Any terpenoid derived from a '
                                        'sesquiterpene. The term includes '
                                        'compounds in which the C15 skeleton '
                                        'of the parent sesquiterpene has been '
                                        'rearranged or modified by the removal '
                                        'of one or more skeletal atoms '
                                        '(generally methyl groups).',
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
    'num_true_positives': 64,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 100,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 0.3902439024390244,
    'f1': 0.5614035087719299,
    'accuracy': 0.3902439024390244}