"""
Classifies: CHEBI:140345 hydroxy polyunsaturated fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_hydroxy_polyunsaturated_fatty_acid(smiles: str):
    """
    Determines if a molecule is a hydroxy polyunsaturated fatty acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydroxy polyunsaturated fatty acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for carboxylic acid group
    carboxylic_acid_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_acid_pattern):
        return False, "No carboxylic acid group found"
        
    # Check for hydroxy groups (excluding the carboxylic acid OH)
    hydroxy_pattern = Chem.MolFromSmarts('[C,c][OH]')
    hydroxy_matches = mol.GetSubstructMatches(hydroxy_pattern)
    
    if len(hydroxy_matches) == 0:
        return False, "No hydroxy substituents found"
        
    # Check for multiple double bonds
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    double_bond_matches = mol.GetSubstructMatches(double_bond_pattern)
    
    if len(double_bond_matches) < 2:
        return False, "Not polyunsaturated (less than 2 double bonds)"
        
    # Count number of hydroxy groups and double bonds
    num_hydroxy = len(hydroxy_matches)
    num_double_bonds = len(double_bond_matches)
    
    return True, f"Found {num_hydroxy} hydroxy groups and {num_double_bonds} double bonds"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140345',
                          'name': 'hydroxy polyunsaturated fatty acid',
                          'definition': 'Any polyunsaturated fatty acid '
                                        'carrying one or more hydroxy '
                                        'substituents.',
                          'parents': ['CHEBI:24654', 'CHEBI:26208']},
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
    'num_true_positives': 27,
    'num_false_positives': 100,
    'num_true_negatives': 3488,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.2125984251968504,
    'recall': 1.0,
    'f1': 0.35064935064935066,
    'accuracy': 0.9723374827109267}