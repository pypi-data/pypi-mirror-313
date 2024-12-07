"""
Classifies: CHEBI:17264 phosphatidylglycerol phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_phosphatidylglycerol_phosphate(smiles: str):
    """
    Determines if a molecule is a phosphatidylglycerol phosphate.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a phosphatidylglycerol phosphate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for required phosphate groups
    phosphate_pattern = Chem.MolFromSmarts('[P](=O)([O,OH])[O,OH]')
    phosphate_matches = mol.GetSubstructMatches(phosphate_pattern)
    if len(phosphate_matches) < 2:
        return False, "Missing required phosphate groups"
        
    # Check for glycerol backbone with ester linkages
    glycerol_pattern = Chem.MolFromSmarts('OCC(O)COP(=O)(O)O')
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "Missing glycerol backbone with phosphate"
        
    # Check for fatty acid ester linkages
    ester_pattern = Chem.MolFromSmarts('C(=O)OC')
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    if len(ester_matches) < 2:
        return False, "Missing required fatty acid ester linkages"
        
    # Check for terminal phosphate group
    terminal_phosphate = Chem.MolFromSmarts('COP(=O)(O)O')
    if not mol.HasSubstructMatch(terminal_phosphate):
        return False, "Missing terminal phosphate group"
        
    # Count total oxygens to verify phosphatidylglycerol phosphate structure
    num_o = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8)
    if num_o < 11:  # Minimum oxygens needed for core structure
        return False, "Insufficient oxygen atoms for phosphatidylglycerol phosphate"

    return True, "Contains phosphatidylglycerol phosphate core structure with required functional groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17264',
                          'name': 'phosphatidylglycerol phosphate',
                          'definition': 'A phosphatidylglycerol in which one '
                                        'of the hydroxy groups of the glycerol '
                                        'moiety has been converted to the '
                                        'corresponding dihydrogen phosphate.',
                          'parents': ['CHEBI:17517']},
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
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 13962,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.9928901528617134}