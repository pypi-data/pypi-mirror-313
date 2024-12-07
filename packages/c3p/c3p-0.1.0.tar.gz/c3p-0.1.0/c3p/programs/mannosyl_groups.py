"""
Classifies: CHEBI:25171 mannosyl groups
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_mannosyl_groups(smiles: str):
    """
    Determines if a molecule contains mannosyl groups.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains mannosyl groups, False otherwise
        str: Reason for classification
    """
    # Check for valid SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for pyranose ring pattern characteristic of mannose
    mannose_pattern = Chem.MolFromSmarts('[C@@H]1[C@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O')
    if not mol.HasSubstructMatch(mannose_pattern):
        return False, "No mannose pyranose ring pattern found"
        
    # Check for glycosidic linkage (removal of hemiacetal OH)
    if '*' not in smiles:
        return False, "No glycosidic linkage point found"
        
    # Count number of mannose units
    matches = mol.GetSubstructMatches(mannose_pattern)
    num_mannose = len(matches)
    
    # Additional checks for correct stereochemistry at C2 position
    c2_pattern = Chem.MolFromSmarts('[C@@H]([C@H]1O[C@H]([C@H]([C@@H]([C@H]1O)O)O)CO)O')
    if not mol.HasSubstructMatch(c2_pattern):
        return False, "Incorrect stereochemistry for mannose"
        
    # Check if terminal mannose has glycosidic linkage
    terminal_pattern = Chem.MolFromSmarts('[C@@H]1[C@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O*')
    if not mol.HasSubstructMatch(terminal_pattern):
        return False, "Terminal mannose unit not properly linked"
        
    return True, f"Contains {num_mannose} mannosyl group(s) with correct stereochemistry and glycosidic linkage"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25171',
                          'name': 'mannosyl groups',
                          'definition': 'A glycosyl group obtained by removing '
                                        'the hydroxy group from the hemiacetal '
                                        'function of a mannose and, by '
                                        'extension, of a lower oligosaccharide '
                                        'having mannose at the reducing end.',
                          'parents': ['CHEBI:24403']},
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
    'num_true_negatives': 183910,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999891252338075}