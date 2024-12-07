"""
Classifies: CHEBI:167098 N-(fatty acyl)-ethanolamine
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_N__fatty_acyl__ethanolamine(smiles: str):
    """
    Determines if a molecule is an N-(fatty acyl)-ethanolamine.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an N-(fatty acyl)-ethanolamine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for ethanolamine part (-NCCO)
    ethanolamine_pattern = Chem.MolFromSmarts('[NH]-[CH2]-[CH2]-[OH]')
    if not mol.HasSubstructMatch(ethanolamine_pattern):
        return False, "Missing ethanolamine (-NCCO) group"
        
    # Check for amide group connected to ethanolamine
    amide_ethanolamine_pattern = Chem.MolFromSmarts('[C](=O)-[NH]-[CH2]-[CH2]-[OH]')
    if not mol.HasSubstructMatch(amide_ethanolamine_pattern):
        return False, "Missing amide group connected to ethanolamine"

    # For wildcards (*), we'll return True as they could represent valid fatty acid chains
    if '*' in smiles:
        return True, "Valid N-(fatty acyl)-ethanolamine structure with unspecified chain"

    # Get the atoms in the ethanolamine-amide match
    match_atoms = mol.GetSubstructMatch(amide_ethanolamine_pattern)
    if not match_atoms:
        return False, "Could not identify key structural elements"

    # The first atom (carbonyl carbon) in the match is our starting point
    carbonyl_idx = match_atoms[0]
    carbonyl_atom = mol.GetAtomWithIdx(carbonyl_idx)

    # Check the number of non-hydrogen atoms in the molecule
    if len(mol.GetAtoms()) > 50:  # If molecule is too complex, likely a peptide or other structure
        return False, "Structure too complex for a simple fatty acyl chain"

    # Look at neighbors of the carbonyl carbon (excluding the amide nitrogen)
    carbon_chain = []
    visited = set([carbonyl_idx, match_atoms[1]])  # carbonyl C and amide N
    
    def trace_aliphatic_chain(atom, visited):
        chain = []
        stack = [(atom, [])]
        while stack:
            current, path = stack.pop()
            if current.GetIdx() not in visited:
                visited.add(current.GetIdx())
                if current.GetSymbol() == 'C':
                    chain.extend(path + [current])
                    for neighbor in current.GetNeighbors():
                        if neighbor.GetIdx() not in visited and neighbor.GetSymbol() == 'C':
                            stack.append((neighbor, path + [current]))
        return chain

    # Start tracing from carbonyl carbon neighbors
    for neighbor in carbonyl_atom.GetNeighbors():
        if neighbor.GetIdx() not in visited and neighbor.GetSymbol() == 'C':
            carbon_chain.extend(trace_aliphatic_chain(neighbor, visited.copy()))

    # Count carbons in the aliphatic chain
    carbon_count = len(carbon_chain)
    
    # Count double bonds in the chain
    double_bond_count = 0
    for atom in carbon_chain:
        for bond in atom.GetBonds():
            if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                double_bond_count += 1
    double_bond_count = double_bond_count // 2  # Each double bond is counted twice

    # Should have at least 2 carbons in chain (not counting the carbonyl carbon)
    if carbon_count < 2:
        return False, "Acyl chain too short to be considered a fatty acyl"

    # Check if the chain is primarily aliphatic
    if len([a for a in carbon_chain if a.GetIsAromatic()]) > 0:
        return False, "Chain contains aromatic carbons"

    # Check if there are too many heteroatoms in the chain
    heteroatom_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() not in ['C', 'H'])
    if heteroatom_count > 4:  # allowing for N, O in ethanolamine and C=O in amide
        return False, "Too many heteroatoms for a fatty acyl chain"

    chain_description = f"N-(fatty acyl)-ethanolamine with fatty acyl chain with {carbon_count} carbons"
    if double_bond_count > 0:
        chain_description += f" and {double_bond_count} double bonds"
    
    return True, chain_description


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:167098',
                          'name': 'N-(fatty acyl)-ethanolamine',
                          'definition': 'an N-acyl-ethanolamine where the acyl '
                                        'group is a fatty acyl chain with '
                                        'composition not specified, major '
                                        'species at pH 7.3.',
                          'parents': ['CHEBI:29348', 'CHEBI:52640']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.1515151515151515 is too low.\n'
               "True positives: [('CCCCCC=CCC=CCC=CCCCCCCC(=O)NCCO', 'N-(fatty "
               'acyl)-ethanolamine with fatty acyl chain with 190 carbons and '
               "28 double bonds'), ('N(C(*)=O)CCO', 'Valid N-(fatty "
               "acyl)-ethanolamine structure with unspecified chain'), "
               "('N(C(*)=O)CCO', 'Valid N-(fatty acyl)-ethanolamine structure "
               "with unspecified chain'), ('CCCCCC(=O)NCCO', 'N-(fatty "
               "acyl)-ethanolamine with fatty acyl chain with 15 carbons'), "
               "('CCCC(=O)NCCO', 'N-(fatty acyl)-ethanolamine with fatty acyl "
               "chain with 6 carbons')]\n"
               'False positives: '
               "[('O=C1O[C@@H]([C@H](NC(=O)[C@@H](NC(=O)/C(=C/C)/C)CCC(=O)N)C(=O)N[C@H](C(=O)N[C@H]2CC[C@H](N([C@H](C(N([C@H](C(N[C@H]1C)=O)CC3=CC=C(O)C=C3)C)=O)CC4=CC=CC=C4)C2=O)OC)CCC(=O)NCCO)C', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 10 "
               "carbons'), "
               "('O=C(N1[C@H](C(=O)N[C@H](C(=O)NC([C@@H](O)C(=O)NCCC(=O)N[C@H](C(=O)NC(C(=O)NCCC(=O)N[C@H](C(=O)NC(C(=O)NC(C(=O)N[C@H](C(=O)NCCC(=O)NCCO)CC(C)C)(C)C)(C)C)CC(C)C)(C)C)CC(C)C)(C)C)C)CCC1)[C@](NC(=O)[C@@H](NC(=O)C(NC(=O)C(NC(=O)[C@@H](NC(=O)[C@H]2N(C(=O)C(NC(=O)C)(C)C)CCC2)C)(C)C)(C)C)CC3=CC=CC=C3)(CC)C', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 3 "
               "carbons'), ('O=C(NCCO)/C(=C/CC/C=C/CCCCCCCCCCCCC)/C', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 192 "
               "carbons and 33 double bonds'), "
               "('CCCCC[C@H](O)\\\\C=C\\\\[C@H]1[C@@H](O)C[C@H](O)[C@@H]1C\\\\C=C/CCCC(=O)NCCO', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 166 "
               "carbons and 23 double bonds'), ('OC(C(=O)NCCO)C', 'N-(fatty "
               "acyl)-ethanolamine with fatty acyl chain with 3 carbons'), "
               "('OC(C(O)C/C=C\\\\C/C=C\\\\CCCC(=O)NCCO)C/C=C\\\\CCCCC', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 190 "
               "carbons and 34 double bonds'), "
               "('C[C@@H](NC(=O)[C@@H](N)Cc1ccc(O)cc1)C(=O)NCC(=O)N(C)[C@@H](Cc1ccccc1)C(=O)NCCO', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 3 "
               "carbons'), "
               "('O[C@@H]1[C@H]([C@H]([C@H](O)C1)/C=C/[C@@H](O)CCCCC)C/C=C\\\\CCCC(=O)NCCO', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 166 "
               "carbons and 23 double bonds'), "
               "('O=C(NCCO)CCCCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC', 'N-(fatty "
               'acyl)-ethanolamine with fatty acyl chain with 190 carbons and '
               "19 double bonds'), "
               "('OC(CCCCC)/C=C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCC(=O)NCCO', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 190 "
               "carbons and 45 double bonds'), "
               "('S(CC[C@@H]1NC(=O)[C@H]2N(C(=O)[C@@H](NC(=O)C3=CC=CC=C3)CNC(=O)[C@@H](CCC(=O)N)NC(\\\\C(\\\\NC([C@H](NC(C1=O)=O)CCC(=O)NCCO)=O)=C\\\\C=4C5=C(C=CC=C5)NC4)=O)CCC2)C', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 10 "
               "carbons'), "
               "('O[C@H]1[C@@H]([C@@H](CCCCCCC(=O)NCCO)C(=O)C1)/C=C/[C@@H](O)CCCCC', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 190 "
               "carbons and 13 double bonds'), ('N(C(*)=O)(CCO)[H]', 'Valid "
               'N-(fatty acyl)-ethanolamine structure with unspecified '
               "chain'), "
               "('O/1[C@@]2([C@@]([C@H]([C@H](O)C2)/C=C/[C@@H](O)CCCCC)(C\\\\C1=C\\\\CCCC(=O)NCCO)[H])[H]', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 166 "
               "carbons and 23 double bonds'), "
               "('O1[C@@H]([C@@H]1C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCC(=O)NCCO)CCCCC', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 190 "
               "carbons and 37 double bonds'), "
               "('O=C(N1[C@H](C(=O)N[C@H](C(=O)NC([C@@H](O)C(=O)NCCC(=O)N[C@H](C(=O)N[C@@](C(=O)NCCC(=O)N[C@H](C(=O)NC(C(=O)NC(C(=O)N[C@H](C(=O)NCCC(=O)NCCO)CC(C)C)(C)C)(C)C)CC(C)C)(CC)C)CC(C)C)(C)C)C)CCC1)[C@](NC(=O)[C@@H](NC(=O)C(NC(=O)C(NC(=O)[C@@H](NC(=O)[C@H]2N(C(=O)C(NC(=O)C)(C)C)CCC2)C)(C)C)(C)C)CC3=CC=CC=C3)(CC)C', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 3 "
               "carbons'), "
               "('O=C(NCCO)CCC/C(=C(\\\\C/C(=C(\\\\C/C(=C(\\\\C/C(=C(\\\\CCCCC)/[2H])/[2H])/[2H])/[2H])/[2H])/[2H])/[2H])/[2H]', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 190 "
               "carbons and 44 double bonds'), "
               "('S(CC[C@@H]1NC(=O)[C@H]2N(C(=O)[C@@H](NC(=O)C3=CC=CC=C3)CNC(=O)[C@@H](CCC(=O)N)NC(\\\\C(\\\\NC([C@H](NC(C1=O)=O)C[C@H](O)C(=O)NCCO)=O)=C\\\\C=4C5=C(C=CC=C5)NC4)=O)CCC2)C', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 10 "
               "carbons'), "
               "('C1[C@H]([C@@H]([C@@H](C/C=C\\\\CCCC(NCCO)=O)C1=O)/C=C/[C@H](CCCCC)O)O', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 190 "
               "carbons and 29 double bonds'), "
               "('O=C(NCCO)CCCCCCCCCCC/C=C\\\\CCCCCCCC', 'N-(fatty "
               'acyl)-ethanolamine with fatty acyl chain with 231 carbons and '
               "9 double bonds'), ('C(C(NCCO)=O)(C)C1=CC=C(C=C1)CC(C)C', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 3 "
               "carbons'), ('O=C(NCCO)CCCCCCCCCCCCCCCCCCCCCC', 'N-(fatty "
               "acyl)-ethanolamine with fatty acyl chain with 253 carbons'), "
               "('OC(CCCCC)C(O)C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCC(=O)NCCO', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 190 "
               "carbons and 37 double bonds'), ('S(\\\\C=C\\\\C(=O)NCCO)C', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 3 "
               "carbons and 1 double bonds'), "
               "('[C@@H]1([C@@H](C[C@H]([C@@H](O1)C)O)O)O[C@@H](CCCCCCCCCCCCCCCCCCCCCCC(CC(=O)NCCO)=O)C', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 351 "
               "carbons and 12 double bonds'), ('C(=CC(NCCO)=O)C1=CC=CC=C1', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 3 "
               "carbons and 1 double bonds'), "
               "('O[C@@H]1[C@@H]([C@H]([C@H](O)C1)/C=C/[C@@H](O)CCCCC)C/C=C/CCCC(NCCO)=O', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 166 "
               "carbons and 23 double bonds'), ('OC(C(O)C(O)C(=O)NCCO)C(O)CO', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 15 "
               "carbons'), "
               "('O=C1O[C@@H]([C@H](NC(=O)[C@@H](NC(=O)/C(=C/C)/C)CCC(=O)N)C(=O)N[C@H](C(=O)N2[C@H](OC)CC[C@H]2C(N[C@H](C(N([C@H](C(N[C@H]1C)=O)CC3=CC=C(O)C=C3)C)=O)CC4=CC=CC=C4)=O)CCC(=O)NCCO)C', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 10 "
               "carbons'), "
               "('OC(CCCC(=O)NCCO)C(O)C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 190 "
               "carbons and 28 double bonds'), "
               "('O1[C@H]([C@H]1C/C=C\\\\C/C=C\\\\CCCCC)C/C=C\\\\CCCC(=O)NCCO', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 190 "
               "carbons and 31 double bonds'), "
               "('O[C@@H](CCCC(=O)NCCO)\\\\C=C/C=C/C=C/[C@H](O)C/C=C\\\\CCCCC', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 190 "
               "carbons and 44 double bonds'), "
               "('OCCNC(=O)CCCCC(NCCCC[C@@H](C(=O)*)N*)=O', 'Valid N-(fatty "
               "acyl)-ethanolamine structure with unspecified chain'), "
               "('O=C(O)\\\\C(\\\\C1=CC=CC=C1)=C/2\\\\OCO\\\\C2=C(/C3=CC=CC=C3)\\\\C(=O)NCCO', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 15 "
               "carbons and 7 double bonds'), "
               "('O=C(NCCO)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC', 'N-(fatty "
               'acyl)-ethanolamine with fatty acyl chain with 153 carbons and '
               "28 double bonds'), "
               "('O=C1O[C@@H]([C@H](NC(=O)[C@@H](NC(=O)/C(=C/C)/C)CCC(=O)N)C(=O)N[C@H](C(=O)N[C@H]2CC[C@H](N([C@H](C(N([C@H](C(N[C@H]1C)=O)CC3=CC=C(O)C=C3)C)=O)CC4=CC=CC=C4)C2=O)O)CCC(=O)NCCO)C', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 10 "
               "carbons'), "
               "('OC(C(O)C/C=C\\\\C/C=C\\\\CCCCC)C/C=C\\\\CCCC(=O)NCCO', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 190 "
               "carbons and 31 double bonds'), "
               "('O[C@@H]1[C@@H]([C@H](C(=O)C1)C/C=C\\\\CCCC(=O)NCCO)/C=C/[C@@H](O)CCCCC', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 190 "
               "carbons and 29 double bonds'), "
               "('O([C@H]1[C@@H](C[C@H]([C@@H](O1)C)O)O)[C@@H](CCCCCCCCCCCCCCCCCCCC/C=C(/C(=O)NCCO)\\\\C)C', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 302 "
               "carbons and 24 double bonds'), "
               "('O=C(NCCO)CCCCCCCCC/C=C\\\\CCCCCC', 'N-(fatty "
               'acyl)-ethanolamine with fatty acyl chain with 153 carbons and '
               "7 double bonds'), "
               "('O=C1O[C@@H]([C@H](NC(=O)[C@@H](NC(=O)/C(=C/C)/C)CCC(=O)N)C(=O)N[C@H](C(=O)N2[C@@H](CCC2)C(N[C@H](C(N([C@H](C(N[C@H]1C)=O)CC3=CC=C(O)C=C3)C)=O)CC4=CC=CC=C4)=O)CCC(=O)NCCO)C', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 10 "
               "carbons'), "
               "('O=C(N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(=O)N[C@H](CC(C)C)C(=O)N[C@H](C(=O)N[C@H](CC(C)C)C(=O)N[C@@H](CC=3C=4C(NC3)=CC=CC4)C(=O)N[C@H](CC(C)C)C(=O)N[C@@H](CC=5C=6C(NC5)=CC=CC6)C(=O)NCCO)CC7=CC=CC=C7)[C@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@@H](NC(=O)CNC(=O)[C@@H](NC=O)C(C)C)C)CC(C)C)C)C(C)C)C(C)C)C(C)C', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 3 "
               "carbons'), "
               "('O[C@@H]1[C@@H]([C@H]([C@H](O)C1)/C=C/[C@@H](O)CCCCC)C/C=C\\\\C(C(CC(=O)NCCO)([2H])[2H])([2H])[2H]', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 166 "
               "carbons and 23 double bonds'), "
               "('N(CCO)C(CC[C@@H](C(=O)[O-])[NH3+])=O', 'N-(fatty "
               "acyl)-ethanolamine with fatty acyl chain with 10 carbons'), "
               "('O=C(NCCO)[C@H](C(=O)/C(=C/CCCC)/C)C', 'N-(fatty "
               'acyl)-ethanolamine with fatty acyl chain with 42 carbons and '
               "10 double bonds'), "
               "('CC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCC(=O)NCCO', 'N-(fatty "
               'acyl)-ethanolamine with fatty acyl chain with 153 carbons and '
               "19 double bonds'), "
               "('O1[C@H]([C@H]1C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CCCC(=O)NCCO', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 190 "
               "carbons and 28 double bonds'), "
               "('C(=C\\\\CCCCC(NCCO)=O)\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 153 "
               "carbons and 32 double bonds'), "
               "('CCCCC[C@H](O)\\\\C=C\\\\[C@H]1[C@H](O)C[C@H](O)[C@@H]1C\\\\C=C/CCCC(=O)NCCO', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 166 "
               "carbons and 23 double bonds'), "
               "('CCCCC[C@H](O)\\\\C=C\\\\[C@@H]1[C@@H](C\\\\C=C/CCCC(=O)NCCO)[C@@H](O)CC1=O', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 190 "
               "carbons and 28 double bonds'), ('O=C(NCCO)CCC(N)C(O)=O', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 10 "
               "carbons'), ('O=C(NCCO)CCCCCC=CCC=CCC=CCC=CCC', 'N-(fatty "
               'acyl)-ethanolamine with fatty acyl chain with 171 carbons and '
               "32 double bonds'), "
               "('O=C(NCCO)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C(CCCCCC)(C)C', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 263 "
               "carbons and 60 double bonds'), "
               "('[C@@H]1([C@@H](C[C@H]([C@@H](O1)C)O)O)O[C@@H](CCCCCCCCCCCCCCCCCCCCC(C(C(=O)NCCO)C)=O)C', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 302 "
               "carbons and 11 double bonds'), "
               "('O=C(NCCO)CCCCCCC/C=C\\\\C(CCCCCCC)([2H])[2H]', 'N-(fatty "
               'acyl)-ethanolamine with fatty acyl chain with 153 carbons and '
               "9 double bonds'), "
               "('CCCCC[C@H](O)\\\\C=C\\\\[C@H]1[C@H]2C[C@H](OO2)[C@@H]1C\\\\C=C/CCCC(=O)NCCO', "
               "'N-(fatty acyl)-ethanolamine with fatty acyl chain with 166 "
               "carbons and 23 double bonds')]\n"
               'False negatives: []',
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 5,
    'num_false_positives': 21,
    'num_true_negatives': 183876,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.19230769230769232,
    'recall': 1.0,
    'f1': 0.32258064516129037,
    'accuracy': 0.9998858087459626}