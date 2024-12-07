"""
Classifies: CHEBI:15904 long-chain fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import FindMolChiralCenters
from collections import deque

def find_longest_carbon_chain(mol):
    """Find the longest continuous carbon chain containing the carboxylic acid group."""
    # Find carboxylic acid carbon
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return []
    
    matches = mol.GetSubstructMatches(carboxylic_pattern)
    carboxylic_carbon = matches[0][0]
    
    # BFS to find longest carbon chain
    visited = set()
    queue = deque([(carboxylic_carbon, [carboxylic_carbon])])
    longest_path = []
    
    while queue:
        current, path = queue.popleft()
        atom = mol.GetAtomWithIdx(current)
        
        for neighbor in atom.GetNeighbors():
            neighbor_idx = neighbor.GetIdx()
            if neighbor_idx not in visited and neighbor.GetSymbol() == 'C':
                new_path = path + [neighbor_idx]
                queue.append((neighbor_idx, new_path))
                if len(new_path) > len(longest_path):
                    longest_path = new_path
                visited.add(neighbor_idx)
    
    return longest_path

def is_long_chain_fatty_acid(smiles: str):
    """
    Determines if a molecule is a long-chain fatty acid (C13-C22).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a long-chain fatty acid, False otherwise
        str: Reason for classification
    """
    # Create RDKit mol object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"
    
    # Find longest carbon chain containing carboxylic acid group
    longest_chain = find_longest_carbon_chain(mol)
    chain_length = len(longest_chain)
    
    if chain_length < 13:
        return False, f"Carbon chain too short (C{chain_length})"
    elif chain_length > 22:
        return False, f"Carbon chain too long (C{chain_length})"
    
    # Check if the carbon chain is the main feature (not part of a larger aromatic/complex system)
    aromatic_pattern = Chem.MolFromSmarts('c1ccccc1')
    complex_ring_pattern = Chem.MolFromSmarts('[R]')
    
    # Get atoms in rings
    ring_atoms = set()
    for ring in mol.GetRingInfo().AtomRings():
        ring_atoms.update(ring)
    
    # Count carbons in longest chain that are part of rings
    chain_ring_atoms = sum(1 for atom_idx in longest_chain if atom_idx in ring_atoms)
    
    # If more than 1/3 of the chain is in rings, it's likely not a fatty acid
    if chain_ring_atoms > len(longest_chain) / 3:
        return False, "Carbon chain is part of a complex ring system"
    
    # Check for peptide bonds which would indicate it's not a fatty acid
    peptide_pattern = Chem.MolFromSmarts('[NX3][CX3](=[OX1])[CX4]')
    if mol.HasSubstructMatch(peptide_pattern):
        return False, "Molecule contains peptide bonds"
    
    return True, f"Long-chain fatty acid with {chain_length} carbons"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15904',
                          'name': 'long-chain fatty acid',
                          'definition': 'A fatty acid with a chain length '
                                        'ranging from C13 to C22.',
                          'parents': ['CHEBI:35366']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.7685774946921445 is too low.\n'
               "True positives: [('OC(=O)CCCC#CCCCCCCC', 'Long-chain fatty "
               "acid with 13 carbons'), ('CCCCCCCCCCCCCCCC(O)CC(O)=O', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C=C/C(O)CCCCCCCC(O)=O', 'Long-chain fatty "
               "acid with 18 carbons'), "
               "('OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCC', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('O=C(CCCCCCCCC)CCCCCC(O)=O', 'Long-chain fatty acid with 16 "
               "carbons'), "
               "('CCCCC[C@@H]1O[C@H]1[C@H](O)\\\\C=C/C\\\\C=C/C\\\\C=C/CCCC(O)=O', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('O[C@@H](CCCCCCCCCCC)CCCC(O)=O', 'Long-chain fatty acid with "
               "16 carbons'), ('O(C(CCCCCCCCCC(O)=O)CCCCCCC)C', 'Long-chain "
               "fatty acid with 19 carbons'), "
               "('O=C(CCCCC)/C=C\\\\C=C\\\\C\\\\C=C\\\\CCCC(O)=O', 'Long-chain "
               "fatty acid with 17 carbons'), ('OC(=O)CCCCCCCCCCCCCCCC(CC)C', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('O1[C@@H]([C@H]([C@@H](O)CC1=O)C/C=C\\\\CCCC(O)=O)/C=C/[C@@H](O)C/C=C\\\\CC', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('CC/C=C\\\\C/C=C\\\\CC(C(CCCCCCCC(O)=O)O)O', 'Long-chain "
               "fatty acid with 18 carbons'), "
               "('OC(=O)CCCCCCCCCCCCCCC.OC(CO)CO', 'Long-chain fatty acid with "
               "19 carbons'), "
               "('O[C@@H](CCCCCC/C=C/[C@H](O)[C@@H](O)[C@H](O)[C@H](N=C(N)N)C(O)=O)CCCCCC', "
               "'Long-chain fatty acid with 21 carbons'), "
               "('O[C@@H](CCCC(O)=O)\\\\C=C/C=C/C=C/C(=O)C/C=C\\\\C=C\\\\[C@@H](O)CC', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('[H]C(\\\\C=C/CCCCCCCC(O)=O)=C1O[C@H]1C\\\\C=C/CC', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('O=C(O)CCCCCCCC/C=C\\\\CC/C=C\\\\CCCCC', 'Long-chain fatty "
               "acid with 20 carbons'), ('OC(CCCCCCCCCC)C(O)CCCCCC(O)=O', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('O=C(CCCCCCCC(O)=O)CCCCCCC', 'Long-chain fatty acid with 16 "
               "carbons'), ('O[C@H](CCCCCCCCCC(O)=O)/C=C/CCCCC', 'Long-chain "
               "fatty acid with 18 carbons'), "
               "('CCCC\\\\C=C\\\\C=C\\\\C=C/CCCCCCCC(O)=O', 'Long-chain fatty "
               "acid with 18 carbons'), "
               "('OC(=O)[C@H](CCCCCCCCCCCCCCCC)C(C(O)=O)=C', 'Long-chain fatty "
               "acid with 21 carbons'), ('CCCCCCCCCCC[C@H](N)C(O)=O', "
               "'Long-chain fatty acid with 13 carbons'), "
               "('OC(=O)CCCCCCCCCCCCCCCCCC(CC)C', 'Long-chain fatty acid with "
               "22 carbons'), ('OC(CCCCCCC/C=C\\\\CCCCCC)CC(O)=O', 'Long-chain "
               "fatty acid with 18 carbons'), ('O=C(CCCCCCCCC)CCCCCCCC(O)=O', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('OC(CCCCCCCCCC)CC(O)=O', 'Long-chain fatty acid with 13 "
               "carbons'), "
               "('C(\\\\C=C\\\\C=C\\\\C([C@@H](O)C/C=C\\\\C/C=C\\\\CC)O)=C\\\\CCCCCC(O)=O', "
               "'Long-chain fatty acid with 22 carbons'), "
               "('OC(CCCC(O)=O)C=CC=CC=CC(O)CC=CCCC(O)=O', 'Long-chain fatty "
               "acid with 18 carbons'), "
               "('CCCCC\\\\C=C/C[C@@H](O)\\\\C=C\\\\C=C/C\\\\C=C/CCCC(O)=O', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('CCCCCCCCC\\\\C=C/CCCCC(O)=O', 'Long-chain fatty acid with 16 "
               "carbons'), "
               "('C(C(O)=O)C/C=C\\\\C/C=C\\\\C\\\\C=C/C=C/[C@@H](C/C=C\\\\C/C=C\\\\CC)O', "
               "'Long-chain fatty acid with 22 carbons'), "
               "('O=C(CCCCCCCCCCCCCCC(O)=O)C', 'Long-chain fatty acid with 17 "
               "carbons'), ('OC(=O)CCCCCCCC#CC#CC#C/C=C/C=C', 'Long-chain "
               "fatty acid with 18 carbons'), ('OCCCCCCCCC/C=C/CCCCC(O)=O', "
               "'Long-chain fatty acid with 16 carbons'), "
               "('OCCCCCCCCCCCCCCC\\\\C=C\\\\C(O)=O', 'Long-chain fatty acid "
               "with 18 carbons'), ('CCCCC\\\\C=C/C\\\\C=C/CCCC(O)=O', "
               "'Long-chain fatty acid with 14 carbons'), "
               "('OC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C=C\\\\1/[C@H](C/C=C\\\\CC)O1)=O', "
               "'Long-chain fatty acid with 22 carbons'), "
               "('OC(=O)C(CCCC(CCCCCCCCC)C)C', 'Long-chain fatty acid with 17 "
               "carbons'), ('OC(=O)CCCCCCCCCC/C=C\\\\C/C=C\\\\CC', 'Long-chain "
               "fatty acid with 18 carbons'), "
               "('CCCCCCCC\\\\C(=C/CCCCCCCC(O)=O)[N+]([O-])=O', 'Long-chain "
               "fatty acid with 18 carbons'), "
               "('O1[C@](C[C@@H](O)[C@H]1CC)([C@@H](O)/C=C/[C@@H](O)CCCCCCCC(O)=O)[H]', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('C(O)(=O)CC/C=C\\\\C[C@H]1[C@H](/C=C/C=C/C=C\\\\C=C\\\\[C@@H](C/C=C\\\\CC)O)O1', "
               "'Long-chain fatty acid with 22 carbons'), "
               "('O1C(C1C(OO)/C=C/CCCCCCCC(O)=O)CCCCC', 'Long-chain fatty acid "
               "with 18 carbons'), ('O=C(O)[C@H](CC(=O)CCCCCCCCCCCCC)C', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('C(CCCCCCCCCC)CCCCCCC(=O)O', 'Long-chain fatty acid with 18 "
               "carbons'), ('O[C@H](CCCCCC)\\\\C=C\\\\CCCCCCCCC(O)=O', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('OCCCCCCCCCC\\\\C=C\\\\C(O)=O', 'Long-chain fatty acid with "
               "13 carbons'), "
               "('O=C(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\[C@H](CCCC)O)O', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('OC(=O)C\\\\C=C\\\\C=C/C=C=CC#CC#C', 'Long-chain fatty acid "
               "with 13 carbons'), "
               "('OC(=O)CCC/C=C\\\\C(/C=C\\\\CCCCCCCCCCC)(C)C', 'Long-chain "
               "fatty acid with 22 carbons'), ('O[C@H](CCCCCCCCCC)CC(O)=O', "
               "'Long-chain fatty acid with 13 carbons'), "
               "('O[C@@H](CCCCCCCC(O)=O)/C=C/[C@H](O)[C@@H](O)C/C=C\\\\CC', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('C(\\\\CC)=C\\\\C/C=C\\\\CC(/C=C/C=C\\\\C/C=C\\\\CCCC(=O)O)O', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('OC(=O)CCC(CCCC(CCCCCCC)C)C', 'Long-chain fatty acid with 17 "
               "carbons'), "
               "('O[C@H](CCCCCCCC(O)=O)\\\\C=C\\\\[C@@H]1[C@H](CC)C(=O)C=C1', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('CCCCCCCC[C@H](OO)\\\\C=C\\\\CCCCCCC(O)=O', 'Long-chain fatty "
               "acid with 18 carbons'), ('OC(CC(O)CCC(O)C)CCCCCCCCC(O)=O', "
               "'Long-chain fatty acid with 16 carbons'), "
               "('OC(=O)CCCCCCCCCCCC(C)(C)C', 'Long-chain fatty acid with 16 "
               "carbons'), ('O[13C](=O)[13CH2][13CH2][13CH2]CCCCCCCCCCCC', "
               "'Long-chain fatty acid with 16 carbons'), "
               "('OC(=O)CCCCCC#CCC#CCCCCCC', 'Long-chain fatty acid with 17 "
               "carbons'), "
               "('C(C(O)=O)C/C=C\\\\C/C=C\\\\C\\\\C=C/C=C/C(C/C=C\\\\C/C=C\\\\CC)O', "
               "'Long-chain fatty acid with 22 carbons'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/CCCC\\\\C=C/CCCC(O)=O', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('OC(=O)CCCC/C=C/C=C/C#CC#C\\\\C=C\\\\C', 'Long-chain fatty "
               "acid with 16 carbons'), ('CCCCCCC#CCCCCCCCCCC(O)=O', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('CCCCCC(=O)CC\\\\C=C/C=C/C=C/[C@@H](O)[C@@H](O)CCCC(O)=O', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('O=C1C(C(=O)N)=CNC(=C1)/C=C\\\\CCCCCCCCC(=O)O', 'Long-chain "
               "fatty acid with 17 carbons'), ('C(CCCCCCC(C)O)CCCCC(O)=O', "
               "'Long-chain fatty acid with 14 carbons'), "
               "('OC(=O)CCCCCC#CCCCCCCCCCC', 'Long-chain fatty acid with 18 "
               "carbons'), "
               "('[H]C(CCCC(O)=O)=CCC([H])=CCC([H])=CC([H])=CCCCCCC', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('CCCCCCC\\\\C=C\\\\C(CCCCCCCC(O)=O)OO', 'Long-chain fatty "
               "acid with 18 carbons'), ('CCCCCCCCCCCCCCC\\\\C=C\\\\C(O)=O', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('C([C@@H](CC)O)C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCC(O)=O', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('OCCCCCCCCCCCCCCCC[C@@H](O)CC(O)=O', 'Long-chain fatty acid "
               "with 19 carbons'), "
               "('O(/C(/CCCCCCC)=C\\\\C=C\\\\C=C\\\\C(O)=O)C(=O)C', "
               "'Long-chain fatty acid with 16 carbons'), "
               "('C(CCC/C=C\\\\C/C=C\\\\CC(/C=C/C=C\\\\CCCCC)=O)(=O)O', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('OC(=O)CCCCCCCCCCCCCCCCCC(O)=O', 'Long-chain fatty acid with "
               "19 carbons'), ('OC(=O)CCC(CCCCCCCCCCCCCC)C', 'Long-chain fatty "
               "acid with 19 carbons'), "
               "('[H]C(CCCC(O)=O)=CCC([H])=CCC([H])=CCC([H])=CCCCCC', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('C(C(/C=C/C=C/C=C\\\\[C@H](CCCC(O)=O)O)=O)/C=C\\\\CCCCCO', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('OC(CCCCC(O)=O)/C=C/C=C/C#CC#CC#CC#C', 'Long-chain fatty acid "
               "with 18 carbons'), ('OC(=O)CC(CC(CCCCCCCC)C)C', 'Long-chain "
               "fatty acid with 15 carbons'), "
               "('CCCCCCCC[C@@H](O)[C@@H](O)CCCCCCCC(O)=O', 'Long-chain fatty "
               "acid with 18 carbons'), "
               "('O[C@H]1[C@@H]([C@@H](C(=O)C1)CC)/C=C/[C@@H](O)C/C=C\\\\C/C=C\\\\C/C=C\\\\CCC(O)=O', "
               "'Long-chain fatty acid with 22 carbons'), "
               "('C(\\\\C=C/CCCCCCCC(=O)O)=C/C(C/C=C\\\\CC)OO', 'Long-chain "
               "fatty acid with 18 carbons'), "
               "('[H]C(CCCCCCCC(O)=O)=CC([H])=CC([H])=CCCCC', 'Long-chain "
               "fatty acid with 18 carbons'), "
               "('OC(=O)\\\\C=C\\\\CC(CCCCCCCC)C', 'Long-chain fatty acid with "
               "14 carbons'), ('C(CCCCCCC/C=C\\\\C=C\\\\C(CCCCC)O)(=O)O', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('OC(=O)CCC/C=C\\\\CCCCCCCC/C=C\\\\CCCC', 'Long-chain fatty "
               "acid with 20 carbons'), "
               "('C(=C/[C@@H](C\\\\C=C/C=C/[C@H](C/C=C\\\\CC)O)O)\\\\C=C\\\\C=C/[C@H](CCC(O)=O)O', "
               "'Long-chain fatty acid with 22 carbons'), "
               "('OC(=O)CC(CCCCCCCCCCCCC)C', 'Long-chain fatty acid with 17 "
               "carbons'), ('OC(CCCCCCCCC(O)=O)CCCCCC(O)=O', 'Long-chain fatty "
               "acid with 16 carbons'), ('OC(=O)CCCCCCCCCC#CCC', 'Long-chain "
               "fatty acid with 14 carbons'), ('O[C@H](CCCCCCCCCC(O)=O)CCC', "
               "'Long-chain fatty acid with 14 carbons'), "
               "('O=C(CCCCCCCCCCCCCCCCC(O)=O)C', 'Long-chain fatty acid with "
               "19 carbons'), ('OC(=O)CCC/C=C/C\\\\C=C\\\\C\\\\C=C\\\\CCCCCC', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('OC(CCCCCCC)/C=C/CCCCCCCC(O)=O', 'Long-chain fatty acid with "
               "18 carbons'), ('OCCCCCCCCCCC\\\\C=C\\\\C(O)=O', 'Long-chain "
               "fatty acid with 14 carbons'), ('OC(=O)C(C(CCCCCCCCCC)C)(C)C', "
               "'Long-chain fatty acid with 16 carbons'), "
               "('ClC(CCCCCCCC)C(Cl)CCCC(O)=O', 'Long-chain fatty acid with 14 "
               "carbons')]\n"
               'False positives: '
               "[('O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)[C@H](O)C)CC2=CC=CC=C2', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('O=C1C(OC(=C1/C=C/C(=O)O)CCC)=C(C)C', 'Long-chain fatty acid "
               "with 13 carbons'), "
               "('CS(=O)(=O)C1=CC=C(C=C1)CN2C3=C(CCCC3CC(=O)O)C4=CC(=CC(=C42)F)F', "
               "'Long-chain fatty acid with 22 carbons'), "
               "('O=C(N[C@@H](CC1=CC=CC=C1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)C', "
               "'Long-chain fatty acid with 16 carbons'), "
               "('OC(=O)C(F)(F)F.[H][C@]12C[C@H](O)CC[C@@]11CCN2Cc2cc(O)c(OC)cc12', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('O[C@H]([C@H](OC(=O)\\\\C=C/c1ccc(O)c(O)c1)C(O)=O)C(O)=O', "
               "'Long-chain fatty acid with 13 carbons'), "
               "('C=1(C=CC(=CC1)[N+]([O-])=O)COP(CCCCCC(O)=O)(=O)O', "
               "'Long-chain fatty acid with 13 carbons'), "
               "('O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)CN)CC2=CC=C(O)C=C2', "
               "'Long-chain fatty acid with 16 carbons'), "
               "('O=C(N[C@@H](CC(=O)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(=O)N)CCCCN', "
               "'Long-chain fatty acid with 15 carbons'), "
               "('O1C(CCCCCCCC(O)=O)=C(C(=C1CCC)C)C', 'Long-chain fatty acid "
               "with 17 carbons'), "
               "('O=C1C=C2[C@@H]3[C@](OC)(CCC[C@H]3/C=C(/C=C(\\\\OC)/C=C/C(=O)O)\\\\C)O[C@H]2[C@@H]4[C@H]1O4', "
               "'Long-chain fatty acid with 22 carbons'), "
               "('[H][C@@]12CCC(=C)[C@H](C[C@H](O)[C@](C)(O)C=C)[C@@]1(C)CCC[C@]2(C)C(O)=O', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('OC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CO)CC(O)=O)[C@H](CC)C', "
               "'Long-chain fatty acid with 13 carbons'), "
               "('O=C(N[C@@H](CCC(O)=O)C(=O)N[C@@H]([C@H](O)C)C(O)=O)[C@@H](N)C(C)C', "
               "'Long-chain fatty acid with 14 carbons'), "
               "('CC(C)C[C@H](NC(=O)[C@@H](N)CC(O)=O)C(=O)N[C@@H](CC(C)C)C(=O)N[C@@H](CO)C(O)=O', "
               "'Long-chain fatty acid with 19 carbons'), "
               "('O=C(N[C@@H](CC=1NC=NC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CCC(=O)N', "
               "'Long-chain fatty acid with 15 carbons'), "
               "('O=C(N[C@@H](CC(C)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=CC=C1)CC(C)C', "
               "'Long-chain fatty acid with 21 carbons'), "
               "('S(CC[C@H](N)C(=O)N[C@H](C(=O)N[C@@H](CC1=CC=C(O)C=C1)C(O)=O)CO)C', "
               "'Long-chain fatty acid with 17 carbons'), "
               "('O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)CN)CC2=CC=CC=C2', "
               "'Long-chain fatty acid with 16 carbons'), "
               "('OC(=O)C(O)=O.CCCCCCCCCOc1ccc2[nH]cc(CCN)c2c1', 'Long-chain "
               "fatty acid with 21 carbons'), "
               "('O=C(N[C@@H](CC=1NC=NC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCCCN)CCCCN', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('S(CC[C@H](NC(=O)[C@@H](N)CC=1NC=NC1)C(=O)N[C@@H](CC=2C=3C(NC2)=CC=CC3)C(O)=O)C', "
               "'Long-chain fatty acid with 22 carbons'), "
               "('SC[C@H](NC(=O)[C@@H](N)CC1=CC=C(O)C=C1)C(=O)NCC(O)=O', "
               "'Long-chain fatty acid with 14 carbons'), "
               "('O=C(N[C@@H](CCCCN)C(O)=O)[C@@H](NC(=O)[C@@H](N)CO)CC(C)C', "
               "'Long-chain fatty acid with 15 carbons'), "
               "('O=C(N[C@@H](CC1=CC=C(O)C=C1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(O)=O)[C@H](CC)C', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('OC1C(C2C(C3C4(C2C(O)=O)CC(CC3)C(C4)=C)(CC1O)C(O)=O)(C)C(O)=O', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('O=C(N[C@@H](CC(O)=O)C(O)=O)[C@H]1N(CCC1)C(=O)[C@@H](N)CC(O)=O', "
               "'Long-chain fatty acid with 13 carbons'), "
               "('O=C(N[C@@H](C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=1NC=NC1)C(C)C', "
               "'Long-chain fatty acid with 14 carbons'), "
               "('O1[C@@H](OC2=CC=C(C3OC=4C(C(=O)C3)=C(O)C=C(O)C4)C=C2)[C@H](O)[C@@H](O)[C@H](O)[C@H]1C(O)=O', "
               "'Long-chain fatty acid with 21 carbons'), "
               "('O=C(N[C@@H](CC1=CC=CC=C1)C(O)=O)[C@@H](NC(=O)CN)CCC(O)=O', "
               "'Long-chain fatty acid with 16 carbons'), "
               "('O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)CC(C)C', "
               "'Long-chain fatty acid with 16 carbons'), "
               "('C1CC(CN(C1)CCC=C(C2=CC=CC=C2)C3=CC=CC=C3)C(=O)O', "
               "'Long-chain fatty acid with 22 carbons'), "
               "('O=C(NCC(O)=O)CCC=1C=2C(NC1)=CC=CC2', 'Long-chain fatty acid "
               "with 13 carbons'), "
               "('O=C(O)[C@H]1N(C(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CCC(=O)N)CC(C)C)C(C)C)CCC1', "
               "'Long-chain fatty acid with 21 carbons'), "
               "('O(CC(COCCCCCC)O)C1=C(C(O)=O)C=CC=C1', 'Long-chain fatty acid "
               "with 16 carbons'), "
               "('O=C1OC2=C(C(=C(C(=O)O)C(=C2COC)O)C)OC3=C1C(=CC(=C3C=O)O)C', "
               "'Long-chain fatty acid with 19 carbons'), "
               "('SC[C@H](NC(=O)[C@@H](N)C)C(=O)N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(O)=O', "
               "'Long-chain fatty acid with 17 carbons'), "
               "('S(CC[C@H](NC(=O)[C@@H](N)CCSC)C(=O)N[C@@H](C(C)C)C(O)=O)C', "
               "'Long-chain fatty acid with 15 carbons'), "
               "('O[C@@H]([C@H](NC(=O)[C@@H](N)CC=1C=2C(NC1)=CC=CC2)C(=O)N[C@@H](CC(=O)N)C(O)=O)C', "
               "'Long-chain fatty acid with 19 carbons'), "
               "('S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=C(O)C=C1)CC(O)=O)C(O)=O)C', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('N[C@@H](CCC(=O)N[C@@H](CSCC(=O)SC[C@H](NC(=O)CC[C@H](N)C(O)=O)C(=O)NCC(O)=O)C(=O)NCC(O)=O)C(O)=O', "
               "'Long-chain fatty acid with 22 carbons'), "
               "('O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC2=CC=C(O)C=C2)[C@H](CC)C', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('OC(=O)CCCC(=O)Nc1ccc(cc1)\\\\C=C\\\\c1ccccc1', 'Long-chain "
               "fatty acid with 19 carbons'), "
               "('O=C1C2=C(O)C3=C(O[C@]4(C)O[C@@]3(C(=O)O)CC4)C=C2C(=O)C=5C1=C(O)C=C(O)C5', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('O=C1O[C@H]2[C@H](O[C@H](C2)CCC(=O)O)C=3C1=C(O)C(OC)=C(OC)C3', "
               "'Long-chain fatty acid with 16 carbons'), "
               "('O(C1=CC(=C(C2=C(NN=C2C)C)C=C1)C(O)=O)C', 'Long-chain fatty "
               "acid with 13 carbons'), "
               "('O[C@@H]([C@H](NC(=O)[C@@H](N)[C@H](O)C)C(=O)N[C@@H](CCC(O)=O)C(O)=O)C', "
               "'Long-chain fatty acid with 13 carbons'), "
               "('O=C(O)C1=CC2=C(O[C@@](CCC=C(C)C)(C)[C@H](C2)O)C=C1', "
               "'Long-chain fatty acid with 17 carbons'), "
               "('O=C1C=2OC3C(=O)C(=C(O)C(C3(C(=O)O)CC2C(=O)C=4C1=C(O)C=CC4)OC)C(=O)C', "
               "'Long-chain fatty acid with 21 carbons'), "
               "('S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CCCCN)CC=1NC=NC1)C(O)=O)C', "
               "'Long-chain fatty acid with 17 carbons'), "
               "('SC[C@H](N)C(=O)N[C@H](C(=O)N[C@@H](CC1=CC=CC=C1)C(O)=O)CO', "
               "'Long-chain fatty acid with 15 carbons'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](CC=1NC=NC1)C(O)=O)[C@H]2NCCC2', "
               "'Long-chain fatty acid with 15 carbons'), "
               "('ClC1=C(O)C=C(/C=C(\\\\NC(=O)[C@@H](NC(=O)C[C@@H](N)CCCCN)C(O)(C)C)/C(=O)O)C=C1O', "
               "'Long-chain fatty acid with 21 carbons'), "
               "('SC[C@H](N)C(=O)N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(=O)N[C@@H]([C@H](CC)C)C(O)=O', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('CSCCC(C(=O)O)NC1=NC=NC2=C1C=C(C=C2)Br', 'Long-chain fatty "
               "acid with 13 carbons'), "
               "('O1[C@@H]([C@H]([C@@H](O)CC1=O)C/C=C\\\\CC(O)=O)/C=C/[C@@H](O)CCCCC', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('S(CC[C@H](N)C(=O)N[C@H](C(=O)N[C@@H]([C@H](CC)C)C(O)=O)CC(O)=O)C', "
               "'Long-chain fatty acid with 15 carbons'), "
               "('N[C@@H](CSC1=CC(=O)C(=O)c2[nH]cc(C[C@H](N)C(O)=O)c12)C(O)=O', "
               "'Long-chain fatty acid with 14 carbons'), "
               "('O=C(N[C@@H]([C@H](O)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=CC=C1)CC(C)C', "
               "'Long-chain fatty acid with 19 carbons'), "
               "('S(CC[C@H](NC(=O)CN)C(=O)N[C@@H](CCCCN)C(O)=O)C', 'Long-chain "
               "fatty acid with 13 carbons'), "
               "('O=C(O)C1=CC(OC2=CC(O)=CC(=C2)C)=CC(=C1)O', 'Long-chain fatty "
               "acid with 14 carbons'), "
               "('O=C(N[C@@H](C(C)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)C)CC=1C=2C(NC1)=CC=CC2', "
               "'Long-chain fatty acid with 19 carbons'), "
               "('O=C1C2=C(O[C@@H](C3=C1C=CC=C3OC/C=C(/C(=O)O)\\\\C)OC)C=C(C)C=C2O', "
               "'Long-chain fatty acid with 21 carbons'), "
               "('OC(=O)[C@@H](NC(=O)CNC(=O)[C@@H](N)C(C)C)CC(C)C', "
               "'Long-chain fatty acid with 13 carbons'), "
               "('C(=O)([C@@H](N)CCSC)N[C@H](C(=O)N[C@H](C(=O)O)CC(O)=O)CC1=CNC2=C1C=CC=C2', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('C[C@@H](O)[C@H](NC(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12)C(O)=O', "
               "'Long-chain fatty acid with 15 carbons'), "
               "('O=C(O)C=C(C=C[C@@]1(O)C(=C[C@@H](O)C[C@H]1C)C)C', "
               "'Long-chain fatty acid with 14 carbons'), "
               "('O=C(O)/C(=C/[C@H]1C=C(CC[C@@H]1C(C)C)COC(=O)C)/COC(=O)C', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('O=C(N[C@@H](C(C)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)C)CC1=CC=CC=C1', "
               "'Long-chain fatty acid with 17 carbons'), "
               "('O(C(CCCCC(C)C)CC(=O)NC(CO)C(O)=O)C(=O)CC(O)CCC(CC)C', "
               "'Long-chain fatty acid with 22 carbons'), "
               "('O=C(N[C@@H](C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CO)CC=1C=2C(NC1)=CC=CC2', "
               "'Long-chain fatty acid with 17 carbons'), "
               "('S(CC[C@H](NC(=O)[C@@H](N)CO)C(=O)N[C@@H](CC=1NC=NC1)C(O)=O)C', "
               "'Long-chain fatty acid with 14 carbons'), "
               "('S(CC[C@H](N)C(=O)N1[C@@H](CCC1)C(=O)N[C@@H](CC(C)C)C(O)=O)C', "
               "'Long-chain fatty acid with 16 carbons'), "
               "('S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CC=1NC=NC1)C(O)=O)C', "
               "'Long-chain fatty acid with 15 carbons'), "
               "('O=C(N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(=O)NCC(O)=O)[C@@H](N)CCCCN', "
               "'Long-chain fatty acid with 19 carbons'), "
               "('O=C1C2=C(C(=O)O)C=CC(=C2CC1)C3=C4C(=C(C(=O)O)C=C3)C(=O)CC4', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('SC[C@H](NC(=O)[C@@H](N)CC=1NC=NC1)C(=O)N[C@@H](CC=2NC=NC2)C(O)=O', "
               "'Long-chain fatty acid with 15 carbons'), "
               "('O1[C@@]2(N(C[C@@H]1CC(O)C(NC(=O)C(N)C(C)C)C(O)=O)C(=O)C2)[H]', "
               "'Long-chain fatty acid with 14 carbons'), "
               "('O=C(N[C@@H](CC1=CC=CC=C1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)CCC(O)=O', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('S(CC[C@H](NC(=O)[C@@H](N)CO)C(=O)N[C@@H](CC1=CC=CC=C1)C(O)=O)C', "
               "'Long-chain fatty acid with 17 carbons'), "
               "('O=C(N[C@@H](CCC(O)=O)C(=O)N[C@@H](CC1=CC=C(O)C=C1)C(O)=O)[C@@H](N)CCCCN', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)[C@H](O)C)[C@H](O)C', "
               "'Long-chain fatty acid with 13 carbons'), "
               "('S(CC[C@H](N)C(=O)N[C@@H](CC=1NC=NC1)C(=O)N[C@@H](C(C)C)C(O)=O)C', "
               "'Long-chain fatty acid with 16 carbons'), "
               "('O=C(N1[C@@H](CCC1)C(=O)N[C@@H](CC(=O)N)C(O)=O)[C@@H](N)CC=2C=3C(NC2)=CC=CC3', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('OC(=O)[C@H](Cc1ccccc1)NC(=O)[C@@H]1CCCN1', 'Long-chain fatty "
               "acid with 14 carbons'), "
               "('S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CCCN=C(N)N)C)C(O)=O)C', "
               "'Long-chain fatty acid with 14 carbons'), "
               "('O=C(N[C@@H](C(C)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)CC1=CC=CC=C1', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('S(CC[C@H](NC(=O)[C@H]1N(CCC1)C(=O)[C@@H](N)CCC(O)=O)C(O)=O)C', "
               "'Long-chain fatty acid with 15 carbons'), "
               "('O=C1C2=C(O)C(O)=C(O)C=C2C(=O)C=3C1=C(O)C=C(C(=O)O)C3', "
               "'Long-chain fatty acid with 15 carbons'), "
               "('ClC[C@@]1(O)[C@@H](C=C)[C@H]2[C@@H]([C@@]3([C@](O)([C@@](C(=O)O)([C@H](O)CC3)C)CC2)C)CC1', "
               "'Long-chain fatty acid with 20 carbons'), "
               "('COc1c(N2CCN[C@@H](C)C2)c(F)cc2c1n(cc(C(O)=O)c2=O)C1CC1', "
               "'Long-chain fatty acid with 19 carbons'), "
               "('C[N+](C)(C)[C@@H](CCc1nc(C[C@H](N-*)C(-*)=O)c[nH]1)C(O)=O', "
               "'Long-chain fatty acid with 13 carbons'), "
               "('Cl/C(/C=1OC2=C(C(O)=CC(=C2)C)C(C1CC(=O)OC)=O)=C/C(=O)O', "
               "'Long-chain fatty acid with 16 carbons'), "
               "('O=C(N[C@@H](CCC(O)=O)C(O)=O)[C@@H](NC(=O)[C@@H](N)CO)C(C)C', "
               "'Long-chain fatty acid with 13 carbons'), "
               "('S1C(=NC(=C1)C2=NC(C(=O)O)=CC(=C2OC)OC)CCCCC[C@@H](O)C', "
               "'Long-chain fatty acid with 18 carbons'), "
               "('O=C1OC(CCCC[C@@H]2[C@H]3C1=C(O[C@@H]3CCC2=O)/C=C/C=C/C=C/C(=O)O)C', "
               "'Long-chain fatty acid with 22 carbons'), "
               "('CCOC(=O)C1=CC=C(C=C1)NN=C2C=CC(=O)C(=C2)CC(=O)O', "
               "'Long-chain fatty acid with 17 carbons'), "
               "('C[C@@H](OP(O)(=O)OC[C@@H](O)[C@@H](O)[C@@H](O)Cn1c2cc(C)c(C)cc2nc2c1nc(=O)[nH]c2=O)[C@H](N)C(O)=O', "
               "'Long-chain fatty acid with 21 carbons'), "
               "('C1(=CC(=C(C(=C1)OC)/C=C/S(CC2=CC=C(C(=C2)NCC(O)=O)OC)(=O)=O)OC)OC', "
               "'Long-chain fatty acid with 21 carbons'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](CC1=CC=CC=C1)C(O)=O)[C@H]2NCCC2', "
               "'Long-chain fatty acid with 18 carbons')]\n"
               'False negatives: '
               "[('O=C(O)C[C@@H](O)/C=C/C=C/C=C/[C@H]([C@@H](O)[C@@H](C[C@H]([C@H](O)CC(=O)C1=CC=C(NC)C=C1)C)C)C', "
               "'Carbon chain too long (C27)'), "
               "('O=C(O)/C(=C\\\\C)/CCCCCCCCC\\\\C=C/C=C/CC1=CC(O)=CC(=C1)O', "
               "'Carbon chain too long (C24)'), "
               "('O=C1C(C(CC1)CC(OC)=O)C/C=C\\\\CC', 'No carboxylic acid group "
               "found'), ('O=C1C(OC)=CC(=O)C(=C1CCCCCCCCCCCCCC/C=C/C(=O)O)O', "
               "'Carbon chain too long (C24)'), "
               "('O=C(O)C[C@H](OC)\\\\C=C/C=C/C=C\\\\C=C\\\\C=C/[C@@H]([C@H](O)[C@@H]([C@H]1O[C@]2(O[C@@H]([C@H](C)[C@@H](C2)OC)[C@@H]([C@@H](O)[C@H](C/C(=C/CC)/C)C)C)[C@H](O)C[C@@H]1C)C)C', "
               "'Carbon chain too long (C42)'), "
               "('N[C@H](C(=O)O)CS[C@H](/C=C/C=C/C=C\\\\C/C=C\\\\CCC(O)=O)[C@H](C/C=C\\\\C/C=C\\\\CC)O', "
               "'Carbon chain too long (C25)'), "
               "('O1C(CCCCCCCCCCCCC(O)=O)=C(C=C1CCCCC)C', 'Carbon chain too "
               "long (C23)'), "
               "('S(C(=O)CCCCC[C@@H]1[C@@H](C(C=C1)=O)C/C=C\\\\CC)CCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]2O[C@@H](N3C4=C(C(=NC=N4)N)N=C3)[C@@H]([C@@H]2OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O', "
               "'No carboxylic acid group found'), "
               "('C(\\\\CC=CC=CC=C[C@@H]([C@@H](C/C=C\\\\CC)O)SC[C@H](N)C(=O)NCC(=O)O)=C\\\\C/C=C\\\\CCC(O)=O', "
               "'Carbon chain too long (C27)')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 185,
    'num_false_positives': 100,
    'num_true_negatives': 17294,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.6491228070175439,
    'recall': 0.9736842105263158,
    'f1': 0.7789473684210527,
    'accuracy': 0.9940286624203821}