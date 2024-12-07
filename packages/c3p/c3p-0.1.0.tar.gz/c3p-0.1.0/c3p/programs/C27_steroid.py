"""
Classifies: CHEBI:131619 C27-steroid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprint
from rdkit.Chem import rdMolDescriptors

def is_C27_steroid(smiles: str):
    """
    Determines if a molecule is a C27 steroid (based on cholestane skeleton).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a C27 steroid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check carbon count
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count != 27:
        return False, f"Carbon count is {carbon_count}, not 27"
        
    # Check for basic steroid ring system (4 fused rings)
    ring_info = mol.GetRingInfo()
    if not ring_info.NumRings() >= 4:
        return False, "Does not contain minimum 4 rings required for steroid skeleton"
        
    # Get all rings of size 6 (should have 3) and size 5 (should have 1)
    rings_6 = []
    rings_5 = []
    for ring in ring_info.AtomRings():
        if len(ring) == 6:
            rings_6.append(ring)
        elif len(ring) == 5:
            rings_5.append(ring)
            
    if len(rings_6) < 3:
        return False, f"Does not contain 3 six-membered rings (found {len(rings_6)})"
    if len(rings_5) < 1:
        return False, f"Does not contain 1 five-membered ring (found {len(rings_5)})"
        
    # Check for fused ring system by verifying shared atoms between rings
    all_rings = rings_6 + rings_5
    ring_atoms = set()
    for ring in all_rings:
        ring_atoms.update(ring)
        
    # For fused rings, number of total ring atoms should be less than sum of individual ring sizes
    # due to shared atoms
    expected_unfused = sum(len(ring) for ring in all_rings)
    if len(ring_atoms) >= expected_unfused:
        return False, "Rings are not fused in steroid pattern"
        
    # Additional check for typical steroid characteristics
    # Most steroids have multiple methyl groups and often hydroxyl groups
    methyl_count = len(mol.GetSubstructMatches(Chem.MolFromSmarts('[CH3]')))
    hydroxyl_count = len(mol.GetSubstructMatches(Chem.MolFromSmarts('[OH]')))
    
    if methyl_count < 2:
        return False, "Insufficient methyl groups for typical steroid structure"
        
    return True, f"C27 steroid with {methyl_count} methyl groups and {hydroxyl_count} hydroxyl groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131619',
                          'name': 'C27-steroid',
                          'definition': 'A steroid compound with a structure '
                                        'based on a 27-carbon (cholestane) '
                                        'skeleton.',
                          'parents': ['CHEBI:35341']},
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
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 15417,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 0.6666666666666666,
    'f1': 0.03809523809523809,
    'accuracy': 0.9934922680412371}