"""
Classifies: CHEBI:17135 long-chain fatty alcohol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_long_chain_fatty_alcohol(smiles: str):
    """
    Determines if a molecule is a long-chain fatty alcohol (C13-C22 with at least one OH group).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a long-chain fatty alcohol, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for presence of OH group
    oh_pattern = Chem.MolFromSmarts('[OH]')
    if not mol.HasSubstructMatch(oh_pattern):
        return False, "No hydroxyl group found"
    
    # Count carbons
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    
    # Check carbon count range for long chain (C13-C22)
    if carbon_count < 13:
        return False, f"Carbon chain too short (C{carbon_count})"
    if carbon_count > 22:
        return False, f"Carbon chain too long (C{carbon_count})"
        
    # Check for continuous carbon chain
    longest_chain = 0
    for i in range(mol.GetNumAtoms()):
        if mol.GetAtomWithIdx(i).GetSymbol() == 'C':
            # Do BFS from each carbon to find longest chain
            visited = set()
            queue = [(i, 1)]
            while queue:
                current, length = queue.pop(0)
                visited.add(current)
                
                for neighbor in mol.GetAtomWithIdx(current).GetNeighbors():
                    if neighbor.GetIdx() not in visited and neighbor.GetSymbol() == 'C':
                        queue.append((neighbor.GetIdx(), length + 1))
                        longest_chain = max(longest_chain, length + 1)

    if longest_chain < 13:
        return False, f"Longest continuous carbon chain too short (C{longest_chain})"
        
    # Count number of OH groups
    oh_count = len(mol.GetSubstructMatches(oh_pattern))
    
    return True, f"Long-chain fatty alcohol with {carbon_count} carbons and {oh_count} OH groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17135',
                          'name': 'long-chain fatty alcohol',
                          'definition': 'A fatty alcohol with a chain length '
                                        'ranging from C13 to C22.',
                          'parents': ['CHEBI:24026']},
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
    'num_true_positives': 30,
    'num_false_positives': 100,
    'num_true_negatives': 2331,
    'num_false_negatives': 11,
    'num_negatives': None,
    'precision': 0.23076923076923078,
    'recall': 0.7317073170731707,
    'f1': 0.3508771929824562,
    'accuracy': 0.9550970873786407}