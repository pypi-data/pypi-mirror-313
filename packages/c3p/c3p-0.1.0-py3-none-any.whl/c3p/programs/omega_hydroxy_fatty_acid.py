"""
Classifies: CHEBI:10615 omega-hydroxy fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_omega_hydroxy_fatty_acid(smiles: str):
    """
    Determines if a molecule is an omega-hydroxy fatty acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an omega-hydroxy fatty acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxyl_pattern = Chem.MolFromSmarts('C(=O)O')
    if not mol.HasSubstructMatch(carboxyl_pattern):
        return False, "No carboxylic acid group found"
    
    # Find carboxylic acid carbon
    matches = mol.GetSubstructMatches(carboxyl_pattern)
    carboxyl_carbon = matches[0][0]
    
    # Get all terminal OH groups
    terminal_oh_pattern = Chem.MolFromSmarts('[OH][CH2]C')
    if not mol.HasSubstructMatch(terminal_oh_pattern):
        return False, "No terminal hydroxyl group found"
        
    # Get all carbons in longest chain from carboxyl carbon
    visited = set()
    longest_chain = []
    
    def get_longest_chain(atom_idx, current_chain):
        nonlocal longest_chain
        visited.add(atom_idx)
        current_chain.append(atom_idx)
        
        atom = mol.GetAtomWithIdx(atom_idx)
        neighbors = atom.GetNeighbors()
        
        terminal = True
        for neighbor in neighbors:
            n_idx = neighbor.GetIdx()
            if n_idx not in visited and neighbor.GetSymbol() == 'C':
                terminal = False
                get_longest_chain(n_idx, current_chain.copy())
                
        if terminal and len(current_chain) > len(longest_chain):
            longest_chain = current_chain.copy()
        visited.remove(atom_idx)
        current_chain.pop()
            
    get_longest_chain(carboxyl_carbon, [])
    
    # Check if terminal carbon has OH group
    terminal_carbon = mol.GetAtomWithIdx(longest_chain[-1])
    has_terminal_oh = False
    for neighbor in terminal_carbon.GetNeighbors():
        if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 1:
            has_terminal_oh = True
            break
            
    if not has_terminal_oh:
        return False, "Hydroxyl group not at terminal (omega) position"
        
    # Check if chain is straight (each carbon has max 2 carbons connected)
    for idx in longest_chain:
        atom = mol.GetAtomWithIdx(idx)
        carbon_neighbors = sum(1 for n in atom.GetNeighbors() if n.GetSymbol() == 'C')
        if carbon_neighbors > 2:
            return False, "Chain is branched"
            
    chain_length = len(longest_chain)
    return True, f"Omega-hydroxy fatty acid with chain length {chain_length}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:10615',
                          'name': 'omega-hydroxy fatty acid',
                          'definition': 'Any member of the class of '
                                        'naturally-occurring straight-chain '
                                        'fatty acids n carbon atoms long with '
                                        'a carboxyl group at position 1 and a '
                                        'hydroxyl at position n (omega).',
                          'parents': ['CHEBI:15734', 'CHEBI:24654']},
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
    'num_true_negatives': 3099,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.08256880733944955,
    'recall': 1.0,
    'f1': 0.15254237288135594,
    'accuracy': 0.9688279301745636}