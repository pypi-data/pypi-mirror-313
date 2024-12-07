"""
Classifies: CHEBI:142348 hexahydronaphthalenes
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetSymmSSSR

def is_hexahydronaphthalenes(smiles: str):
    """
    Determines if a molecule is a hexahydronaphthalene or derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hexahydronaphthalene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Get ring information
    rings = mol.GetRingInfo()
    if rings.NumRings() < 2:
        return False, "Molecule does not contain bicyclic system"
        
    # Find fused 6-membered rings
    fused_rings = []
    ring_atoms = rings.AtomRings()
    
    # Check for pairs of 6-membered rings
    for i, ring1 in enumerate(ring_atoms):
        if len(ring1) != 6:
            continue
        for j, ring2 in enumerate(ring_atoms[i+1:], i+1):
            if len(ring2) != 6:
                continue
                
            # Check if rings share exactly 2 atoms (fused)
            shared = set(ring1).intersection(set(ring2))
            if len(shared) == 2:
                fused_rings.append((ring1, ring2))
                
    if not fused_rings:
        return False, "No fused 6-membered ring system found"
        
    # For each fused ring pair, check if at least one ring has significant saturation
    for ring1, ring2 in fused_rings:
        ring1_atoms = [mol.GetAtomWithIdx(i) for i in ring1]
        ring2_atoms = [mol.GetAtomWithIdx(i) for i in ring2]
        
        # Count number of sp3 carbons in each ring
        ring1_sp3 = sum(1 for atom in ring1_atoms if atom.GetHybridization() == Chem.HybridizationType.SP3)
        ring2_sp3 = sum(1 for atom in ring2_atoms if atom.GetHybridization() == Chem.HybridizationType.SP3)
        
        # Check if at least one ring has significant saturation (4 or more sp3)
        if ring1_sp3 >= 4 or ring2_sp3 >= 4:
            # Get substituents
            all_ring_atoms = set(ring1).union(set(ring2))
            substituents = []
            
            for atom_idx in all_ring_atoms:
                atom = mol.GetAtomWithIdx(atom_idx)
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetIdx() not in all_ring_atoms:
                        substituents.append(neighbor.GetSymbol())
                        
            if len(substituents) > 0:
                return True, f"Substituted hexahydronaphthalene with substituents: {', '.join(sorted(set(substituents)))}"
            else:
                return True, "Unsubstituted hexahydronaphthalene"
                
    return False, "No hexahydronaphthalene core structure found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:142348',
                          'name': 'hexahydronaphthalenes',
                          'definition': 'Any carbobycyclic compound that is an '
                                        'hexahydronaphthalene or a compound '
                                        'obtained from an hexahydronaphthalene '
                                        'by formal substitution of one or more '
                                        'hydrogens.',
                          'parents': ['CHEBI:36785']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.019417475728155338 is too low.\n'
               'True positives: '
               "[('[H][C@@]12C[C@H](C)C[C@H](C(O)=O)[C@@]1([H])[C@](C)(C(=O)CCO)C([C@H](C)CCCC)=C(O)C2=O', "
               "'Substituted hexahydronaphthalene with substituents: C, O')]\n"
               'False positives: '
               "[('O=C1C(=O)C2=C([C@]34C(=O)C=5C=C(C)C=C(C5C([C@@]4(C2)[C@@H](O)[C@H](O)C=C3)=O)O)C(=C1C[C@H]6C(=C)CC[C@@H]7[C@@]6(CC[C@H](C7(C)C)O)C)O', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('C[C@@H]([C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('C[C@H](C[C@H]([C@@H](C(C)(C)O[C@H]1[C@@H]([C@H]([C@@H]([C@@H](CO)O1)O)O)O)O)O)[C@]2(CC[C@@]3(C)[C@@]4(CC=C5[C@](CC[C@@H](C5(C)C)O[C@H]6[C@@H](C([C@@H]([C@@H](CO[C@H]7[C@@H]([C@H]([C@@H]([C@@H](CO)O7)O)O)O)O6)O)O)O)([H])[C@]4(C)CC[C@]23C)[H])[H]', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O=C(O[C@H]1[C@@]2([C@]3(C=CC(C)=C[C@H]3O[C@H](C1)[C@]24OC4)C)C)/C=C\\\\C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('[H][C@@]12CC[C@@]3(C)[C@]4([H])CCC5=C(C(=O)OC5)[C@@]4(C)[C@H](O)C[C@]3([H])[C@@]1(C)CCC[C@@]2(C)CO', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('OC(=O)C(F)(F)F.[H][C@]12C[C@H](O)CC[C@@]11CCN2Cc2cc(O)c(OC)cc12', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('[H][C@@]12CC=C3C[C@@H](O)CC[C@]3(C)[C@@]1([H])CC[C@]1(C)[C@H](CC[C@@]21[H])C(C)=O', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('[H][C@]12CC[C@]3([H])C(C)(C)[C@H](O)CC[C@@]3(C)[C@]1([H])C(=O)C=C(C=C)[C@H]2C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O=C1[C@@]2([C@@H](C(=C)CC1)C[C@@H](C(O)(C)C)CC2)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('C1[C@@]([C@@]2([C@@](C1)(C3=CC[C@@]4([H])[C@H](C)[C@@H](O)CC[C@]4(C)[C@]3(CC2)[H])[H])C)([C@H](C)CC/C(=C/C)/C(C)C)[H]', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O=C(O[C@H]1[C@@]2([C@@]3([C@@H](C=C(C)CC3)O[C@H]([C@@H]1O)[C@]24OC4)C)C)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('[H][C@@]12CCC(=C)[C@H](C[C@H](O)[C@](C)(O)C=C)[C@@]1(C)CCC[C@]2(C)C(O)=O', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O(C1CC=2C(C3C(C4C(C(CC4)C(CCCC(C)C)C)(CC3)C)CC2)(CC1)C)C(=O)CCCCCCCCC', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('CC(=O)[C@H]1CC[C@H]2[C@@H]3CC[C@H]4CC(=O)CC[C@@H]4[C@H]3CC[C@]12C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O(C1C(C2C(C3C(C4(C(C5C(C(O)C4)(CCC(C5)(C)C)C(O)=O)=CC3)C)(CC2)C)(CC1)C)(C)C)C6OC(C(O)C(O)C6O)COC7OCC(O)C(O)C7O', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O[C@]12[C@@]([C@](CC1)([C@@](O)([C@H](O)CCC(C)C)C)[H])(CC[C@@]3([C@@]4([C@@](C[C@@H](O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)CO)[C@@H](O)C4)(C(=O)C=C23)[H])C)[H])C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O1C2C(C3C(CC2)(C(C(CC3)=C)CC4=C(O)C(=C(OC4=O)C)C)C)(CCC(OC(=O)/C=C/C=C/C=C/C(CC)C)C1(C)C)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O(C1CC=2C(C3C(C4C(C(CC4)C(CC/C(/C(C)C)=C\\\\C)C)(CC3)C)CC2)(CC1)C)C5OC(C(O)C(O)C5O)COC(=O)CCCCCCCCCCCCCCC', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O=C1C=C[C@@]23[C@H](O)C[C@@H](CC2[C@@]1(CCC(=O)NC4=C(O)C(C(=O)OC)=CC=C4O)C)C(C3)=C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCC(=O)O[C@H]1CC[C@]2(C)[C@H]3CC[C@]4(C)[C@H](CC[C@H]4[C@@H]3CC=C2C1)[C@H](C)CCCC(C)C', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O1C2C34C5(OC6C2C(C1C3=C(C(=O)C5(O)C7C4C(=O)C89C(C(NC8=O)CC(C)C)C(C(=CC9C=C(CCC(=O)C7=O)C)C)C)C)C(=O)C%10%11C(C(NC%10=O)CC(C)C)C(C(=CC%11C=C(CCC6O)C)C)C)O', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O1[C@H]2O[C@@H]3[C@]4([C@@H](C5=C(C(C)C)C[C@@H]([C@]5(C)CC4)O)CC=C6[C@H]3[C@@]2(O)[C@]7(O[C@@H]6O[C@]7(C1)O)O)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)C=C[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)\\\\C=C\\\\CC(C)C', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('C1C[C@]2([C@]([C@]([C@H]1O)(C)CO)(CC[C@@]3([C@@]2(CC=C4[C@]3(CC[C@@]5([C@]4(CC(CC5)(C)C)[H])C([O-])=O)C)[H])C)[H])C', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O=C1N(C(CC(O)(C(=O)O)C(CC)C)C(C1=C(O)/C=C/[C@@H]2[C@@H]3[C@@H](C=C[C@@H]2C)CCCC3)=O)C', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('[H][C@@]12CCC3=CC(=O)C=C[C@]3(C)[C@@]1([H])[C@@H](O)C[C@@]1(C)[C@@]2([H])C[C@H]2OC(CCC)O[C@@]12C(=O)CO', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O=C1OCC=2C1(O)[C@@]3([C@H](C(CCC3)(C)C)[C@@H](C2)OC(=O)CCCCC)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O=C(O)[C@@]1([C@@H](O)CC[C@]2([C@H]1CCC3=C2C=C4C5=C(C=CC=C5)N(C4=C3)C6=CC7=C(NC8=C7C=C9[C@@]%10([C@H]([C@](C(=O)O)([C@@H](O)CC%10)C)CCC9=C8)C)C=C6)C)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)[C@@H](O)[C@H](O)[C@@H](C)C(C)C', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('C[C@@H]1C[C@H]2CC3=C(CCC(=O)N3)[C@@]3(C1)[C@@H]2CCCN3C', "
               "'Substituted hexahydronaphthalene with substituents: C, N'), "
               "('[H][C@]12C(C)(C)CCC[C@@]11C(=O)O[C@]2(O)C(=O)C2=C[C@](C)(C[C@@H](O)[C@]12O)C=C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('F[C@@]12[C@]([C@]3([C@@](C[C@@H]1O)(C)[C@](CC3)(C(COC(C)=O)=O)OC(C)=O)[H])(C[C@H](C=4[C@]2(C)C=C(C(C4)=O)Br)F)[H]', "
               "'Substituted hexahydronaphthalene with substituents: F, C, "
               "O'), "
               "('[H][C@@]1(CC[C@@]2([H])[C@]3([H])[C@H](O)C=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@H](C)CCCC(C)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('[H][C@]12C[C@@]3([H])C(=COC[C@@]3([H])[C@]([H])(Cc3c1n(C)c1cc4O[C@]5(C)OC[C@@]6([H])[C@]7([H])Cc8c(n(C)c9ccccc89)[C@]([H])(C[C@@]6([H])[C@]5([H])Cc4cc31)N7C)N2C)C(C)=O', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O[C@@H]1[C@@]([C@]2([C@@]([C@@]3([C@]([C@]4(C([C@]5([C@@](CC4)(CCC(C5)(C)C)C(O)=O)[H])=CC3)C)(CC2)C)[H])(C[C@@H]1O)C)[H])(C)C(O)=O', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O=C1O[C@@H](C)[C@@]2([C@@]13C(=C)[C@](C[C@@H]4[C@@]3(CC[C@@H]([C@]4(CCC(=O)OC)C)C(O)(C)C)C)(C)C2=O)O', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O1[C@H]2C(=CC[C@H]3[C@H]2[C@]4(OC(C)(C)O[C@H]4C[C@@H]3C)[C@@H](C1)CO)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('C/C=C\\\\1/CN2CC[C@@]34C5=CC=CC=C5N6[C@]4(C(C=C([C@H]7C[C@@]89C%10=CC=CC=C%10N%11C(C=C[C@@]([C@]/%12(C[C@@]8(N7C\\\\C%12=C\\\\C)[H])[H])([C@@]9%11[H])[H])=O)C6=O)[C@]1(C[C@@]32[H])[H])[H]', "
               "'Substituted hexahydronaphthalene with substituents: C, O, "
               "N'), "
               "('Cl[C@H]1[C@](C=C)([C@]2([N+]#[C-])[C@]3(O)C=4C=5C(=CC=CC5C([C@H]3C1)(C)C)NC4C([C@H]([C@@H]2O)O)(C)C)C', "
               "'Substituted hexahydronaphthalene with substituents: Cl, C, O, "
               "N'), "
               "('O[C@]1([C@H]2[C@@]([C@@H]3C(C[C@](CCO)(C)C[C@H]3O)=CC2)(CCC1)C)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O[C@@H]1CC=2[C@@]([C@@]3([C@]([C@]4([C@@]([C@@]([C@@H]([C@@]5([C@](C5)([C@@H](C(C)C)C)C)[H])C)(CC4)[H])(CC3)C)[H])(CC2)[H])[H])(CC1)C', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O1C2C(C3(C(C4C(CC3)C5(C(=CC4)CC(O)CC5O[C@@H]6OC[C@H](OC(=O)C(O)C(CC)C)[C@H](O)[C@H]6O[C@@H]7O[C@H]([C@H](O)[C@@H](O)[C@H]7O)C)C)C2)C)C(C18OCC(CC8)=C)C', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O[C@H]1C[C@]2([C@]3([C@@]([C@@]4([C@@](CC3)(C([C@@H](O)CC4)(C)C)[H])C)(CC[C@@]2([C@]5([C@@]1([C@@H](O)C=C([C@H]5C)C)C)[H])[H])[H])C)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('COC(=O)[C@@]1(C)CC[C@@]2(CC[C@]3(C)C(=CC[C@@H]4[C@@]5(C)C[C@H](O)[C@H](O[C@@H]6OC[C@@H](O)[C@H](O)[C@H]6O)[C@@](C)(CO)[C@@H]5CC[C@@]34C)[C@@H]2C1)C(O)=O', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O[C@@]1([C@@]2([C@]([C@]3([C@@]([C@@]4(C(CC3)=CC(=O)CC4)C)(CC2)[H])[H])(CC1)[H])C)CC', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('Cl[C@H]1C[C@]2([C@]3([C@@]([C@H]([C@@H](C3)C)C(=O)C)(CC[C@@]2([C@@]4(C1=CC(=O)CC4)C)[H])C)[H])[H]', "
               "'Substituted hexahydronaphthalene with substituents: Cl, C'), "
               "('O=C1OCC=2C1=C(O)C3=C(O[C@@]4(CC[C@@H]5[C@@]([C@H]4C3)(CC[C@H](C5(C)C)O)C)C)C2C', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O=C1[C@@H]([C@]2(CC=C3C([C@@]2(C1)C)=CC[C@@H]4[C@@]3(CC[C@@H](C4(C)C)O)C)C)[C@H](C(=O)O)CCC=C(C)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O=C1C2([C@@]3([C@@H](C=C(C)[C@H](C3)O)O[C@H](C1)[C@@]24OC4)C)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('OC1C(C2C(C3C(C4(C(=C5C(CC4)(CCC(C5)(C)C(OC)=O)C)C=C3)C)(CC2)C)(CC1)C)(CO)C', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC=C2C[C@H](C1)O)[H])(CC[C@@]4([C@H](C)CCCC(C)C)[H])[H])C)[H])C', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('C(COC(CC)=O)(=O)[C@]1(OC(CC)=O)[C@]2(C)[C@@](C[C@H]1C)([C@]3([C@@]([C@H](C2)O)(F)[C@]4(C)C(CC3)=CC(C=C4)=O)[H])[H]', "
               "'Substituted hexahydronaphthalene with substituents: F, C, "
               "O'), "
               "('[H][C@@]12[C@H](O)[C@H](OC(C)=O)[C@@]3(C)O[C@](C)(CC(=O)[C@]3([H])[C@@]1(C)[C@@H](O)CCC2(C)C)C=C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O1[C@@]2([C@@]([C@@]3([C@](O)([C@]4([C@](CC3)([C@@]5(C(=CC4)C[C@@H](O)CC5)C)[H])[H])C2)C)([C@@H]([C@]16OC[C@@H](CC6)C)C)[H])[H]', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('[H][C@@]1(CC[C@@]2([H])[C@]3([H])CCC4=CC(=O)CC[C@]4(C)[C@@]3([H])CC[C@]12C)[C@@H](C)O', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('[H][C@@]1(C[C@]2([H])N(CCc3c2[nH]c2ccccc32)C[C@@H]1CC)C(=C/OC)\\\\C(=O)OC', "
               "'Substituted hexahydronaphthalene with substituents: C, N'), "
               "('[H][C@@]1(C[C@]1([H])[C@@H](C)[C@@]1([H])CC[C@]2([H])[C@]1(C)CC[C@]1([H])[C@@]3(C)CC[C@H](O)C[C@@]33OO[C@@]21C=C3)[C@H](C)C(C)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O[C@@H]1[C@H]([C@]2([C@@](C3=C(C4[C@@]([C@](CC4)([C@@H](CCC=C(C)C)C)[H])(CC3)C)CC2)(CC1)C)[H])C(O)=O', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O=C(O)[C@@H]([C@@H]1[C@@]2([C@@](C3=C([C@@]4([C@H](C([C@H](OC(=O)C[C@@](O)(CC(=O)OC)C)CC4)(C)C)CC3)C)CC2)(C)[C@H](C1)O)C)CCC=C(C)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('C[C@@]12CC[C@H]3C(=CC[C@H]4C(C)(C)[C@H](O)CC[C@]34C)[C@@]1(C)CC[C@H]2C1COC(=O)C1', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('[C@@H]1(C[C@H](C([C@]2([H])[C@]1(C)[C@@]3(C(C=C([C@H]([C@]3(CC2)[H])C)C=C)=O)[H])(C)C)O)O', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O=C1OCC=2[C@@]1(O)[C@@]3([C@H](C(CCC3)(C)C)[C@@H](C2)OC(=O)/C=C/C=C/CC(O)C)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('[H][C@]1(OC[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1[C@@H](O)[C@H](O)[C@@H](CO)O[C@@]1([H])O[C@@H]1[C@@H](O)[C@@H](O)[C@@H](C)O[C@@]1([H])O[C@H]1CC[C@@]2(C)[C@@]([H])(CC[C@]3(C)[C@]2([H])C=C[C@]24OC[C@@]5(CC[C@@H](C)[C@H](C)[C@@]25[H])[C@H](O)C[C@@]34C)C1(C)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O[C@@H]1CC=2[C@@](C3C(C4[C@@]([C@](CC4)([C@H](C)C(=O)CCC(C)C)[H])(CC3)C)CC2)(CC1)C', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('ClC1=C2C(=CC3=C1NC=4C=CC=CC34)[C@@]5([C@H]([C@](C(=O)O)([C@@H](O)CC5)C)CC2)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('S(OC1=CC2=C([C@@]3([C@]([C@]4([C@](CC3)(CCC4)C)[H])(CC2)[H])[H])C=C1)(O)(=O)=O', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O=C1OCC23C4(C5(OC5)C(OC2C=C(C)CC3)C(C4OC(=O)C=CC=CC(OCCC(=C1)C)C(O)C)O)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('[H][C@@]12CCC3=CC(=O)CC[C@]3(C)[C@@]1([H])CC[C@@]1(C)[C@@]2([H])CC[C@]1(O)[C@@H](C)O', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O=C1C2=C(O)C=C(OC)C=C2C(=O)[C@@]3([C@]1(O)[C@H](O[C@@H](C3)CC(=O)N)CCC)O', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('CC(C)C1=C[C@@]23CC[C@@H]4[C@@](CCCC4(C)C)(C(=O)O2)C3=CC1=O', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('C[C@@]12[C@]3(CC[C@]1([C@]4([C@](CC2)([C@]5(C)C(C=C4)=CC(CC5)=O)[H])[H])[H])OC(CC3)=O', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O[C@@H]1[C@]2(C(=C3[C@@]([C@@]4([C@](CC3)(C[C@H](O)CC4)[H])C)(C1)[H])[C@H](O)C[C@@]2([C@@H](CCC(O)=O)C)[H])C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('[H][C@]1(OC[C@@H](O[C@]2([H])O[C@H](CO)[C@H](O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O)O[C@H]1[C@H](C)O[C@@]([H])(O[C@@H]2[C@@H](O)[C@@H](OC(=O)\\\\C=C\\\\c3ccc(OC)cc3)[C@@H](C)O[C@H]2OC(=O)[C@]23CCC(C)(C)C[C@@]2([H])C2=CC[C@]4([H])[C@@]5(C)C[C@H](O)[C@H](O[C@]6([H])O[C@H](CO)[C@@H](O)[C@H](O)[C@H]6O)[C@@](C)(C(O)=O)[C@]5([H])CC[C@@]4(C)[C@]2(CO)CC3)[C@H](O)[C@@H]1O[C@]1([H])OC[C@](O)(CO)[C@H]1O', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O=C1N[C@@](OC)(CC(C)C)C=C1C(=O)[C@H]2[C@H](C(=C[C@@]3([C@@H]2CC[C@@H](C3)C)C)C)/C(=C/C)/C', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('[H][C@@]12CC(C)(C)CC[C@@]1(CC[C@]1(C)C2=CC[C@]2([H])[C@@]3(C)CC[C@H](O[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@@H]5O[C@@H](C)[C@H](O)[C@@H](O)[C@H]5O)[C@H]4O)C(O)=O)[C@@](C)(C=O)[C@]3([H])CC[C@@]12C)C(O)=O', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O=C1[C@](OC[C@@]2([C@]1([C@@H]3[C@H](C[C@@H](C)CC3)C=C2)C)O)(O)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('OC1C(C2C3C(C4(C(C5(C(CC4)C(C(=O)CC5)(C)C)C)CC3)C)(CCC2(CC1)C)C)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('C1=CC(C=C2[C@]1([C@@]3([C@@](C[C@@]2(F)[H])([C@]4([C@@](C[C@@]3(O)[H])(C)[C@]5([C@@](C4)(OC(O5)(C)C)[H])C(=O)COC(C)=O)[H])[H])F)C)=O', "
               "'Substituted hexahydronaphthalene with substituents: F, C, "
               "O'), "
               "('O1[C@@]2(OC(C)(C)[C@H]([C@H]2O)C)[C@H]([C@@H]3[C@@]4([C@@]1(C5=C(C(=C(O)C=C5)C)CC4)CC3)C)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('[H][C@@]1(CC[C@@]2([H])[C@]3([H])C=CC4=CC(=O)CC[C@]4(C)[C@@]3([H])C[C@H](O)[C@]12C)[C@H](C)CCC([O-])=O', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('Oc1ccc2C[C@H]3N(CC4CC4)CC[C@@]45[C@@H](Oc1c24)c1[nH]c2ccccc2c1C[C@@]35O', "
               "'Substituted hexahydronaphthalene with substituents: C, O, "
               "N'), "
               "('O=C1O[C@@H]2[C@H]3O[C@@]3(C=O)C([C@@]4([C@@H]2[C@@]1(CCC4)C)C)=CC(=O)OC', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('[H][C@@]12CC[C@](O)(C(=O)CO)[C@@]1(C)C[C@H](O)[C@@]1([H])[C@@]2([H])C[C@@H](O)C2=CC(=O)C=C[C@]12C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('CC(C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)=C1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O[C@@]1([C@@H]2[C@](CCC(C2)=C(CO)C)(CCC1)C)C', 'Substituted "
               "hexahydronaphthalene with substituents: C, O'), "
               "('[H][C@]12CC[C@@]3(C)[C@@]([H])(CC[C@@]33CCC(=O)O3)[C@]1([H])[C@@H](CC1=CC(=O)CC[C@]21C)SC(C)=O', "
               "'Substituted hexahydronaphthalene with substituents: C, S'), "
               "('O([C@@H]1C([C@]2([C@@]([C@@]3([C@]([C@]4(C([C@]5([C@@](CC4)(CCC(C5)(C)C)C(O)=O)[H])=CC3)C)(CC2)C)[H])(CC1)C)[H])(C)C)[C@@H]6O[C@@H]([C@@H](O)[C@H](O[C@H](OCC(O)=O)[C@H](O)C(O)=O)[C@H]6O)C(O)=O', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('[H][C@@]12CC[C@]3(C)[C@]([H])(CC=C4[C@]5([H])[C@@H](C)C(=C)CC[C@@]5(CC[C@@]34C)C(O)=O)[C@@]1(C)C[C@@H](O)[C@H](O)[C@@]2(C)CO', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('C[C@]12CC[C@H]3[C@@H](CC(=C(Br)Br)C4=CC(=O)CC[C@]34C)[C@@H]1CC[C@@H]2O', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('O=C(O[C@@H](C(O)(C)C)C[C@@H](O)[C@H]([C@@H]1[C@@]2([C@@](C3=C([C@@]4([C@H](C([C@@H](O)CC4)(C)C)CC3)C)CC2)(C)CC1)C)COC(=O)C)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O=C1OC[C@]2(C1=CC[C@H]3C(CC[C@@H]([C@]23C)OC(=O)[C@@H](NC(=O)C)C(C)C)(C)C)O', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O=C1O[C@@H]2[C@@](O[C@@H](C)[C@@H]([C@H]2C)OC(=O)/C=C\\\\C(=O)CCCCCC)(C)[C@H]([C@H]1C)OC(=O)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('CC(=O)O[C@@H]1C[C@H]2C(C)(C)C(=O)C=C[C@]2(C)[C@H]2CC[C@]3(C)[C@@H](C(=O)C(O)=C3c3ccoc3)[C@]12C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('C12=CC=C(C=C1CC[C@@]3([C@@]2(CC[C@]4([C@]3(C[C@H]([C@H]4O)O)[H])C)[H])[H])O', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('C[C@@H]1CC2(SCC=N2)[C@]2(O)O[C@@H]3C[C@@]4(C)[C@@H](C[C@@H]5O[C@]55[C@@H]4[C@H](O)C(=O)[C@]4(C)[C@H](CC[C@]54O)C4=CC(=O)OC4)C[C@H]3O[C@@H]2O1', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('C[C@](O)(CC[C@@H]1C(=C)CC[C@@H]2C(C)(C)CCC[C@@]12C)C=C', "
               "'Substituted hexahydronaphthalene with substituents: C'), "
               "('[H][C@]12CC[C@]3([H])[C@@]4(C)CCC(=O)C(C)(C)[C@]4([H])CC[C@@]3(C)[C@]1(C)CC[C@]1(O)CC[C@H](O[C@]21[H])C(C)(C)O', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('O=C(OC[C@]1(O)[C@H]2[C@@H](C=3[C@@]4([C@H]([C@@]([C@H](O)CC4)(CO)C)CCC3C2)C)CC1)C', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('CC(C)C[C@@H]1CN2CCC3=CC(=C(C=C3[C@H]2C[C@H]1O)OC)O', "
               "'Substituted hexahydronaphthalene with substituents: C, O'), "
               "('[H][C@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@H]1[C@H](O)[C@@H](CO[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O[C@]2([H])O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)O[C@@H](OC(=O)[C@]23CCC(C)(C)C[C@@]2([H])C2=CC[C@]4([H])[C@@]5(C)CC[C@H](O)[C@@](C)(C(=O)O[C@@H]6O[C@H](CO)[C@@H](O)[C@H](O)[C@H]6O)[C@]5([H])CC[C@@]4(C)[C@]2(C)C[C@H]3O)[C@@H]1O', "
               "'Substituted hexahydronaphthalene with substituents: C, O')]\n"
               'False negatives: '
               "[('[C@@]12([C@@H](OC([C@H](CC)C)=O)C[C@H](O)C=C1C=C[C@@H]([C@@H]2CC[C@H]3OC(C[C@@H](C3)O)=O)C)[H]', "
               "'No hexahydronaphthalene core structure found')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 895,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.8996990972918756}