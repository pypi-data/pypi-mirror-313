"""
Classifies: CHEBI:167095 secondary fatty alcohol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_secondary_fatty_alcohol(smiles: str):
    """
    Determines if a molecule is a secondary fatty alcohol.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a secondary fatty alcohol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for presence of OH group
    oh_pattern = Chem.MolFromSmarts('[OH1]')
    oh_matches = mol.GetSubstructMatches(oh_pattern)
    if not oh_matches:
        return False, "No hydroxyl group found"
    
    if len(oh_matches) > 1:
        return False, "Multiple hydroxyl groups found"
        
    # Get the carbon atom connected to OH
    oh_atom = mol.GetAtomWithIdx(oh_matches[0][0])
    c_atom = oh_atom.GetNeighbors()[0]
    
    if c_atom.GetSymbol() != 'C':
        return False, "Hydroxyl not attached to carbon"
        
    # Check if OH is attached to secondary carbon
    c_neighbors = c_atom.GetNeighbors()
    carbon_neighbors = sum(1 for n in c_neighbors if n.GetSymbol() == 'C')
    if carbon_neighbors != 2:
        return False, "Hydroxyl not attached to secondary carbon"
        
    # Count total carbons in longest chain
    carbon_pattern = Chem.MolFromSmarts('C-C-C') # Minimum 3 carbons
    carbon_matches = mol.GetSubstructMatches(carbon_pattern)
    if not carbon_matches:
        return False, "No valid carbon chain found"
        
    # Find the longest carbon chain containing the OH group
    def find_chain_length(atom, visited):
        if atom.GetSymbol() != 'C':
            return 0
        max_length = 0
        visited.add(atom.GetIdx())
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in visited and neighbor.GetSymbol() == 'C':
                length = 1 + find_chain_length(neighbor, visited.copy())
                max_length = max(max_length, length)
        return max_length

    chain_length = 1 + find_chain_length(c_atom, {c_atom.GetIdx()})
    
    if chain_length < 3:
        return False, "Chain too short (less than 3 carbons)"
    if chain_length > 27:
        return False, "Chain too long (more than 27 carbons)"
    
    # Check if carbon with OH is saturated
    for bond in c_atom.GetBonds():
        if bond.GetBondType() != Chem.BondType.SINGLE:
            return False, "Carbon with hydroxyl group is not saturated"
    
    # Calculate position of OH group
    def count_carbons_to_end(atom, visited, direction):
        if atom.GetSymbol() != 'C':
            return 0
        count = 1
        visited.add(atom.GetIdx())
        max_chain = 0
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in visited and neighbor.GetSymbol() == 'C':
                chain_length = count_carbons_to_end(neighbor, visited.copy(), direction)
                max_chain = max(max_chain, chain_length)
        return count + max_chain

    # Count carbons in both directions from OH
    visited = {c_atom.GetIdx()}
    pos1 = count_carbons_to_end(c_atom, visited.copy(), 'forward')
    pos2 = count_carbons_to_end(c_atom, visited.copy(), 'backward')
    oh_position = min(pos1, pos2)

    return True, f"Secondary fatty alcohol with {chain_length} carbons, OH at position {oh_position}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:167095',
                          'name': 'secondary fatty alcohol',
                          'definition': 'A fatty alcohol consisting of a chain '
                                        'of 3 to greater than 27 carbon atoms '
                                        'in which a hydroxy group is attached '
                                        'to a saturated carbon atom different '
                                        'from the terminal carbons. Secondary '
                                        'fatty alcohols may be saturated or '
                                        'unsaturated and may be branched or '
                                        'unbranched.',
                          'parents': ['CHEBI:24026', 'CHEBI:35681']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: 'Mol' object has no attribute "
               "'HasSubstructMatches'",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 13,
    'num_false_positives': 100,
    'num_true_negatives': 2158,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.11504424778761062,
    'recall': 1.0,
    'f1': 0.20634920634920637,
    'accuracy': 0.9559665345662703}