"""
Classifies: CHEBI:10036 wax ester
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_wax_ester(smiles: str):
    """
    Determines if a molecule is a wax ester - a fatty acid ester formed between a fatty acid
    and a fatty alcohol.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a wax ester, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for ester group (R-O-C(=O)-R)
    ester_pattern = Chem.MolFromSmarts('[CH2,CH3]-[O;H0]-C(=O)-[C;!R]')
    if not mol.HasSubstructMatch(ester_pattern):
        return False, "No ester group found"

    # Get the ester atoms
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    if not ester_matches:
        return False, "No valid ester group found"
    
    # Calculate ring information
    ring_info = mol.GetRingInfo()
    ring_atoms = set()
    for ring in ring_info.AtomRings():
        ring_atoms.update(ring)

    # For each ester group found
    for match in ester_matches:
        # Skip if ester is part of a lactone (cyclic ester)
        if any(idx in ring_atoms for idx in match):
            continue

        # Get the atoms on either side of the ester
        alcohol_carbon = mol.GetAtomWithIdx(match[0])
        acid_carbon = mol.GetAtomWithIdx(match[3])
        
        # Check alcohol side chain length (should be at least 8 carbons for fatty alcohol)
        alcohol_chain = get_chain_length(mol, alcohol_carbon, ring_atoms)
        if alcohol_chain < 8:
            continue
            
        # Check acid side chain length (should be at least 8 carbons for fatty acid)
        acid_chain = get_chain_length(mol, acid_carbon, ring_atoms)
        if acid_chain < 8:
            continue
            
        # Check if the molecule has too many heteroatoms
        num_n = len(mol.GetSubstructMatches(Chem.MolFromSmarts('[N]')))
        num_o = len(mol.GetSubstructMatches(Chem.MolFromSmarts('[O]')))
        num_other = len(mol.GetSubstructMatches(Chem.MolFromSmarts('[!#1!#6!#7!#8]')))
        
        if num_n > 2 or num_o > 3 or num_other > 0:
            continue

        return True, f"Wax ester found with alcohol chain length {alcohol_chain} and acid chain length {acid_chain}"

    return False, "No fatty acid ester found with sufficient chain lengths"

