"""
Classifies: CHEBI:138088 long chain primary alcohol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_long_chain_primary_alcohol(smiles: str):
    """
    Determines if a molecule is a long chain primary alcohol (chain length 13-22 carbons).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a long chain primary alcohol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of primary alcohol group (CH2OH)
    primary_alcohol_pattern = Chem.MolFromSmarts("[CH2][OH]")
    if not mol.HasSubstructMatch(primary_alcohol_pattern):
        return False, "Not a primary alcohol"

    # Get the carbon atom connected to OH
    matches = mol.GetSubstructMatches(primary_alcohol_pattern)
    ch2_atom = mol.GetAtomWithIdx(matches[0][0])

    # Count total carbons and check for linearity
    total_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()
    
    # If there are rings, check their size and nature
    if rings:
        ring_carbons = set()
        for ring in rings:
            ring_carbons.update(idx for idx in ring if mol.GetAtomWithIdx(idx).GetSymbol() == 'C')
            
        # If CH2OH is part of a ring or connected to a ring atom, reject
        for neighbor in ch2_atom.GetNeighbors():
            if neighbor.GetIdx() in ring_carbons:
                return False, "Primary alcohol is directly connected to ring system"
                
        # If most carbons are in rings, reject
        if len(ring_carbons) > total_carbons / 2:
            return False, "Structure is predominantly cyclic"

    # For wildcard atoms, assume it's a valid chain
    if '*' in smiles:
        return True, "Valid long chain primary alcohol with wildcard atoms"

    # Calculate the longest chain from CH2OH
    def get_longest_chain(atom, visited=None):
        if visited is None:
            visited = set()
        
        visited.add(atom.GetIdx())
        max_length = 0
        
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in visited and neighbor.GetSymbol() == 'C':
                length = get_longest_chain(neighbor, visited.copy())
                max_length = max(max_length, length)
                
        return max_length + 1

    chain_length = get_longest_chain(ch2_atom)

    if chain_length < 13:
        return False, f"Chain too short ({chain_length} carbons)"
    elif chain_length > 22:
        return False, f"Chain too long ({chain_length} carbons)"

    # Check for excessive branching
    branching_count = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetDegree() > 2:
            branching_count += 1
            if branching_count > 2:  # Allow some branching but not too much
                return False, "Structure is too branched"

    return True, f"Long chain primary alcohol with {chain_length} carbons"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:138088',
                          'name': 'long chain primary alcohol',
                          'definition': 'A primary alcohol with a chain length '
                                        'ranging from 13-22 carbons which is '
                                        'usually but not always a fatty '
                                        'alcohol.',
                          'parents': ['CHEBI:15734']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.056074766355140186 is too low.\n'
               "True positives: [('CCC(C)CCCCCCCCCCCCCCCCCCCO', 'Long chain "
               "primary alcohol with 22 carbons'), ('CC(C)CCCCCCCCCCCCCCO', "
               "'Long chain primary alcohol with 16 carbons'), "
               "('CCCCCCCCCCCCCCCCCO', 'Long chain primary alcohol with 17 "
               "carbons')]\n"
               'False positives: '
               "[('[H][C@@]12CC[C@](C)(CC1=CC[C@@]1([H])[C@@](C)(CO)CCC[C@]21C)C=C', "
               "'Long chain primary alcohol with 16 carbons'), "
               "('COc1cc(C[C@@H]2[C@@H](Cc3cc(OC)c(O)c(c3)C(CO)C(O)c3ccc(O)c(OC)c3)COC2=O)ccc1O', "
               "'Long chain primary alcohol with 17 carbons'), "
               "('O=C1C2=C(OC3=C1C(C(=O)OC)=CC=C3O)C(OC)=C(C(C(O)CO)CO)C=C2OC', "
               "'Long chain primary alcohol with 15 carbons'), "
               "('CC1(C)O[C@@H]2C[C@H]3[C@@H]4C[C@H](F)C5=CC(=O)C=C[C@]5(C)[C@H]4[C@@H](O)C[C@]3(C)[C@@]2(O1)C(=O)CO', "
               "'Long chain primary alcohol with 20 carbons'), "
               "('[C@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)(NC(=O)*COC(CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)CO', "
               "'Long chain primary alcohol with 18 carbons'), "
               "('O[C@@H]1C([C@H]2[C@](C3=C([C@]4([C@]([C@@H]([C@@H]([C@H](O)CC=C(C)C)CO)CC4)(C)CC3)C)CC2)(C)CC1)(C)C', "
               "'Long chain primary alcohol with 20 carbons'), "
               "('O=C1C2=C([C@]3(CCC(C([C@@H]3C1)(C)C)=O)C)CC[C@]4([C@]2(CC[C@@H]4[C@H](CO)CC/C=C(/CO)\\\\C)C)C', "
               "'Long chain primary alcohol with 20 carbons'), "
               "('CCNC(=O)C1=NC(=C2[C@@H](N(CC2=C1)[S@@](=O)C(C)(C)C)CCO)C3=CC(=CC=C3)C4=CCCC4', "
               "'Long chain primary alcohol with 15 carbons'), "
               "('[H][C@@]12CCC3CC(=O)CC[C@]3(C)[C@@]1([H])C(=O)C[C@@]1(C)[C@@]2([H])CC[C@]1(O)C(=O)CO', "
               "'Long chain primary alcohol with 20 carbons'), "
               "('O=C1C=2C(=CC[C@H]3[C@]4(O[C@@H](/C=C(/CO)\\\\C)C[C@@H]4C)CC[C@@]3(CC2[C@@H](C1)C)C)CO', "
               "'Long chain primary alcohol with 20 carbons'), "
               "('C1[C@H]2[C@@H]([C@H]([C@H](N2)C3=CC=C(C(=O)N31)C4=CC=C(C=C4)F)C(=O)NCCC5=CC=NC=C5)CO', "
               "'Long chain primary alcohol with 14 carbons'), "
               "('O=C1[C@]2([C@]([C@]3([C@@]([C@H](CC3)C(=O)CO)(C1)CO)[H])(CC[C@]4([C@@]2(CC[C@@H](O)C4)C)[H])[H])[H]', "
               "'Long chain primary alcohol with 20 carbons'), "
               "('OCCCCC\\\\C=C/C[C@@H](O)C(O)\\\\C=C\\\\C(O)C\\\\C=C/CCCC(O)=O', "
               "'Long chain primary alcohol with 20 carbons'), "
               "('COCC(=O)N1C[C@@H]2[C@H]([C@@H](N2C(=O)C1)CO)C3=CC=C(C=C3)C4=CC=CC=C4F', "
               "'Long chain primary alcohol with 13 carbons'), "
               "('CC(C)NC[C@@H]1[C@@H]([C@@H](N1C(=O)NC(C)C)CO)C2=CC=C(C=C2)C3=CCCCC3', "
               "'Long chain primary alcohol with 13 carbons'), "
               "('O[C@]([C@@H](O)[C@@H](O)C[C@@]1([C@H]2C3=C4C(=C(C)CC4=C(C)C=C3)C[C@@]2(C)C[C@@H]1O)C)(CO)C', "
               "'Long chain primary alcohol with 20 carbons'), "
               "('C1CN([C@@H]2[C@H]1[C@@H](NC3=C2C=C(C=C3)C#CC4=CC=CC=C4)CO)C(=O)C5=CC(=CC=C5)F', "
               "'Long chain primary alcohol with 17 carbons'), "
               "('C1=2C(OC(=CC1=O)C3=CC=C(C(=C3)OC)O)=CC(=C(C2O)[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O)O)O)OC', "
               "'Long chain primary alcohol with 20 carbons'), "
               "('O[C@H](C(=C)CC/C=C(/CO)\\\\C)CC/C(=C/CC/C(=C/CO)/C)/C', "
               "'Long chain primary alcohol with 16 carbons'), "
               "('C1CCC(C1)NC(=O)[C@@H]2[C@H]([C@@H]3CN4C(=CC=C(C4=O)C5=CC=CC=C5)[C@H]2N3CCC6=CC=CC=C6)CO', "
               "'Long chain primary alcohol with 14 carbons'), "
               "('CCCCCCCCCCCCC(O)CO', 'Long chain primary alcohol with 14 "
               "carbons'), "
               "('C1CCC(CC1)C#CC2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@H]3CO)C(=O)CC5=CN=CC=C5', "
               "'Long chain primary alcohol with 15 carbons'), "
               "('Cl[C@H]([C@H](O)[C@H](O)[C@H](O)/C=C/C1=C(C(OC)=CC=C1)CO)C', "
               "'Long chain primary alcohol with 14 carbons'), "
               "('O=C1C(OC)=C(C(=O)C2=C1C=C(O)C3=C2O[C@@H](C)[C@]3(C(O)C/C=C(/CO)\\\\C)C)C', "
               "'Long chain primary alcohol with 16 carbons'), "
               "('C(C\\\\C=C(\\\\CC\\\\C=C(\\\\CC\\\\C=C(\\\\CCC=C(C)C)/C)/C)/C)/C(=C\\\\CO)/C', "
               "'Long chain primary alcohol with 20 carbons'), "
               "('O1[C@]([C@H](O)[C@@H](O)[C@H](O)[C@H]1CO)(C2=C(O)C([C@@]3(O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)CO)[H])=C(O)C(=C2O)C(=O)CCC4=CC=C(O)C=C4)[H]', "
               "'Long chain primary alcohol with 20 carbons'), "
               "('O=C/1O[C@](CO)(C)C\\\\C1=C\\\\CCCCCCC/C=C\\\\CCCCCC', 'Long "
               "chain primary alcohol with 20 carbons'), "
               "('[H][C@]12O[C@]11CC[C@]3([H])C(C)(C)CCC[C@@]3(C)[C@]1([H])[C@@]1([H])O[C@]11OC(=O)C(CO)=C21', "
               "'Long chain primary alcohol with 16 carbons'), "
               "('O=C(O[C@@H]1[C@]23O[C@@](OC)(C=C([C@H]2CC3(C)C)CO)C=C(C1)C)C', "
               "'Long chain primary alcohol with 13 carbons'), "
               "('C1CCN(CC1)C(=O)[C@H]2[C@@H]([C@H]3CN4C(=CC=C(C4=O)C5=CCCCC5)[C@@H]2N3CC6=NC=CS6)CO', "
               "'Long chain primary alcohol with 14 carbons'), "
               "('OC1=C([C@H](CCN(C(C)C)C(C)C)C2=CC=CC=C2)C=C(C=C1)CO', 'Long "
               "chain primary alcohol with 13 carbons'), "
               "('O1C(C(O)C(O)C(O)C1CO)C2=C(O)C(=C(O)C=C2O)C(=O)C', 'Long "
               "chain primary alcohol with 13 carbons'), "
               "('C(\\\\C=C/C=C/C=C/[C@H]([C@H](CCCCCO)O)O)=C/[C@H](CCCC([O-])=O)O', "
               "'Long chain primary alcohol with 20 carbons'), "
               "('O=C1C=C2[C@@]3(CC[C@]([C@H](C2)C3)(O)CO)[C@@]4([C@@H]1[C@@]([C@H](O)CC4)(CO)C)C', "
               "'Long chain primary alcohol with 18 carbons'), "
               "('O=C(O[C@H]1[C@H](O[C@@H]2O[C@@H]([C@H](O)[C@@H]([C@H]2O)O)COC(=O)/C=C/C=C\\\\CCCCC)[C@H](OC([C@@H]1O)C3=C(O)C=C(O)C=C3CO)CO)/C(=C/C=C/CC(O)C(CC)C)/C', "
               "'Long chain primary alcohol with 13 carbons'), "
               "('[H][C@@]12C=C(CO)C[C@]3(O)C(=O)C(C)=C[C@@]3([H])[C@@]1(O)[C@H](C)[C@@H](OC(=O)CC\\\\C=C/CCCCC)[C@]1(OC(C)=O)[C@@]2([H])C1(C)C', "
               "'Long chain primary alcohol with 16 carbons'), "
               "('CC1=CC=C(C=C1)S(=O)(=O)N2CC[C@H]3[C@@H]2C4=C(C=CC(=C4)C5=CC(=CC=C5)C(=O)N(C)C)N[C@@H]3CO', "
               "'Long chain primary alcohol with 15 carbons'), "
               "('C1COCCC1C(=O)N2C[C@@H]3[C@H]([C@H](N3C(=O)C2)CO)C4=CC=C(C=C4)C#CCC5=CC=CC=C5', "
               "'Long chain primary alcohol with 16 carbons'), "
               "('O=C(O)/C(=C/CC[C@H]([C@@H]1[C@@]2([C@@]([C@H]3[C@@]([C@@H](C(=C(C)C)CC3)CCCO)(C)CC2)(C)CC1)C)C)/C', "
               "'Long chain primary alcohol with 22 carbons'), "
               "('CN(C)C(=O)[C@H]1[C@@H]([C@H]2CN3C(=CC=C(C3=O)C4=CCCC4)[C@@H]1N2CC5CCOCC5)CO', "
               "'Long chain primary alcohol with 13 carbons'), "
               "('CCC(=O)N1[C@@H]2CN3C(=CC=C(C3=O)C4=CC=C(C=C4)F)[C@H]1[C@H]([C@@H]2CO)C(=O)OC', "
               "'Long chain primary alcohol with 14 carbons'), "
               "('COC1=CC=CC=C1C2=CC=C(C=C2)[C@@H]3[C@H](N[C@@H]3C#N)CO', "
               "'Long chain primary alcohol with 13 carbons'), "
               "('OC[C@H]1O[C@H]([C@H](O)[C@@H](O)[C@@H]1O)c1c(O)c([C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)c2occ(-c3ccc(O)cc3)c(=O)c2c1O', "
               "'Long chain primary alcohol with 19 carbons'), "
               "('O1[C@@H]([C@H]1/C=C/C(=O)[C@@]2(O)[C@@H](O)[C@@H](NC2=O)CO)CCCCCCCCC', "
               "'Long chain primary alcohol with 18 carbons'), "
               "('O1[C@H](O[C@@H]2C3=C(C(C)C)C[C@@H]([C@@]3(C=C4[C@H](CO)CC[C@H]4[C@H]([C@H]2O)C)C)O)[C@H](O)[C@@H](O)[C@@H]([C@H]1CO)O', "
               "'Long chain primary alcohol with 16 carbons'), "
               "('C[C@]12C[C@H](O)[C@@]3(F)[C@@H](CCC4=CC(=O)C=C[C@]34C)[C@@H]1CC[C@]2(O)C(=O)CO', "
               "'Long chain primary alcohol with 20 carbons'), "
               "('COC1=CC=CC(=C1)C2=CC3=C(C=C2)N[C@H]([C@H]4[C@@H]3N(CC4)C(=O)CC5=CC=CC=C5)CO', "
               "'Long chain primary alcohol with 15 carbons'), "
               "('CC1=CC=CC=C1S(=O)(=O)N2CC[C@@H]3[C@H]2C4=C(C=CC(=C4)C5=CC(=CC=C5)OC)N[C@@H]3CO', "
               "'Long chain primary alcohol with 15 carbons'), "
               "('O=C1C(=C(C=CCCCCC)[C@@H](O)[C@H](C1)O)CO', 'Long chain "
               "primary alcohol with 14 carbons'), "
               "('COC1=CC=CC(=C1)NC(=O)N2C[C@@H]3[C@@H]([C@H](N3C(=O)C2)CO)C4=CC=C(C=C4)C#CCC5CCCC5', "
               "'Long chain primary alcohol with 15 carbons'), "
               "('C1CCC(CC1)C#CC2=CC=C(C=C2)[C@@H]3[C@@H]4CN(CC(=O)N4[C@H]3CO)C(=O)C5CCOCC5', "
               "'Long chain primary alcohol with 15 carbons'), "
               "('C\\\\C(CO)=C/CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\C([O-])=O', "
               "'Long chain primary alcohol with 16 carbons'), "
               "('C1CCC(=CC1)C2=CC=C3[C@@H]4[C@@H]([C@H]([C@@H](N4)CN3C2=O)CO)C(=O)NCC5=CC=C(C=C5)F', "
               "'Long chain primary alcohol with 14 carbons'), "
               "('CCCCCCCCCCCC(=O)[C@@H]([NH3+])CO', 'Long chain primary "
               "alcohol with 14 carbons'), "
               "('O=C1C(=C)[C@]2([C@H]3[C@H](CC(C3)(C)C)C[C@]42[C@@H]1O4)CO', "
               "'Long chain primary alcohol with 13 carbons'), "
               "('O1[C@](C(O)[C@@H](O)[C@H](O)C1CO)(C=2C=3OC=C(C(=O)C3C=CC2O)C4=CC=C(OC)C=C4)[H]', "
               "'Long chain primary alcohol with 19 carbons'), "
               "('O=C1N2[C@@]3([C@@]4([C@]5(N(CC4)C\\\\C(\\\\[C@](C5)([C@]3([C@@H](C1)O)[H])[H])=C\\\\CO)[H])C=6C2=CC=CC6)[H]', "
               "'Long chain primary alcohol with 13 carbons'), "
               "('OC[C@@]12[C@]([C@]3([C@](CC1)([C@@]4(C(CC3)=CC(=O)C=C4)C)[H])[H])(CC[C@@H]2C=C)[H]', "
               "'Long chain primary alcohol with 20 carbons'), "
               "('CCCCCCCCCCCCCCCC(=O)C(N)CO', 'Long chain primary alcohol "
               "with 18 carbons'), "
               "('Cc1coc2C(=O)c3c(ccc4c3CCCC4(C)CO)C(=O)c12', 'Long chain "
               "primary alcohol with 16 carbons'), "
               "('C\\\\C(CCC1=C(C)CCCC1(C)C)=C/CC\\\\C(CO)=C/C[C@H]1OC(=O)C=C1CO', "
               "'Long chain primary alcohol with 15 carbons'), "
               "('O=C1C(O)=C(C(=O)C=C1CO)C[C@H]2C(=C)CC[C@@H]3[C@@]2(CCC[C@@]3(CO)C)C', "
               "'Long chain primary alcohol with 17 carbons'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@H](O)[C@H](N)CO', 'Long chain "
               "primary alcohol with 18 carbons'), "
               "('O=C1C2=C(O)C(=C(O)C=C2C(=O)C=3C1=C(O)C=C(O)C3)[C@H](C(=O)O)CCO', "
               "'Long chain primary alcohol with 17 carbons'), "
               "('C(\\\\CC(/C=C/C=C\\\\C/C=C\\\\CCCCCO)OO)=C\\\\CCCC(OC)=O', "
               "'Long chain primary alcohol with 20 carbons'), "
               "('CC(C)(C)[S@@](=O)N1CC2=CC(=NC(=C2[C@H]1CCO)C3=CC=CC(=C3)C4=CC=C(C=C4)F)C(=O)N5CCCCC5', "
               "'Long chain primary alcohol with 16 carbons'), "
               "('OCCCCCCCCCC/C=C/CCCCCCCC', 'Long chain primary alcohol with "
               "20 carbons'), "
               "('O=C(O)/C(=C/CO)/CC=C1[C@](CC[C@@H]1C(C)C)(C/C=C(/C(=O)O)\\\\C)C', "
               "'Long chain primary alcohol with 14 carbons'), "
               "('O=C(O)/C=C/C=C/[C@@H]1[C@@H](C(=C[C@H]2[C@H]1[C@H](C[C@@H](C2)O)C)C)C(=CCO)C', "
               "'Long chain primary alcohol with 18 carbons'), "
               "('CC(C)(C)[S@@](=O)N1CC2=CC(=NC(=C2[C@H]1CCO)C3=CC(=CC=C3)C4=CCCC4)C(=O)N5CCN(CC5)C', "
               "'Long chain primary alcohol with 15 carbons'), "
               "('CC(=O)N1[C@@H]([C@@H]([C@@H]1CO)C2=CC=C(C=C2)C3=CCCCC3)CNC(=O)CN(C)C', "
               "'Long chain primary alcohol with 13 carbons'), "
               "('C[C@@H]1O[C@H](C[C@H](N)[C@@H]1O)O[C@H]1C[C@@](O)(Cc2cc3C(=O)c4cccc(O)c4C(=O)c3c(O)c12)C(=O)CO', "
               "'Long chain primary alcohol with 20 carbons'), "
               "('O[C@H](C(=C)CC/C=C(/CC/C=C(/CO)\\\\C)\\\\C)CC/C(=C/CO)/C', "
               "'Long chain primary alcohol with 16 carbons'), "
               "('C1[C@@H]2[C@H]([C@@H](N2C(=O)CN1C(=O)NC3=CC=C(C=C3)F)CO)C4=CC=C(C=C4)C#CC5=CN=CC=C5', "
               "'Long chain primary alcohol with 13 carbons'), "
               "('O1C(C(C2=C1C(OC)=CC(=C2)/C=C\\\\CO)CO)C3=CC(OC)=C(O)C=C3', "
               "'Long chain primary alcohol with 16 carbons'), "
               "('O=C1[C@]2(C(=C(CO)C3=C(C1)C(OC(C3)=O)(C)C)C[C@]4(C(=O)O[C@@H]5[C@H]4[C@H]2C(=O)[C@H](O5)C)C)C', "
               "'Long chain primary alcohol with 15 carbons'), "
               "('CCCCCCCCCCCCCCC[C@@H](O)[C@H](CO)NC(=O)CCCCCCCCCCCCC', 'Long "
               "chain primary alcohol with 18 carbons'), "
               "('COC1=CC=CC(=C1)C2=CC3=C(C=C2)N[C@@H]([C@H]4[C@@H]3N(CC4)C(=O)CC5=CC=CC=C5)CO', "
               "'Long chain primary alcohol with 15 carbons'), "
               "('O=C1N[C@@](OC)(C(=O)C2=CC=CC=C2)C([C@@]13OC(CO)=C(C3=O)C)O', "
               "'Long chain primary alcohol with 14 carbons'), "
               "('CN1[C@H]2CN3C(=CC=C(C3=O)C4=CC(=CC=C4)C(=O)N(C)C)[C@@H]1[C@@H]([C@H]2CO)C(=O)NCC(F)(F)F', "
               "'Long chain primary alcohol with 14 carbons'), "
               "('O=C1O[C@H](C2=C(O)C=CC(=C2)O)C=C1CC/C=C(\\\\CO)/C', 'Long "
               "chain primary alcohol with 14 carbons'), "
               "('O=C1C2=C(O[C@]3(CC=C([C@]3(C2)O)C(CCCC(CO)C)C)C)CC[C@@H]1O', "
               "'Long chain primary alcohol with 18 carbons'), "
               "('COc1cc(C[C@@H]2[C@@H](Cc3ccc(OC)c(OC)c3)COC2=O)cc2[C@H](CO)[C@H](Oc12)c1ccc(O)c(OC)c1', "
               "'Long chain primary alcohol with 17 carbons'), "
               "('CCC(=O)N1C[C@@H]2[C@H]([C@@H](N2C(=O)C1)CO)C3=CC=C(C=C3)C#CC4=CN=CC=C4', "
               "'Long chain primary alcohol with 13 carbons'), "
               "('COC1=CC=CC=C1C2=CC=C3[C@@H]4[C@@H]([C@H]([C@@H](N4CC5=CC=CC=C5)CN3C2=O)CO)C(=O)OC', "
               "'Long chain primary alcohol with 14 carbons'), "
               "('O[C@H]1[C@@]2([C@H]([C@@H]3[C@@H]4[C@@](CC[C@H]4C(C)C)(C)CC[C@]3(C1)C)C2)CO', "
               "'Long chain primary alcohol with 15 carbons'), "
               "('CCS(=O)(=O)N1CCCCN2[C@H](C1)[C@H]([C@H]2CO)C3=CC=C(C=C3)C4=CC=C(C=C4)C(=O)N(C)C', "
               "'Long chain primary alcohol with 13 carbons'), "
               "('O1[C@]2([C@H]3[C@](C[C@]4(O)[C@H]([C@H](O)C[C@H]4C)C(=CC3)CO)(C)CC2)[C@@H](C)C[C@@H]1C=C(C)C', "
               "'Long chain primary alcohol with 18 carbons'), "
               "('O[C@@H]([C@@H](NC(=O)CCC[C@@H](O)/C=C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'Long chain primary alcohol with 18 carbons'), "
               "('[H][C@]12C[C@@H](OC(C)=O)C(CO)=C[C@H](O)[C@]1(C)CC[C@@]1(C)CCC(C(C)C)=C21', "
               "'Long chain primary alcohol with 15 carbons'), "
               "('C1CCC(=CC1)C2=CC=C(C=C2)[C@H]3[C@H]4CN(CC(=O)N4[C@@H]3CO)C(=O)CC5=CN=CC=C5', "
               "'Long chain primary alcohol with 13 carbons'), "
               "('C1CCC(=CC1)C2=CC=C(C=C2)[C@@H]3[C@H]4CNCC(=O)N4[C@H]3CO', "
               "'Long chain primary alcohol with 13 carbons'), "
               "('O=C(O)C=CC=CC1=C2C(=CC=C1C)C[C@@H](CO)C[C@H]2C', 'Long chain "
               "primary alcohol with 15 carbons'), "
               "('O=C1C=C2[C@]([C@H](CC[C@@H]2O)C)(C)[C@@H]3[C@H]1[C@]3(CO)C', "
               "'Long chain primary alcohol with 13 carbons'), "
               "('CCC1=CN=C(S1)N2[C@H]([C@@H]([C@@H]2C#N)C3=CC=C(C=C3)C4=CCCCC4)CO', "
               "'Long chain primary alcohol with 13 carbons'), "
               "('C1CCC(C1)(C#CC2=CC=C(C=C2)[C@H]3[C@H](N([C@@H]3C#N)C(=O)C4CC4)CO)O', "
               "'Long chain primary alcohol with 14 carbons'), "
               "('C1[C@@H]2[C@@H]([C@@H](N2C(=O)CN1CC3=CC=C(C=C3)F)CO)C4=CC=C(C=C4)C5=CC=CC=C5', "
               "'Long chain primary alcohol with 13 carbons'), "
               "('CCCN1[C@@H]2[C@@H](CN3C2=CC=C(C3=O)C4=CC=C(C=C4)C(=O)N(C)C)[C@@H]([C@H]1C(=O)NCCOC)CO', "
               "'Long chain primary alcohol with 14 carbons'), "
               "('CCCNC(=O)[C@@H]1[C@H]([C@@H]2CN3C(=CC=C(C3=O)C4=CC=CC=C4F)[C@@H]2N1CC5CC5)CO', "
               "'Long chain primary alcohol with 14 carbons'), "
               "('OCC12C(C(C(CC1)C)(CCC(CC(O)=O)C)C)CCC=C2CO', 'Long chain "
               "primary alcohol with 13 carbons')]\n"
               "False negatives: [('OC[*]', 'Chain too short (1 carbons)')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 27380,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 1.0,
    'f1': 0.07407407407407407,
    'accuracy': 0.9963615194294863}