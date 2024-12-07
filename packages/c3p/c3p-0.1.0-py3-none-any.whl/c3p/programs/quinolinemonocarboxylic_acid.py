"""
Classifies: CHEBI:26512 quinolinemonocarboxylic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_quinolinemonocarboxylic_acid(smiles: str):
    """
    Determines if a molecule is a quinoline monocarboxylic acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a quinoline monocarboxylic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for quinoline core structure
    quinoline_pattern = Chem.MolFromSmarts('c1cccc2c1ncc[c]2')
    if not mol.HasSubstructMatch(quinoline_pattern):
        return False, "No quinoline core structure found"
        
    # Count carboxylic acid groups
    carboxyl_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
    carboxyl_matches = mol.GetSubstructMatches(carboxyl_pattern)
    
    if len(carboxyl_matches) == 0:
        return False, "No carboxylic acid group found"
    elif len(carboxyl_matches) > 1:
        return False, "More than one carboxylic acid group found"
        
    # Verify that carboxylic acid is attached to quinoline
    quinoline_matches = mol.GetSubstructMatches(quinoline_pattern)
    quinoline_atoms = set()
    for match in quinoline_matches:
        quinoline_atoms.update(match)
        
    carboxyl_carbon = carboxyl_matches[0][0]
    
    # Check if carboxyl group is connected to quinoline system
    carboxyl_neighbors = [x.GetIdx() for x in mol.GetAtomWithIdx(carboxyl_carbon).GetNeighbors()]
    is_connected = any(neighbor in quinoline_atoms for neighbor in carboxyl_neighbors)
    
    if not is_connected:
        return False, "Carboxylic acid group not connected to quinoline system"
        
    return True, "Contains quinoline core with one attached carboxylic acid group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26512',
                          'name': 'quinolinemonocarboxylic acid',
                          'definition': 'Any aromatic carboxylic acid that '
                                        'contains a quinoline moiety that is '
                                        'substituted by one carboxy '
                                        'substituent.',
                          'parents': ['CHEBI:26513', 'CHEBI:33859']},
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
    'num_false_positives': 94,
    'num_true_negatives': 183808,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.030927835051546393,
    'recall': 1.0,
    'f1': 0.06000000000000001,
    'accuracy': 0.999488866534352}