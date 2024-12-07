"""
Classifies: CHEBI:26643 aldehydic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_aldehydic_acid(smiles: str):
    """
    Determines if a molecule is an aldehydic acid (contains both carboxylic acid and aldehyde groups).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an aldehydic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for carboxylic acid group using SMARTS
    carboxylic_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
    has_carboxylic = len(mol.GetSubstructMatches(carboxylic_pattern)) > 0
    
    # Check for aldehyde group using SMARTS
    aldehyde_pattern = Chem.MolFromSmarts('[CX3H1](=O)[#6]')
    has_aldehyde = len(mol.GetSubstructMatches(aldehyde_pattern)) > 0
    
    if not has_carboxylic:
        return False, "No carboxylic acid group found"
        
    if not has_aldehyde:
        return False, "No aldehyde group found"
        
    # Count number of carboxylic acid groups
    if len(mol.GetSubstructMatches(carboxylic_pattern)) > 1:
        return False, "More than one carboxylic acid group found"
        
    # Count number of aldehyde groups
    if len(mol.GetSubstructMatches(aldehyde_pattern)) > 1:
        return False, "More than one aldehyde group found"
    
    # Additional check to ensure the aldehyde and carboxylic groups are not on the same carbon
    for match1 in mol.GetSubstructMatches(carboxylic_pattern):
        for match2 in mol.GetSubstructMatches(aldehyde_pattern):
            if match1[0] == match2[0]:  # Compare carbon atoms
                return False, "Aldehyde and carboxylic acid groups are on the same carbon"
    
    # If we get here, the molecule has exactly one carboxylic acid and one aldehyde group
    return True, "Contains one carboxylic acid group and one aldehyde group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26643',
                          'name': 'aldehydic acid',
                          'definition': 'A monocarboxylic acid derived from '
                                        'any dicarboxylic acid that has a '
                                        'retained name by the formal reduction '
                                        'of one of the carboxy groups to a '
                                        'formyl group. The resulting '
                                        'structure, also known as a '
                                        'semialdehyde, may be named by '
                                        "replacing the ending '...ic acid' of "
                                        'the retained name of the dicarboxylic '
                                        "acid by the ending '...aldehydic "
                                        "acid'. Aldehydic acids therefore "
                                        'contain one carboxy group and one '
                                        'aldehyde group.',
                          'parents': ['CHEBI:17478', 'CHEBI:25384']},
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
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 59062,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 1.0,
    'f1': 0.07407407407407407,
    'accuracy': 0.9983098401108745}