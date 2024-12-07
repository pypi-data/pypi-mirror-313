"""
Classifies: CHEBI:194321 hydroperoxy unsaturated fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_hydroperoxy_unsaturated_fatty_acid(smiles: str):
    """
    Determines if a molecule is a hydroperoxy unsaturated fatty acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydroperoxy unsaturated fatty acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
    
    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"
        
    # Check for hydroperoxy group(s)
    hydroperoxy_pattern = Chem.MolFromSmarts('[OX2][OX2H]')
    hydroperoxy_matches = mol.GetSubstructMatches(hydroperoxy_pattern)
    if not hydroperoxy_matches:
        return False, "No hydroperoxy group found"
    
    # Check for double bonds
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    double_bond_matches = mol.GetSubstructMatches(double_bond_pattern)
    if not double_bond_matches:
        return False, "No carbon-carbon double bonds found"

    # Count carbons in the main chain
    def get_main_chain_length():
        # Create a copy of the molecule
        mol_copy = Chem.RWMol(mol)
        
        # Remove hydroperoxy groups to simplify chain finding
        for match in reversed(mol.GetSubstructMatches(hydroperoxy_pattern)):
            mol_copy.RemoveAtom(match[1])  # Remove -OH
            mol_copy.RemoveAtom(match[0])  # Remove -O-
            
        # Find carboxylic carbon
        carb_matches = mol_copy.GetSubstructMatches(carboxylic_pattern)
        if not carb_matches:
            return 0
        start_idx = carb_matches[0][0]
        
        # BFS to find longest chain
        visited = set()
        queue = [(start_idx, [start_idx])]
        longest_path = []
        
        while queue:
            current_idx, path = queue.pop(0)
            current_atom = mol_copy.GetAtomWithIdx(current_idx)
            
            if len(path) > len(longest_path):
                longest_path = path
                
            for neighbor in current_atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C' and neighbor.GetIdx() not in visited:
                    visited.add(neighbor.GetIdx())
                    new_path = path + [neighbor.GetIdx()]
                    queue.append((neighbor.GetIdx(), new_path))
                    
        return len(longest_path)

    chain_length = get_main_chain_length()
    if chain_length < 16:
        return False, f"Carbon chain too short ({chain_length} carbons)"

    # Check for cyclic structures (excluding prostaglandin-like structures)
    ring_info = mol.GetRingInfo()
    if ring_info.NumRings() > 0:
        ring_sizes = [len(ring) for ring in ring_info.AtomRings()]
        if any(size > 6 for size in ring_sizes):
            return False, "Contains large ring structures"
        if any(size == 6 for size in ring_sizes):
            atoms_in_6_ring = next(ring for ring in ring_info.AtomRings() if len(ring) == 6)
            atoms = [mol.GetAtomWithIdx(i) for i in atoms_in_6_ring]
            if any(atom.GetIsAromatic() for atom in atoms):
                return False, "Contains aromatic rings"

    # Count number of hydroperoxy groups and double bonds
    num_hydroperoxy = len(hydroperoxy_matches)
    num_double_bonds = len(double_bond_matches)
    
    # Check for double bond minimum
    if num_double_bonds < 1:
        return False, "Insufficient number of double bonds"

    # Check for peroxide bridges (endoperoxides)
    peroxide_bridge_pattern = Chem.MolFromSmarts('[C,O]OO[C,O]')
    if mol.HasSubstructMatch(peroxide_bridge_pattern):
        return False, "Contains peroxide bridge"

    return True, f"Found {num_hydroperoxy} hydroperoxy group(s), {num_double_bonds} double bond(s), carbon chain length {chain_length}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:194321',
                          'name': 'hydroperoxy unsaturated fatty acid',
                          'definition': 'Any unsaturated fatty acid carrying '
                                        'one or more hydroperoxy substituents.',
                          'parents': ['CHEBI:27208', 'CHEBI:64009']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.5499999999999999 is too low.\n'
               'True positives: '
               "[('C(CCC(O)=O)CCC/C=C\\\\C/C=C\\\\C=C\\\\[C@H](CCCCC)OO', "
               "'Found 1 hydroperoxy group(s), 3 double bond(s), carbon chain "
               "length 20'), "
               "('CCCCC\\\\C=C/C[C@@H](OO)\\\\C=C\\\\C=C/CCCCC(O)=O', 'Found 1 "
               'hydroperoxy group(s), 3 double bond(s), carbon chain length '
               "18'), "
               "('CCCCC\\\\C=C/C[C@@H](OO)\\\\C=C\\\\C=C/C\\\\C=C/CCCC(O)=O', "
               "'Found 1 hydroperoxy group(s), 4 double bond(s), carbon chain "
               "length 20'), "
               "('OC(CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C=C\\\\[C@H](C/C=C\\\\CC)OO)=O', "
               "'Found 1 hydroperoxy group(s), 5 double bond(s), carbon chain "
               "length 22'), ('CCCCC[C@H](OO)\\\\C=C\\\\C=C/CCCCCCCC(O)=O', "
               "'Found 1 hydroperoxy group(s), 2 double bond(s), carbon chain "
               "length 18'), "
               "('C(C[C@H]1[C@@H]2C[C@H]([C@@H]1/C=C/[C@H](CCCCC)OO)OO2)CCCCC(O)=O', "
               "'Found 1 hydroperoxy group(s), 1 double bond(s), carbon chain "
               "length 17'), "
               "('C(CCCCCCC[C@@H](/C=C/C=C\\\\C=C\\\\[C@H](CC)OO)OO)(O)=O', "
               "'Found 2 hydroperoxy group(s), 3 double bond(s), carbon chain "
               "length 18'), "
               "('C(/C=C\\\\C=C/C(C/C=C\\\\C/C=C\\\\CCC(O)=O)OO)=C\\\\[C@H](CCCCC)OO', "
               "'Found 2 hydroperoxy group(s), 5 double bond(s), carbon chain "
               "length 22'), "
               "('C(\\\\CC)=C\\\\C/C=C\\\\C/C=C\\\\C=C\\\\C(C/C=C\\\\CCCC(=O)O)OO', "
               "'Found 1 hydroperoxy group(s), 5 double bond(s), carbon chain "
               "length 20'), "
               "('O(O)C(C/C=C\\\\C/C=C\\\\CCCC(O)=O)/C=C/C=C\\\\CCCCC', 'Found "
               '1 hydroperoxy group(s), 4 double bond(s), carbon chain length '
               "20'), "
               "('OC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C=C\\\\[C@H](C/C=C\\\\CC)OO)=O', "
               "'Found 1 hydroperoxy group(s), 6 double bond(s), carbon chain "
               "length 22')]\n"
               'False positives: '
               "[('O(O)C(CCCCC)/C=C/C=C\\\\C/C=C\\\\CCCCCCC(O)=O', 'Found 1 "
               'hydroperoxy group(s), 3 double bond(s), carbon chain length '
               "20'), "
               "('O[C@@H]1[C@@H]([C@H](C(=O)C1)/C=C/[C@@H](OO)CCCCC)C/C=C\\\\CCCC(O)=O', "
               "'Found 1 hydroperoxy group(s), 2 double bond(s), carbon chain "
               "length 17'), "
               "('O[C@H]1[C@@H]([C@H](C(=O)C1)C/C=C\\\\CCCC(O)=O)/C=C/[C@@H](OO)CCCCC', "
               "'Found 1 hydroperoxy group(s), 2 double bond(s), carbon chain "
               "length 17'), ('O(O)C(=CC=CCCCCCCCCCCCCCCC)C(O)=O', 'Found 1 "
               'hydroperoxy group(s), 2 double bond(s), carbon chain length '
               "20'), ('C(CCCCCCCC(/C=C/C1C(CCCCC)O1)OO)(=O)O', 'Found 1 "
               'hydroperoxy group(s), 1 double bond(s), carbon chain length '
               "18'), ('O(O)C(CCCCCCCCCC(O)=O)/C=C\\\\CCCCC', 'Found 1 "
               'hydroperoxy group(s), 1 double bond(s), carbon chain length '
               "18'), "
               "('CCCCC[C@H](OO)\\\\C=C\\\\[C@H]1[C@H]2C[C@H](OO2)[C@@H]1C\\\\C=C/CCCC(O)=O', "
               "'Found 1 hydroperoxy group(s), 2 double bond(s), carbon chain "
               "length 17'), ('O(O)[C@H](CCCCCCCCCC(O)=O)/C=C\\\\CCCCC', "
               "'Found 1 hydroperoxy group(s), 1 double bond(s), carbon chain "
               "length 18'), ('O1C(C1C(OO)/C=C/CCCCCCCC(O)=O)CCCCC', 'Found 1 "
               'hydroperoxy group(s), 1 double bond(s), carbon chain length '
               "18'), ('O(O)C(CCCCCCC(O)=O)/C=C\\\\CCCCCCCC', 'Found 1 "
               'hydroperoxy group(s), 1 double bond(s), carbon chain length '
               "18'), "
               "('O1OC(CC1C(OO)C/C=C\\\\CCC(O)=O)/C=C/C=C/C/C=C\\\\C/C=C\\\\CC', "
               "'Found 1 hydroperoxy group(s), 5 double bond(s), carbon chain "
               "length 22'), ('O(O)[C@H](CCCCCCC(O)=O)/C=C\\\\CCCCCCCC', "
               "'Found 1 hydroperoxy group(s), 1 double bond(s), carbon chain "
               "length 18'), "
               "('O1O[C@]2([C@@H]([C@@H]([C@@]1(C2)[H])CCC(O)=O)/C=C/[C@@H](OO)C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)[H]', "
               "'Found 1 hydroperoxy group(s), 4 double bond(s), carbon chain "
               "length 19'), ('OC(CCCCCCCC(O)=O)C(O)/C=C/C(OO)CCCCC', 'Found 1 "
               'hydroperoxy group(s), 1 double bond(s), carbon chain length '
               "18'), ('OC(CCCCC)C(O)\\\\C=C\\\\C(OO)CCCCCCCC(O)=O', 'Found 1 "
               'hydroperoxy group(s), 1 double bond(s), carbon chain length '
               "18'), ('O(O)CCCCCCCCCCCCC/C=C/C=C/C(O)=O', 'Found 1 "
               'hydroperoxy group(s), 2 double bond(s), carbon chain length '
               "18'), ('O(O)[C@H](CCCCC)\\\\C=C\\\\CCCCCCCCCC(O)=O', 'Found 1 "
               'hydroperoxy group(s), 1 double bond(s), carbon chain length '
               "18'), "
               "('O1O[C@@]2([C@H]([C@H]([C@]1(C2)[H])C/C=C\\\\CC)/C=C/[C@@H](OO)C/C=C\\\\C/C=C\\\\CCC(O)=O)[H]', "
               "'Found 1 hydroperoxy group(s), 4 double bond(s), carbon chain "
               "length 19')]\n"
               'False negatives: []',
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 10,
    'num_false_positives': 15,
    'num_true_negatives': 183804,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.4,
    'recall': 0.9090909090909091,
    'f1': 0.5555555555555556,
    'accuracy': 0.9999129630637001}