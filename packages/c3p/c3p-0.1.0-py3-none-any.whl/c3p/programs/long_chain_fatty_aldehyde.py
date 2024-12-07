"""
Classifies: CHEBI:17176 long-chain fatty aldehyde
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from collections import deque

def is_long_chain_fatty_aldehyde(smiles: str):
    """
    Determines if a molecule is a long-chain fatty aldehyde (C13-C22).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a long-chain fatty aldehyde, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for aldehyde group (C=O with H)
    aldehyde_pattern = Chem.MolFromSmarts('[CH1](=O)')
    if not mol.HasSubstructMatch(aldehyde_pattern):
        return False, "No aldehyde group found"

    # Count number of aldehyde groups
    matches = mol.GetSubstructMatches(aldehyde_pattern)
    if len(matches) > 1:
        return False, "Multiple aldehyde groups found"

    # Get the aldehyde carbon
    aldehyde_carbon = matches[0][0]

    # Function to check if atom is part of an aromatic ring
    def is_in_aromatic_ring(atom_idx):
        atom = mol.GetAtomWithIdx(atom_idx)
        return atom.GetIsAromatic()

    # Find the longest carbon chain containing the aldehyde carbon
    def find_longest_chain(start_idx):
        visited = {start_idx}
        queue = deque([(start_idx, [start_idx])])
        longest_path = []
        
        while queue:
            current_idx, current_path = queue.popleft()
            current_atom = mol.GetAtomWithIdx(current_idx)
            
            if len(current_path) > len(longest_path):
                longest_path = current_path
                
            for neighbor in current_atom.GetNeighbors():
                neighbor_idx = neighbor.GetIdx()
                if (neighbor_idx not in visited and 
                    neighbor.GetSymbol() == 'C'):
                    visited.add(neighbor_idx)
                    queue.append((neighbor_idx, current_path + [neighbor_idx]))
                    
        return longest_path

    longest_chain = find_longest_chain(aldehyde_carbon)
    chain_length = len(longest_chain)
    
    # Check chain length
    if chain_length < 13 or chain_length > 22:
        return False, f"Carbon chain length C{chain_length} outside C13-C22 range"

    # Check if the molecule is primarily a straight chain
    total_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    branch_carbons = total_carbons - chain_length
    if branch_carbons > 2:  # Allow minimal branching
        return False, "Structure too branched for a fatty aldehyde"
        
    # Check for cyclic structures
    if mol.GetRingInfo().NumRings() > 0:
        return False, "Contains cyclic structures"

    # Check for carboxylic acid groups
    carboxyl_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
    if mol.HasSubstructMatch(carboxyl_pattern):
        return False, "Contains carboxylic acid group"

    return True, f"Long-chain fatty aldehyde with {chain_length} carbons"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17176',
                          'name': 'long-chain fatty aldehyde',
                          'definition': 'A fatty aldehyde that has a chain '
                                        'length ranging from C13 to C22.',
                          'parents': ['CHEBI:35746']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.038461538461538464 is too low.\n'
               "True positives: [('[H]C(=O)CCCCCC\\\\C=C/CCCCCCCC', "
               "'Long-chain fatty aldehyde with 17 carbons'), "
               "('C(CCCCCCCCCC(C(=O)[H])O)CCCC', 'Long-chain fatty aldehyde "
               "with 16 carbons')]\n"
               "False positives: [('O=CCCCCCCCCCCCCCCCCCC', 'Long-chain fatty "
               "aldehyde with 19 carbons'), "
               "('O=CCC\\\\C=C\\\\C=C\\\\CCC\\\\C=C\\\\CCCC', 'Long-chain "
               "fatty aldehyde with 16 carbons'), ('O=CCCCC/C=C/CCC/C=C/CCCC', "
               "'Long-chain fatty aldehyde with 16 carbons'), "
               "('O=C(CCCCCCCCCCC)CC=O', 'Long-chain fatty aldehyde with 14 "
               "carbons'), ('O=CCCCCCCCC/C=C/CCCCC', 'Long-chain fatty "
               "aldehyde with 16 carbons'), "
               "('O=CCC(CCC[C@@H](CCC[C@@H](CCCC(C)C)C)C)C', 'Long-chain fatty "
               "aldehyde with 16 carbons'), "
               "('[H]C(=O)\\\\C=C\\\\CCCCCCCCCC(C)C', 'Long-chain fatty "
               "aldehyde with 14 carbons'), ('O=CCCCCCCC\\\\C=C\\\\CCCCCCCC', "
               "'Long-chain fatty aldehyde with 18 carbons'), "
               "('O=CCCCCCCCC/C=C/C=C/C=C/C', 'Long-chain fatty aldehyde with "
               "16 carbons'), ('[H]C(=O)CCCC([H])=CCC=C([H])CCCCC', "
               "'Long-chain fatty aldehyde with 14 carbons'), "
               "('O=C(C#CC#CCCCCCCCCCC)CC=O', 'Long-chain fatty aldehyde with "
               "17 carbons'), "
               "('[H]C(=O)C(\\\\C)=C\\\\C=C\\\\C(C)=C\\\\C=C\\\\C=C(C)\\\\C=C\\\\C=C(/C)C([H])=O', "
               "'Long-chain fatty aldehyde with 16 carbons'), "
               "('O=CCCCCCCC/C=C/C\\\\C=C\\\\CCCCC', 'Long-chain fatty "
               "aldehyde with 18 carbons'), ('O=CCCCCCCC/C=C/C=C/CCCC', "
               "'Long-chain fatty aldehyde with 16 carbons'), "
               "('O=C(CCCCC/C=C\\\\CCCCCC)CC=O', 'Long-chain fatty aldehyde "
               "with 16 carbons'), ('O=CCCCCCCC=CCC=CCCCCC', 'Long-chain fatty "
               "aldehyde with 17 carbons'), ('CCCCCCCCCCCCCCCCCC=O', "
               "'Long-chain fatty aldehyde with 18 carbons'), "
               "('C(\\\\C=C\\\\C([H])=O)(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C(=O)[H])\\\\C)\\\\C)/C)/C', "
               "'Long-chain fatty aldehyde with 20 carbons'), "
               "('O=CCCCCCCCCCC#C/C=C\\\\CC', 'Long-chain fatty aldehyde with "
               "16 carbons'), ('O=CCCCCCCCCC/C=C/CC', 'Long-chain fatty "
               "aldehyde with 14 carbons'), "
               "('O=C/C=C/C=C/C=C/C=C/C=C/C=C/C=C/C=C/C=C/C', 'Long-chain "
               "fatty aldehyde with 20 carbons'), "
               "('O=CCCCCCCCCC/C=C/C=C\\\\CC', 'Long-chain fatty aldehyde with "
               "16 carbons'), ('O=C/C=C/C=C/C=C/C=C/C=C/C=C/C=O', 'Long-chain "
               "fatty aldehyde with 14 carbons'), "
               "('O=CCC[C@H](CC/C=C\\\\CC/C=C\\\\CCCCC)C', 'Long-chain fatty "
               "aldehyde with 17 carbons'), ('IC(CCCCCCCCCCCCCC)C=O', "
               "'Long-chain fatty aldehyde with 16 carbons'), "
               "('C(CCCCCCCCCC(=O)[H])CCCCC([O-])=O', 'Long-chain fatty "
               "aldehyde with 16 carbons'), "
               "('O=C/C=C/C=C/C=C/C=C/C=C/C=C/C/C=C\\\\C', 'Long-chain fatty "
               "aldehyde with 17 carbons'), ('[H]C(=O)C(C)CCCCCCCCCCCCC', "
               "'Long-chain fatty aldehyde with 15 carbons'), "
               "('O=C/C=C\\\\C(CCCCCCCCCC)=C', 'Long-chain fatty aldehyde with "
               "14 carbons'), ('O=CCCCCCC/C=C/C/C=C\\\\C/C=C/CC', 'Long-chain "
               "fatty aldehyde with 17 carbons'), "
               "('O=C/C=C/C=C/C=C/C=C/C=C/[C@H](O)C/C=C\\\\C', 'Long-chain "
               "fatty aldehyde with 16 carbons'), "
               "('[O-]C(=O)CCCCCCCCCCCCCCCCCCCCC=O', 'Long-chain fatty "
               "aldehyde with 22 carbons'), ('CC(C)CCCC(C)CCCC(C)CCCC(C)C=O', "
               "'Long-chain fatty aldehyde with 15 carbons'), "
               "('O=CCCCCC/C=C\\\\CCCCCC', 'Long-chain fatty aldehyde with 14 "
               "carbons'), "
               "('C(/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=C(\\\\CCC=C(C)C)/C)\\\\C)\\\\C)/C)([H])=O', "
               "'Long-chain fatty aldehyde with 22 carbons'), "
               "('CC(CC/C=C(\\\\CC/C=C(\\\\CCC(=O)[H])/C)/C)=O', 'Long-chain "
               "fatty aldehyde with 13 carbons'), "
               "('O=CCCCCCCCC\\\\C=C/C=C\\\\CCC', 'Long-chain fatty aldehyde "
               "with 16 carbons'), ('BrC(CCCCCCCCCCCCCC)C=O', 'Long-chain "
               "fatty aldehyde with 16 carbons'), "
               "('O=C/C=C\\\\C=C\\\\CCCCCCCCCC', 'Long-chain fatty aldehyde "
               "with 15 carbons'), ('C(CCCCCCCCCC(=O)[H])CCCCC(O)=O', "
               "'Long-chain fatty aldehyde with 16 carbons'), "
               "('O=CCCCCCCCCCCCCCCCCCCC', 'Long-chain fatty aldehyde with 20 "
               "carbons'), ('O=CCCCCC\\\\C=C\\\\CCCCCC', 'Long-chain fatty "
               "aldehyde with 14 carbons'), ('O=CCC\\\\C=C\\\\C=C/CCCCCCCCC', "
               "'Long-chain fatty aldehyde with 16 carbons'), "
               "('O=C/C=C(/CC/C=C(/CC/C=C(/CCC=C(C)C)\\\\C)\\\\C)\\\\C', "
               "'Long-chain fatty aldehyde with 16 carbons'), "
               "('O=C\\\\C=C\\\\C=C\\\\C/C=C\\\\CCCCC', 'Long-chain fatty "
               "aldehyde with 13 carbons'), ('O=CCCCCCCCCC/C=C\\\\C=C/CC', "
               "'Long-chain fatty aldehyde with 16 carbons'), "
               "('OC(=O)CCCCCCC/C=C/C=C/C=O', 'Long-chain fatty aldehyde with "
               "13 carbons'), ('O=C\\\\C=C\\\\C=C\\\\CCCCCCCCCC', 'Long-chain "
               "fatty aldehyde with 15 carbons'), "
               "('O=CCCCCC/C=C\\\\CC/C=C\\\\C=C\\\\CC', 'Long-chain fatty "
               "aldehyde with 16 carbons'), ('O=CCCCCCCCCC/C=C\\\\CCCCCCCC', "
               "'Long-chain fatty aldehyde with 20 carbons'), "
               "('[H]C(=O)\\\\C=C\\\\CCCCCCCCCCCCC', 'Long-chain fatty "
               "aldehyde with 16 carbons'), ('O=CCCC\\\\C=C\\\\CCCCCCCC', "
               "'Long-chain fatty aldehyde with 14 carbons'), "
               "('O=CCCCCCCC/C=C\\\\C=C\\\\CCCC', 'Long-chain fatty aldehyde "
               "with 16 carbons'), ('O=CCCCCCCC/C=C/C=C\\\\CCCC', 'Long-chain "
               "fatty aldehyde with 16 carbons'), "
               "('[H]C(=O)C([H])=C([H])CCCCCCCCCCCCC', 'Long-chain fatty "
               "aldehyde with 16 carbons'), "
               "('[H]C(=O)C=C([H])CCCCCCCC([H])=CCC', 'Long-chain fatty "
               "aldehyde with 14 carbons'), ('O=CCCCCCCCC/C=C/C=C/C=C\\\\C', "
               "'Long-chain fatty aldehyde with 16 carbons'), "
               "('O=CCCCCC/C=C\\\\CC\\\\C=C\\\\CCCC', 'Long-chain fatty "
               "aldehyde with 16 carbons'), "
               "('O=C\\\\C=C\\\\CCCCCCCCC/C=C\\\\CCCC', 'Long-chain fatty "
               "aldehyde with 18 carbons'), ('O=CCCCCCCC/C=C/CCCC', "
               "'Long-chain fatty aldehyde with 14 carbons'), "
               "('O=C\\\\C=C\\\\CCCCCCCCCCCCCCC', 'Long-chain fatty aldehyde "
               "with 18 carbons'), ('O=C/C=C\\\\CCCCCCCCCCCCC', 'Long-chain "
               "fatty aldehyde with 16 carbons'), ('O=CCCC/C=C\\\\CCCCCCCC', "
               "'Long-chain fatty aldehyde with 14 carbons'), "
               "('OC(=O)CCCCCCCCCCCCCCCCCCCCC=O', 'Long-chain fatty aldehyde "
               "with 22 carbons'), ('O=CCCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC', "
               "'Long-chain fatty aldehyde with 18 carbons'), "
               "('O=C(CCCCCCCCCC=C)CC=O', 'Long-chain fatty aldehyde with 14 "
               "carbons'), ('O=CCC\\\\C=C\\\\CCC/C=C\\\\CCCC', 'Long-chain "
               "fatty aldehyde with 14 carbons'), ('O=CCCCCC/C=C\\\\CCCCCCCC', "
               "'Long-chain fatty aldehyde with 16 carbons'), "
               "('O=CC(CCCCCCCCCCCCCCCCCCC)CCCCCCCCC', 'Long-chain fatty "
               "aldehyde with 21 carbons'), ('O=C\\\\C=C\\\\CCCCCCCCCCC', "
               "'Long-chain fatty aldehyde with 14 carbons'), "
               "('O=CCC/C=C\\\\CCCCCCCC', 'Long-chain fatty aldehyde with 13 "
               "carbons'), ('O=CCCCCCCC/C=C\\\\C=C/CCCC', 'Long-chain fatty "
               "aldehyde with 16 carbons'), ('O=CCCCC/C=C/C=C/C=C/C=C/CC', "
               "'Long-chain fatty aldehyde with 15 carbons'), "
               "('O=CCCCCCCCCCC/C=C\\\\CCC', 'Long-chain fatty aldehyde with "
               "16 carbons'), ('O=CCCCCCCCCC/C=C\\\\C=C\\\\CC', 'Long-chain "
               "fatty aldehyde with 16 carbons'), "
               "('C(=O)([H])/C=C/CCCCCCCC/C=C\\\\CCC', 'Long-chain fatty "
               "aldehyde with 16 carbons'), ('O=CCCCCCCCC/C=C\\\\CCCCCCCC', "
               "'Long-chain fatty aldehyde with 19 carbons'), "
               "('O=C\\\\C=C\\\\CCCCCCCCCC', 'Long-chain fatty aldehyde with "
               "13 carbons'), ('O=CCCCCC\\\\C=C\\\\CCCCCCCC', 'Long-chain "
               "fatty aldehyde with 16 carbons'), "
               "('O=CCCCCCC\\\\C=C\\\\CCCCC(CC)C', 'Long-chain fatty aldehyde "
               "with 16 carbons'), ('O=C\\\\C=C\\\\C=C\\\\C\\\\C=C\\\\CCCCC', "
               "'Long-chain fatty aldehyde with 13 carbons'), "
               "('O=CCCCCCCCC/C=C\\\\CCCCC', 'Long-chain fatty aldehyde with "
               "16 carbons'), ('O=CCCCCCCCCC/C=C/C=C/CC', 'Long-chain fatty "
               "aldehyde with 16 carbons'), ('O=CCCCC/C=C/CCC/C=C\\\\CCCC', "
               "'Long-chain fatty aldehyde with 16 carbons'), "
               "('O=CCC(C(C/C=C(/CC/C=C(\\\\CC)/C)\\\\C)C)C', 'Long-chain "
               "fatty aldehyde with 13 carbons'), ('O=CCCCCCCC/C=C/CCCCCC', "
               "'Long-chain fatty aldehyde with 16 carbons'), "
               "('O=CCCCCCCCCCC#CCCCC', 'Long-chain fatty aldehyde with 16 "
               "carbons'), "
               "('[O-]C(=O)CCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC=O', "
               "'Long-chain fatty aldehyde with 20 carbons'), "
               "('O=CCC\\\\C=C\\\\C=C\\\\CCC/C=C\\\\CCCC', 'Long-chain fatty "
               "aldehyde with 16 carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCCCC=O', 'Long-chain fatty "
               "aldehyde with 17 carbons'), ('O=CCCCCCCCCC/C=C\\\\C=C', "
               "'Long-chain fatty aldehyde with 14 carbons'), "
               "('O=CCCCCCCC/C=C\\\\CCCC', 'Long-chain fatty aldehyde with 14 "
               "carbons'), ('O=CC(CCCC(CCCC(CCCC(C)C)C)C)=C', 'Long-chain "
               "fatty aldehyde with 15 carbons'), "
               "('O=CCCCCCC\\\\C=C\\\\CCCC[C@@H](CC)C', 'Long-chain fatty "
               "aldehyde with 16 carbons'), ('O=CCCCCCCCCC/C=C\\\\CC', "
               "'Long-chain fatty aldehyde with 14 carbons'), "
               "('C(\\\\C=C/C=C/CCC)CCCCCCCC([H])=O', 'Long-chain fatty "
               "aldehyde with 16 carbons'), "
               "('C(\\\\CCCCCCCC(=O)O)=C\\\\CCCCCCCC(=O)[H]', 'Long-chain "
               "fatty aldehyde with 18 carbons'), "
               "('O=CCCCCCCCC/C=C/C=C\\\\CCC', 'Long-chain fatty aldehyde with "
               "16 carbons'), ('O=CCCCCCCCCC/C=C/C=C', 'Long-chain fatty "
               "aldehyde with 14 carbons'), ('O=CCCCCCCC/C=C/C/C=C/C/C=C/CC', "
               "'Long-chain fatty aldehyde with 18 carbons')]\n"
               'False negatives: []',
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 96,
    'num_true_negatives': 183815,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02040816326530612,
    'recall': 1.0,
    'f1': 0.039999999999999994,
    'accuracy': 0.9994780140609962}