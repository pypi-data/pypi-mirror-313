"""
Classifies: CHEBI:143004 ultra-long-chain fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_ultra_long_chain_fatty_acid(smiles: str):
    """
    Determines if a molecule is an ultra-long-chain fatty acid (chain length > C27).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an ultra-long-chain fatty acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxylic_acid_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_acid_pattern):
        return False, "No carboxylic acid group found"

    # Count carbons in longest chain
    # First convert to explicit hydrogens to ensure proper chain finding
    mol = Chem.AddHs(mol)
    
    # Find the carboxylic acid carbon
    matches = mol.GetSubstructMatches(carboxylic_acid_pattern)
    if not matches:
        return False, "Could not locate carboxylic acid carbon"
    
    acid_carbon = matches[0][0]
    
    # Use BFS to find longest carbon chain starting from acid carbon
    visited = set()
    queue = [(acid_carbon, [acid_carbon])]
    longest_chain = []
    
    while queue:
        current_atom_idx, current_path = queue.pop(0)
        current_atom = mol.GetAtomWithIdx(current_atom_idx)
        
        if len(current_path) > len(longest_chain):
            longest_chain = current_path
            
        for neighbor in current_atom.GetNeighbors():
            neighbor_idx = neighbor.GetIdx()
            if (neighbor_idx not in visited and 
                neighbor.GetSymbol() == 'C'):
                visited.add(neighbor_idx)
                queue.append((neighbor_idx, current_path + [neighbor_idx]))

    chain_length = len(longest_chain)
    
    if chain_length > 27:
        return True, f"Ultra-long-chain fatty acid with chain length C{chain_length}"
    else:
        return False, f"Chain length C{chain_length} is not greater than C27"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:143004',
                          'name': 'ultra-long-chain fatty acid',
                          'definition': 'Any very long-chain fatty acid which '
                                        'has a chain length greater than C27.',
                          'parents': ['CHEBI:27283']},
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
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 94864,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.9989470248186251}