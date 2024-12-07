"""
Classifies: CHEBI:189832 hydroperoxy polyunsaturated fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_hydroperoxy_polyunsaturated_fatty_acid(smiles: str):
    """
    Determines if a molecule is a hydroperoxy polyunsaturated fatty acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydroperoxy polyunsaturated fatty acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"

    # Check for hydroperoxy group (-OOH)
    hydroperoxy_pattern = Chem.MolFromSmarts('[OH]O')
    hydroperoxy_matches = mol.GetSubstructMatches(hydroperoxy_pattern)
    if not hydroperoxy_matches:
        return False, "No hydroperoxy group found"

    # Count number of double bonds
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    double_bond_matches = mol.GetSubstructMatches(double_bond_pattern)
    
    if len(double_bond_matches) < 2:
        return False, "Not polyunsaturated (fewer than 2 double bonds)"

    # Verify it's a fatty acid by checking carbon chain length
    # Typically fatty acids have 12+ carbons
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 12:
        return False, "Carbon chain too short for fatty acid"

    return True, f"Contains {len(hydroperoxy_matches)} hydroperoxy group(s) and {len(double_bond_matches)} double bonds"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:189832',
                          'name': 'hydroperoxy polyunsaturated fatty acid',
                          'definition': 'Any polyunsaturated fatty acid '
                                        'carrying one or more hydroperoxy '
                                        'substituents.',
                          'parents': ['CHEBI:194321', 'CHEBI:26208']},
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
    'num_true_positives': 11,
    'num_false_positives': 17,
    'num_true_negatives': 183807,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.39285714285714285,
    'recall': 1.0,
    'f1': 0.5641025641025641,
    'accuracy': 0.9999075257703919}