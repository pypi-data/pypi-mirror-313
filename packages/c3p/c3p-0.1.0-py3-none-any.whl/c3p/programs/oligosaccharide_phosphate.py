"""
Classifies: CHEBI:16916 oligosaccharide phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_oligosaccharide_phosphate(smiles: str):
    """
    Determines if a molecule is an oligosaccharide phosphate (oligosaccharide with at least one phosphorylated hydroxy group)
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an oligosaccharide phosphate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of phosphate groups
    phosphate_pattern = Chem.MolFromSmarts('[P](=O)([O,OH])[O,OH]')
    if not mol.HasSubstructMatch(phosphate_pattern):
        return False, "No phosphate groups found"
    
    # Count sugar rings (pyranose/furanose)
    sugar_pattern = Chem.MolFromSmarts('[C,O]1[C][C][C][C][O]1') # pyranose
    sugar_pattern2 = Chem.MolFromSmarts('[C,O]1[C][C][C][O]1') # furanose
    
    sugar_rings = len(mol.GetSubstructMatches(sugar_pattern)) + len(mol.GetSubstructMatches(sugar_pattern2))
    
    if sugar_rings < 2:
        return False, "Not an oligosaccharide - requires at least 2 sugar rings"
        
    # Check for characteristic sugar hydroxyl groups
    hydroxyl_pattern = Chem.MolFromSmarts('[C][OH]')
    if not mol.HasSubstructMatch(hydroxyl_pattern):
        return False, "No hydroxyl groups found - not a sugar structure"
        
    # Count phosphate groups
    num_phosphates = len(mol.GetSubstructMatches(phosphate_pattern))
    
    return True, f"Oligosaccharide with {sugar_rings} sugar rings and {num_phosphates} phosphate group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16916',
                          'name': 'oligosaccharide phosphate',
                          'definition': 'An oligosaccharide derivative in '
                                        'which at least one hydroxy group has '
                                        'been phosphorylated.',
                          'parents': ['CHEBI:26816', 'CHEBI:63563']},
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
    'num_true_positives': 9,
    'num_false_positives': 100,
    'num_true_negatives': 12615,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.08256880733944955,
    'recall': 1.0,
    'f1': 0.15254237288135594,
    'accuracy': 0.9921408362150267}