def get_chain_length(mol, start_atom, ring_atoms):
    """Helper function to get the length of a carbon chain from a starting atom"""
    visited = set()
    queue = [(start_atom, 1)]
    max_length = 1
    
    while queue:
        current_atom, length = queue.pop(0)
        visited.add(current_atom.GetIdx())
        
        for neighbor in current_atom.GetNeighbors():
            if (neighbor.GetIdx() not in visited and 
                neighbor.GetSymbol() == 'C' and 
                neighbor.GetIdx() not in ring_atoms):
                queue.append((neighbor, length + 1))
                max_length = max(max_length, length + 1)
                
    return max_length


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:10036',
                          'name': 'wax ester',
                          'definition': 'A fatty acid ester resulting from the '
                                        'condensation of the carboxy group of '
                                        'a fatty acid with the alcoholic '
                                        'hydroxy group of a fatty alcohol.',
                          'parents': ['CHEBI:35748', 'CHEBI:73702']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.1652892561983471 is too low.\n'
               'True positives: '
               "[('O(C(=O)CCCCCCCCCCCCCCCCCCCCC)CCCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC', "
               "'Wax ester found with alcohol chain length 18 and acid chain "
               "length 23'), "
               "('O(CCCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)C(=O)CCCCCCC/C=C\\\\CCCCCCCC', "
               "'Wax ester found with alcohol chain length 18 and acid chain "
               "length 19'), "
               "('O(CCCCCCCC/C=C\\\\CCCCCC)C(=O)CCCCCCC/C=C\\\\CCCCCC', 'Wax "
               'ester found with alcohol chain length 16 and acid chain length '
               "17'), "
               "('O(CCCCCCCCCCCCCCCCCC)C(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC', "
               "'Wax ester found with alcohol chain length 18 and acid chain "
               "length 19'), ('O(CCCCCCCCCCCC)C(=O)CCCCCCC/C=C\\\\CCCC', 'Wax "
               'ester found with alcohol chain length 12 and acid chain length '
               "15'), ('CCCCCCCCCCCCCCCCOC(=O)CCCCCCC\\\\C=C\\\\CCCCCCCC', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 19'), ('O(CCCCCCCCCCCCCCCCCC)C(=O)CCCCCCCCC/C=C/CCCC', "
               "'Wax ester found with alcohol chain length 18 and acid chain "
               "length 17'), "
               "('O(CCCCCCCCCCCC)C(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC', 'Wax "
               'ester found with alcohol chain length 12 and acid chain length '
               "19'), ('O(CCCCCCCC/C=C\\\\CCCCCC)C(=O)CCCCCCC/C=C\\\\CCCC', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 15'), ('O(CCCCCCCC/C=C\\\\CCCC)C(=O)CCCCCCCCCCCCC', "
               "'Wax ester found with alcohol chain length 14 and acid chain "
               "length 15')]\n"
               'False positives: '
               "[('O[C@H]1C[C@H]([C@]2([C@@](C1)(CC[C@]3([C@]4(CC[C@@H]([C@]4(C[C@H]([C@]23[H])O)C)C5COC(C5)=O)O)[H])O)CO)O', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 14'), "
               "('[H][C@@]12CC[C@]3([H])[C@]([H])(CC[C@@]4(C)[C@@]3([H])CC[C@]4(C)O)[C@@]1(C)COC(=O)C2', "
               "'Wax ester found with alcohol chain length 8 and acid chain "
               "length 11'), "
               "('CCCCC\\\\C=C/C\\\\C=C/CCCCCCCC(=O)OCCCc1cc(OC)c2oc(cc2c1)-c1ccc2OCOc2c1', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 19'), ('O1CCCCCCCCC=CCC1=O', 'Wax ester found with "
               "alcohol chain length 12 and acid chain length 13'), "
               "('O=C(O[C@H](C=C(C)C)C/C(=C/CC1=C(O)C(=C(COC(=O)CCCCCCCCCCCCCCC)C=C1OC)C=O)/C)CCCCCCCCCCCCCCC', "
               "'Wax ester found with alcohol chain length 13 and acid chain "
               "length 17'), "
               "('[H][C@@]1(CC[C@]2(O)[C@]3([H])CC[C@]4(O)C[C@H](C[C@@H](O)[C@]4(CO)[C@@]3([H])[C@H](O)C[C@]12C)O[C@@H]1O[C@@H](C)[C@H](O)[C@@H](O)[C@H]1O)C1COC(=O)C1', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 14'), "
               "('O(C(=O)CCCCCCC/C=C/C\\\\C=C\\\\CCCCC)CC=1C(=C(O)C(C/C=C(/CC(=O)C=C(C)C)\\\\C)=C(OC)C1)C=O', "
               "'Wax ester found with alcohol chain length 13 and acid chain "
               "length 19'), "
               "('O=C1C2=C([C@@]3([C@@H](O)C[C@@H]([C@]3(C1)C)[C@]4(COC(C4)=O)CO)C)[C@@H](O)C[C@@H]5[C@@]2(CCC(C5(C)C)=O)C', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 14'), "
               "('CCCCCCCCCCCCCC(=O)OC\\\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 15'), "
               "('O=C(OC[C@H](C1=C2C3=CC=C(C=O)C[C@@H]([C@@]3(CC[C@@]2(C)CC1)C)O)C)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC', "
               "'Wax ester found with alcohol chain length 9 and acid chain "
               "length 19'), "
               "('COc1cc2OC(=C)C(=O)Nc2c(c1)C(=O)O[C@H]1COC(=O)C[C@H](N)c2ccc(O[C@@H]3c4ccc1cc4C1=CC=C[C@]31OC1OC(C)(C)C(C(O)C1O)N(C)C)c(Cl)c2', "
               "'Wax ester found with alcohol chain length 9 and acid chain "
               "length 8'), "
               "('C1=2N3C(C=C4[N+]5=C(C=C6N7C8=C(C9=[N+](C(=C1)[C@H]([C@@H]9CCC(OC/C=C(/CCC[C@@H](CCC[C@@H](CCCC(C)C)C)C)\\\\C)=O)C)[Mg-2]735)[C@H](C(C8=C6C)=O)C(=O)OC)C(=C4*)*)=C(C2*)*', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 15'), "
               "('ClC1=C2O[C@@H]3C4=C(C=C([C@@H](OC(=O)C5=C6NC(=O)C(=C)OC6=CC(=C5)OC)COC(C[C@@H](C(=C1)C=C2O)N)=O)C=C4)C=7[C@]3(O[C@@H]8OC([C@@H](N(C)C)[C@@H](C8O)O)(C)C)C=CC7', "
               "'Wax ester found with alcohol chain length 9 and acid chain "
               "length 8'), "
               "('O=C1OCC2C=C(C34OC5CC(C3C(C5)C=CC4C(OC)C(C(OC2C(O)COC=CC6=C(CC1)C(=O)OC6=O)=O)OC)O)C', "
               "'Wax ester found with alcohol chain length 9 and acid chain "
               "length 8'), "
               "('O(C(=O)CCC1C(C=2NC1=C3CC(=O)C=4C3=NC(C4C)=CC=5N=C(C=C6N=C(C2)C(=C6C=C)C)C(C5CC)=CO)C)C\\\\C=C(\\\\CC(CC(CCCC(CCCCC)C)C)C)/C', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 17'), "
               "('COC1=C[C@@H](C)[C@@H]2C[C@H]3OC(=O)C[C@H]4[C@@](C)(C[C@@H](O)[C@@H]([C@@]34C)[C@@]2(C)C1=O)C(=O)[C@H]1COC(=O)C1', "
               "'Wax ester found with alcohol chain length 11 and acid chain "
               "length 13'), "
               "('[H][C@@]1(CCC(=O)OC1)[C@@]1([H])CC[C@]2([H])[C@]3([H])CC[C@@]4([H])CCCC[C@]4(C)[C@@]3([H])CC[C@]12C', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 15'), "
               "('CCCCCCCCCCCCCCCC(=O)OC\\\\C=C(C)\\\\C=C\\\\C=C(C)\\\\C=C\\\\C1=C(C)CCCC1(C)C', "
               "'Wax ester found with alcohol chain length 13 and acid chain "
               "length 17'), "
               "('ClC1=C2C=CC3=C1C4=CC=C[C@]4(O[C@@H]5OC([C@@H](N(C)C)[C@H]([C@H]5O)O)(C)C)[C@@H]3OC6=C(Cl)C=C([C@H](CC(OC[C@@H]2OC(=O)C7=C8NC(=O)C(=C)OC8=CC(=C7)OC)=O)N)C=C6O', "
               "'Wax ester found with alcohol chain length 9 and acid chain "
               "length 8'), "
               "('O=C1OC[C@@H](C1)C(=C2[C@H](C=C)CC(C2)(C)C)COC(=O)CCC(=O)OC', "
               "'Wax ester found with alcohol chain length 8 and acid chain "
               "length 10'), "
               "('CCC1=C(C)C2=Cc3c(C=C)c(C)c4C=C5[C@@H](C)[C@H](CCC(=O)OC\\\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C6=[N+]5[Mg--]5(n34)n3c(=CC1=[N+]25)c(C)c1C(=O)[C-](C(=O)OC)C6=c31', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 17'), "
               "('CCC1=C(C=O)C2=Cc3c(C=C)c(C)c4C=C5[C@@H](C)[C@H](CCC(=O)OC\\\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C6=[N+]5[Mg--]5(n34)n3c(=CC1=[N+]25)c(C)c1C(=O)[C@H](C(=O)OC)C6=c31', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 17'), "
               "('ClC1=C2OC3C#CC=C(C(OC(=O)C4=C5NC(=O)C(C)OC5=CC(=C4)OC)COC(CC(C(=C1)C=C2O)N)=O)C#CC=6C3(O[C@@H]7OC([C@@H](N(C)C)C(C7O)O)(C)C)C=CC6', "
               "'Wax ester found with alcohol chain length 9 and acid chain "
               "length 8'), "
               "('O1C2(C3(C(C4(C(CC3=O)C(O)(C)C)C(O)CC(OC4)=O)CCC2(C(OC5OC(C(O)C(O)C5O)CO)C=6C=COC6)C)C)C1C(O)=O', "
               "'Wax ester found with alcohol chain length 10 and acid chain "
               "length 13'), ('O(CCCCCCCCCC)C(=O)CCCCCCC', 'Wax ester found "
               "with alcohol chain length 10 and acid chain length 9'), "
               "('O1C(CC(=O)C2=C1C=CC(=C2N)C(=O)CC(NC(=O)C)COC(=O)CCCCCCC/C=C/CCCCCCCC)(C)C', "
               "'Wax ester found with alcohol chain length 11 and acid chain "
               "length 19'), "
               "('C12=CC=CC=C1N=C3C(=C2)CN4C(C5=C(C=C34)[C@](CC(OC5)=O)(CC)O)=O', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 14'), "
               "('O(C(=O)CCCCCCCCCCCCCCCCC)CC=1C(=C(O)C(=C(OC)C1)C/C=C(/CC(=O)C=C(C)C)\\\\C)C=O', "
               "'Wax ester found with alcohol chain length 13 and acid chain "
               "length 19'), "
               "('O=C(OCC1=C(C=2O[C@](CCC2C(=C1)OC)(CC(=O)C=C(C)C)C)C=O)CCCCCCCCCCCCCCCCC', "
               "'Wax ester found with alcohol chain length 13 and acid chain "
               "length 19'), "
               "('CCCCCCCCCC(=O)OC\\\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 11'), "
               "('C1(C)(C)C(\\\\C=C\\\\C(=C\\\\C=C\\\\C(=C\\\\COC(CCCCCC)=O)\\\\C)\\\\C)=C(C)CCC1', "
               "'Wax ester found with alcohol chain length 13 and acid chain "
               "length 8'), "
               "('C=12N3C(=CC4=[N+]5C(=CC=6N7C=8C(=C9[N+](=C(C1)[C@H]([C@@H]9CCC(OC/C=C(/CC/C=C(/CC/C=C(/CCC=C(C)C)\\\\C)\\\\C)\\\\C)=O)C)[Mg-2]735)[C-](C(C8C6C)=O)C(=O)OC)[C@@H]([C@H]4C)CC)C(=C2C)C(=O)C', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 16'), "
               "('COC(=O)[C@H]1C(=O)c2c(C)c3=CC4=[N+]5C(=Cc6c(C=C)c(C)c7C=C8[C@@H](C)[C@H](CCC(=O)OC\\\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C9=[N+]8[Mg--]5(n67)n3c2=C19)C(C)=C4C=C', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 16'), "
               "('C\\\\C=C(/C)C(=O)O[C@@H]1[C@@H]2OC[C@@]3(C)[C@H]2[C@](C)([C@@H](O)C[C@H]3OC(C)=O)[C@H]2CC[C@@]3(C)[C@H](C4COC(=O)C4)C(=O)C=C3[C@]12C', "
               "'Wax ester found with alcohol chain length 11 and acid chain "
               "length 13'), "
               "('[H][C@@]12CC[C@](O)(C(=O)COC(=O)CCCCCCC(=O)N(C)CCS([O-])(=O)=O)[C@@]1(C)C[C@H](O)[C@@]1([H])[C@@]2([H])C[C@H](C)C2=CC(=O)C=C[C@]12C', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 9'), "
               "('O=C1OCC2=CC(O)=CC(=C2)CC(=CC=C[C@H](C(C[C@@H]([C@H](C=C([C@H](C1)O)C)C)O)=O)OC)C', "
               "'Wax ester found with alcohol chain length 19 and acid chain "
               "length 20'), "
               "('[H][C@]12CCC=C(C)[C@]1(C)[C@@H](OC(=O)c1cccnc1)[C@H](OC(C)=O)[C@]1(C)O[C@@]3(COC(=O)C3)C[C@H](OC(=O)c3cccnc3)[C@]21C', "
               "'Wax ester found with alcohol chain length 9 and acid chain "
               "length 11'), "
               "('CC(O)C1=C2C=C3C(C)=C(C)C4=[N+]3[Mg--]35N6C(=C4)C(C)=C4C(=O)CC(=C64)C4=[N+]3C([C@@H](C)[C@@H]4CCC(=O)OC\\\\C=C(/C)CC\\\\C=C(/C)CCC=C(C)C)=C(C)C(N25)=C1C', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 16'), "
               "('O=C1O[C@H]([C@H]([C@@H]2[C@@]3([C@@]([C@@]45OC([C@@H]([C@]6(C4=CC3)COC(=O)CC6)CC5)(C)C)(C)CC2)C)C)CC=C1C', "
               "'Wax ester found with alcohol chain length 13 and acid chain "
               "length 16'), "
               "('C(C[C@@H](CCC[C@H](C)CCCC(C)C)C)C/C(=C/COC(=O)CC[C@@]1(C=2C3=C4N5C(=CC=6[C@@H]([C@@H](C)C(N6)=CC=7N([Zn]5)C(=C(C)C7C(C)=O)C=C(N2)[C@H]1C)CC)C(=C4C(=O)[C@@H]3C(OC)=O)C)[H])/C', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 16'), "
               "('[H][C@]1(COC(=O)C1)[C@@]1([H])CC[C@]2([H])[C@]3([H])CCC4CCCC[C@]4(C)[C@@]3([H])CC[C@]12C', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 14'), "
               "('CCC1=C(C)C2=Cc3c(C=C)c(C)c4C=C5[C@@H](C)[C@H](CCC(=O)OC\\\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C6=[N+]5[Mg--]5(n34)n3c(=CC1=[N+]25)c(C)c1C(=O)[C@H](C(=O)OC)C6=c31', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 17'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OCCCc1cc(OC)c2oc(cc2c1)-c1ccc2OCOc2c1', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 19'), ('O(CCCCCCCCCCCCC)C(=O)CCC1=CC=C(O)C=C1', 'Wax "
               'ester found with alcohol chain length 13 and acid chain length '
               "8'), ('O1CCCCCCCCCCCCC1=O', 'Wax ester found with alcohol "
               "chain length 13 and acid chain length 14'), "
               "('O(C(=O)CCCCCCCCC)C/C=C(\\\\CCC=C(C)C)/C', 'Wax ester found "
               "with alcohol chain length 8 and acid chain length 11'), "
               "('C1=2N3C(C=C4[N+]5=C(C=C6N7C8=C(C9=[N+](C(=C1)[C@H]([C@@H]9CCC(OC/C=C(/CCC[C@@H](CCC[C@@H](CCCC(C)C)C)C)\\\\C)=O)C)[Mg-2]735)[C-](C(C8=C6C)=O)C(=O)OC)C(=C4*)*)=C(C2*)*', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 15'), "
               "('O=C1OCC(C1)/C(=C/2\\\\[C@H](C=C)C[C@](C2)(CO)C)/CO', 'Wax "
               'ester found with alcohol chain length 8 and acid chain length '
               "10'), "
               "('O1C(CC(=O)C2=C1C=CC(=C2N)C(=O)CC(NC(=O)C)COC(=O)CCCCCCCCCCCCC(C)C)(C)C', "
               "'Wax ester found with alcohol chain length 11 and acid chain "
               "length 16'), "
               "('C1(CC(OC/C=C(/CC/C=C(/CCC=C(C)C)\\\\C)\\\\C)=O)=C(C)N(C2=C1C=C(C=C2)OC)C(C3=CC=C(Cl)C=C3)=O', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 8'), "
               "('O=C1C2=C([C@@]3(C(=O)C[C@@H]([C@]3([C@H]1O)C)C4(COC(C4)=O)C)C)[C@@H](O)C[C@@H]5[C@@]2(CC[C@@H](C5(C)C)O)C', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 14'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OCCCc1ccc2oc(cc2c1)-c1ccc2OCOc2c1', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 19'), "
               "('CCc1c(C)c2cc3[nH]c(cc4nc([C@@H](CCC(=O)OC\\\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)[C@@H]4C)c4[C@@H](C(=O)OC)C(=O)c5c(C)c(cc1n2)[nH]c45)c(C)c3C=C', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 17'), "
               "('O=C(OC[C@H](C1=C2C3=CC=C(C=O)C[C@@H]([C@@]3(CC[C@@]2(C)CC1)C)O)C)CCCCCCCCCCCCCCCCC', "
               "'Wax ester found with alcohol chain length 9 and acid chain "
               "length 19'), "
               "('O1C(CCC=2C1=C(C(=CC2OC)COC(=O)CCCCCCCCCCCCCCC)C=O)(CC(=O)C=C(C)C)C', "
               "'Wax ester found with alcohol chain length 13 and acid chain "
               "length 17'), "
               "('CC(O)c1c(C)c2\\\\C=C3/N=C([C@@H](CCC(=O)OC\\\\C=C(/C)CC\\\\C=C(/C)CCC=C(C)C)[C@@H]3C)C3=c4c(C(=O)C3)c([*])c3=CC5=N\\\\C(=C/c1n2[Mg]n43)\\\\C(C)=C5[*]', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 16'), "
               "('CCCCCCCCCCCCCCCCCC(=O)OC\\\\C=C(C)\\\\C=C\\\\C=C(C)\\\\C=C\\\\C1=C(C)CCCC1(C)C', "
               "'Wax ester found with alcohol chain length 13 and acid chain "
               "length 19'), "
               "('O=C1OC[C@]2([C@@]3(O[C@]45O[C@@]6(OC([C@H]([C@@H]([C@]4(C3)C)C)[C@@H]6O5)=O)C)[C@H]([C@@H](O)C[C@H]2C(O)(C)C)C)CC1', "
               "'Wax ester found with alcohol chain length 10 and acid chain "
               "length 13'), "
               "('[H]C(=O)c1c(C=C)c2\\\\C=C3/N=C(C=c4c(C)c5C(=O)[C@H](C(=O)OC)C6=c5n4[Mg]n2c1\\\\C=C1/N=C6[C@@H](CCC(=O)OC\\\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)[C@@H]1C)C(CC)=C/3C', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 17'), "
               "('C1CCC(=C(/C=C/C(=C\\\\C=C\\\\C(=C\\\\COC(CCCCCCCCCCCCC)=O)\\\\C)/C)C1(C)C)C', "
               "'Wax ester found with alcohol chain length 13 and acid chain "
               "length 15'), "
               "('Cl[C@@H]1[C@@H](O)C[C@@H](O)/C(=C/C=2N=C(C)SC2)/COC(=O)C[C@H](O)C(C([C@@H]([C@H]([C@H](CCC1)C)O)C)=O)(C)C', "
               "'Wax ester found with alcohol chain length 17 and acid chain "
               "length 20'), "
               "('Cl/C=C/1\\\\C=CC=2C(O)=C(COC(=O)CCCCCCCCCCCCCCC)C=CC2OC1', "
               "'Wax ester found with alcohol chain length 8 and acid chain "
               "length 17'), "
               "('COC(=O)[C-]1C(=O)c2c(C)c3=CC4=[N+]5C(=Cc6c(C=C)c(C)c7C=C8[C@@H](C)[C@H](CCC(=O)OC\\\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C9=[N+]8[Mg--]5(n67)n3c2=C19)C(C)=C4C=C', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 16'), "
               "('O=C1O[C@H]([C@H]([C@@H]2[C@@]3([C@@](C=4C([C@@]5([C@H](C(OC(=O)C)(C)C)CC4)COC(=O)CC5)=CC3)(C)CC2)C)C)CC=C1C', "
               "'Wax ester found with alcohol chain length 13 and acid chain "
               "length 16'), "
               "('[H][C@]1(COC(=O)C1)[C@@]1([H])CC[C@]2(O)[C@]3([H])CC[C@]4([H])C[C@H](CC[C@]4(C)[C@@]3([H])CC[C@]12C)O[C@H]1C[C@H](O)[C@H](O[C@H]2C[C@H](O)[C@H](O[C@H]3C[C@H](O)[C@H](O)[C@@H](C)O3)[C@@H](C)O2)[C@@H](C)O1', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 14'), ('O1CCCCCCCCC=CCCCCCC1=O', 'Wax ester found with "
               "alcohol chain length 16 and acid chain length 17'), "
               "('CCCCC\\\\C=C/C\\\\C=C/CCCCCCCC(=O)OCCCc1ccc2oc(cc2c1)-c1ccc2OCOc2c1', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 19'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](COC(=O)CCCCCCC\\\\C=C/C\\\\C=C/CCCCC)NC(C)=O', "
               "'Wax ester found with alcohol chain length 18 and acid chain "
               "length 19'), "
               "('O1C[C@@]2([C@]3([C@@]([C@@]4([C@@](CC3)(C([C@@H](O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)CO)CC4)(C)C)[H])C)(CC[C@@]2([C@H]([C@@H](OC(=O)C)C[C@H]6OC(=O)[C@@H](C6)C)C)[H])[H])C)CC1=O', "
               "'Wax ester found with alcohol chain length 10 and acid chain "
               "length 12'), "
               "('COc1cc2OC(=C)C(=O)Nc2c(c1)C(=O)O[C@H]1COC(=O)C[C@H](N)c2cc(O)c(O[C@@H]3c4ccc1cc4C1=CC=C[C@]31OC1OC(C)(C)C(C(O)C1O)N(C)C)c(Cl)c2', "
               "'Wax ester found with alcohol chain length 9 and acid chain "
               "length 8'), "
               "('CCCCCCCCCCCC(=O)OC\\\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 13'), ('O(CCCCCCCC)C(=O)CCCCCCCCC', 'Wax ester found "
               "with alcohol chain length 8 and acid chain length 11'), "
               "('O1CCCCCCCCCCCCCCCCCCCCCC1=O', 'Wax ester found with alcohol "
               "chain length 22 and acid chain length 23'), "
               "('O1C(CC(=O)C2=C1C=CC(=C2N)C(=O)CC(NC(=O)C)COC(=O)CCCCCCCC/C=C/C=C/CCCCC)(C)C', "
               "'Wax ester found with alcohol chain length 11 and acid chain "
               "length 19'), "
               "('[H][C@@]1(CCC(=O)OC1)[C@@]1([H])CC[C@]2([H])[C@]3([H])CC[C@]4([H])CCCC[C@]4(C)[C@@]3([H])CC[C@]12C', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 15'), "
               "('O1C(CCC=2C1=C(C(=CC2OC)COC(=O)CCCCCCC/C=C/C/C=C/CCCCC)C=O)(CC(=O)C=C(C)C)C', "
               "'Wax ester found with alcohol chain length 13 and acid chain "
               "length 19'), "
               "('O=C1OCC2=CC(O)=CC(=C2)CC(=CC=C[C@@H](C(C[C@@H]([C@H](C=C([C@H](C1)O)C)C)O)=O)OC)C', "
               "'Wax ester found with alcohol chain length 19 and acid chain "
               "length 20'), "
               "('[H][C@]12C=C(COC(=O)CCCCCCCCCCCCCCC)[C@@H](O)[C@]3(O)[C@@H](OC(=O)C(C)C(C)C)C(C)=C[C@]3([C@H](C)C[C@]3(OC(=O)CCCCCCCCCCC)[C@@]1([H])C3(C)C)C2=O', "
               "'Wax ester found with alcohol chain length 8 and acid chain "
               "length 17'), ('O1C=2CCCCCOC(=O)CCC1=C(C2C)C', 'Wax ester found "
               "with alcohol chain length 12 and acid chain length 13'), "
               "('[C@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)(NC(=O)CCCCCCCCCCCCCCCCCCCCCCCCCCCOC(CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)CO', "
               "'Wax ester found with alcohol chain length 28 and acid chain "
               "length 19'), "
               "('[H][C@]12CCC=C(C)[C@]1(C)[C@@H](OC(=O)c1cccnc1)[C@H](OC(=O)c1cccnc1)[C@]1(C)O[C@@]3(COC(=O)C3)C[C@H](OC(=O)c3cccnc3)[C@]21C', "
               "'Wax ester found with alcohol chain length 9 and acid chain "
               "length 11'), "
               "('C[C@]12C[C@H](O)[C@H]3[C@@H](CCC4=CC(=O)C=C[C@]34C)[C@@H]1CC[C@]2(O)C(=O)COC(=O)CCCc1ccc(cc1)N(CCCl)CCCl', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 9'), ('CCCCCCCCCCCCCCCC(=O)OCC(O)CCCCCCCCCCCCCC', 'Wax "
               'ester found with alcohol chain length 16 and acid chain length '
               "17'), ('O1CCCCCCCCCCCCCCCCCCCC1=O', 'Wax ester found with "
               "alcohol chain length 20 and acid chain length 21'), "
               "('O=C1C(=C2[C@@](CC2)(C)C3=C1C[C@](COC(=O)CCCCCCCCCCCCCCCCC)(C)C3)C', "
               "'Wax ester found with alcohol chain length 8 and acid chain "
               "length 19'), "
               "('[H][C@]1(COC(=O)C1)[C@@]1([H])CC[C@]2([H])[C@]3([H])CC[C@]4([H])CCCC[C@]4(C)[C@@]3([H])CC[C@]12C', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 14'), "
               "('O=C(OCC(O)([C@@H]1C[C@H]2[C@H](CC[C@H]2C)[C@@](CC1)(O)C)C)CCCCCCCCCCCCCCC', "
               "'Wax ester found with alcohol chain length 8 and acid chain "
               "length 17'), "
               "('[H]C(C)=C1C(C)C2=CC3=C(C(C)=O)C(C)=C4C=C5[C@@H](C)[C@H](CCC(=O)OC\\\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C6=[N+]5[Mg--]5(N34)N3C(=CC1=[N+]25)C(C)=C1C(=O)[C@H](C(=O)OC)C6=C31', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 17'), "
               "('O=C1C2=C(O[C@](C1)([C@@H](O)[C@H]3COC(C3)=O)CO)C=CC=C2O', "
               "'Wax ester found with alcohol chain length 10 and acid chain "
               "length 12'), ('O(CCC(CCC=C(C)C)C)C(=O)CC(CCCC(C)C)C', 'Wax "
               'ester found with alcohol chain length 8 and acid chain length '
               "9'), "
               "('C12=CC(=C(C=C1N=C3C(=C2)CN4C(C5=C(C=C43)[C@](CC(OC5)=O)(CC)O)=O)F)F', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 14'), "
               "('[H][C@]1(COC(=O)C1)[C@@]1([H])CC[C@]2([H])[C@]3([H])CC[C@@]4([H])CCCC[C@]4(C)[C@@]3([H])CC[C@]12C', "
               "'Wax ester found with alcohol chain length 12 and acid chain "
               "length 14'), ('O(CCCCCCCC)C(=O)CCCCCC', 'Wax ester found with "
               "alcohol chain length 8 and acid chain length 8'), "
               "('O(CCCCCCC(C)C)C(=O)CCCCCC(C)C', 'Wax ester found with "
               "alcohol chain length 8 and acid chain length 9'), "
               "('O=C1OC[C@@H]2CC=C3[C@@H]([C@]2(CC1)C)CC[C@]4([C@H]3CC[C@@H]4[C@@H]([C@@H](O)[C@@H](O[C@@H]5O[C@@H]([C@@H](O)[C@@H]([C@@H]5O)O)CO)[C@@H](C(C)C)C)C)C', "
               "'Wax ester found with alcohol chain length 14 and acid chain "
               "length 16'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](COC(=O)CCCCCCC\\\\C=C/CCCCCCCC)NC(C)=O', "
               "'Wax ester found with alcohol chain length 18 and acid chain "
               "length 19'), "
               "('CCCCCCCCCCCCCCCC(=O)OC\\\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 17'), ('O1CCCCCCCCC1=O', 'Wax ester found with alcohol "
               "chain length 9 and acid chain length 10'), "
               "('COC(=O)[C@H]1C(=O)c2c(C)c3C=C4C(C=C)=C(C=O)C5=[N+]4[Mg--]46n3c2C1=C1[C@@H](CCC(=O)OC\\\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)[C@H](C)C(C=c2c(C)c(C=C)c(=C5)n42)=[N+]61', "
               "'Wax ester found with alcohol chain length 16 and acid chain "
               "length 16'), "
               "('[H][C@]12O[C@@]1(COC(=O)CCCCCCCCCCCCCCC)[C@@H](O)[C@]1(O)[C@@H](OC(=O)C(C)C(C)C)C(C)=C[C@@]11[C@H](C)C[C@]3(OC(=O)CCCCCCCCCCC)[C@]([H])([C@@]2([H])C1=O)C3(C)C', "
               "'Wax ester found with alcohol chain length 8 and acid chain "
               "length 17')]\n"
               "False negatives: [('*C(O*)=O', 'No ester group found')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 10,
    'num_false_positives': 46,
    'num_true_negatives': 183779,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.17857142857142858,
    'recall': 0.9090909090909091,
    'f1': 0.2985074626865672,
    'accuracy': 0.9997443373441546}