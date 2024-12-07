"""
Classifies: CHEBI:145039 polyunsaturated fatty ester
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_polyunsaturated_fatty_ester(smiles: str):
    """
    Determines if a molecule is a polyunsaturated fatty ester.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a polyunsaturated fatty ester, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for ester group
    ester_pattern = Chem.MolFromSmarts('[C,c](=O)O[C,c]')
    if not mol.HasSubstructMatch(ester_pattern):
        return False, "No ester group found"
        
    # Count double and triple bonds
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    triple_bond_pattern = Chem.MolFromSmarts('C#C')
    
    double_bonds = len(mol.GetSubstructMatches(double_bond_pattern))
    triple_bonds = len(mol.GetSubstructMatches(triple_bond_pattern))
    
    total_unsaturations = double_bonds + triple_bonds
    
    if total_unsaturations < 2:
        return False, "Not polyunsaturated (less than 2 unsaturations found)"
        
    # Check for fatty acid chain - look for a chain of at least 4 carbons
    fatty_chain_pattern = Chem.MolFromSmarts('CCCC')
    if not mol.HasSubstructMatch(fatty_chain_pattern):
        return False, "No fatty acid chain found (minimum 4 carbons)"
        
    # If we get here, we have:
    # 1. An ester group
    # 2. Multiple unsaturations
    # 3. A fatty acid chain
    reason = f"Found polyunsaturated fatty ester with {double_bonds} double bonds and {triple_bonds} triple bonds"
    return True, reason


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:145039',
                          'name': 'polyunsaturated fatty ester',
                          'definition': 'Any fatty acid ester resulting from '
                                        'the formal esterification of the '
                                        'carboxy group of a polyunsaturated '
                                        'fatty acid.',
                          'parents': ['CHEBI:35748']},
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
    'num_true_negatives': 1352,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.9312714776632303}