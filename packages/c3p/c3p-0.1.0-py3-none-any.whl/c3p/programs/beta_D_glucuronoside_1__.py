"""
Classifies: CHEBI:132367 beta-D-glucuronoside(1-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_beta_D_glucuronoside_1__(smiles: str):
    """
    Determines if a molecule is a beta-D-glucuronoside(1-) derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a beta-D-glucuronoside(1-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of carboxylate anion [O-]
    if '[O-]' not in smiles:
        return False, "No carboxylate anion found"

    # Check for pyranose ring (6-membered ring with 5 carbons and 1 oxygen)
    rings = mol.GetRingInfo()
    pyranose_rings = []
    
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            atom_symbols = [atom.GetSymbol() for atom in atoms]
            if atom_symbols.count('C') == 5 and atom_symbols.count('O') == 1:
                pyranose_rings.append(ring)

    if not pyranose_rings:
        return False, "No pyranose ring found"

    # For each potential pyranose ring
    for ring in pyranose_rings:
        # Get ring atoms
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        
        # Find oxygen atom in ring
        ring_oxygen = None
        for atom in ring_atoms:
            if atom.GetSymbol() == 'O':
                ring_oxygen = atom
                break
                
        if ring_oxygen is None:
            continue

        # Count OH groups on carbons
        oh_count = 0
        carboxylate_found = False
        has_glycosidic_bond = False
        
        for atom in ring_atoms:
            if atom.GetSymbol() == 'C':
                for neighbor in atom.GetNeighbors():
                    # Check for OH groups
                    if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 1:
                        oh_count += 1
                    # Check for carboxylate group
                    elif neighbor.GetSymbol() == 'C':
                        for n2 in neighbor.GetNeighbors():
                            if n2.GetSymbol() == 'O' and n2.GetFormalCharge() == -1:
                                carboxylate_found = True
                    # Check for glycosidic bond
                    elif neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 0:
                        non_ring_bonds = [b for b in neighbor.GetBonds() if not b.IsInRing()]
                        if len(non_ring_bonds) > 0:
                            has_glycosidic_bond = True

        # Need 3 OH groups, carboxylate, and glycosidic bond
        if oh_count >= 3 and carboxylate_found and has_glycosidic_bond:
            # Check for beta configuration
            # Look for specific stereochemistry patterns in SMILES
            if ('O[C@@H]' in smiles or 'O[C@H]' in smiles) and ('[C@@H]' in smiles or '[C@H]' in smiles):
                return True, "Found beta-D-glucuronoside(1-) structure"

    return False, "Missing required structural features of beta-D-glucuronoside(1-)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:132367',
                          'name': 'beta-D-glucuronoside(1-)',
                          'definition': 'A carbohydrate acid derivative anion '
                                        'obtained by deprotonation of the '
                                        'carboxy group of any '
                                        'beta-D-glucuronoside.',
                          'parents': ['CHEBI:63551']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.07058823529411765 is too low.\n'
               'True positives: '
               "[('C[C@]12CC[C@H]3[C@@H](CCc4cc(O)ccc34)[C@@H]1CC[C@@H]2O[C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(C[C@@H]([C@@]2(C[C@@H](C1)O)[H])O)[H])(CC[C@@]4([C@@H](CCC(O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C([O-])=O)=O)C)[H])[H])C)[H])C', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('C1[C@]2([C@]3([C@@](C4=C(C=C(O)C=C4)CC3)(CC[C@@]2([C@@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C([O-])=O)C)[H])[H])[H]', "
               "'Found beta-D-glucuronoside(1-) structure')]\n"
               'False positives: '
               "[('NCCCO[C@@H]1O[C@@H]([C@H](O)[C@H](O)[C@H]1O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)C[NH3+])O)O)O)O[C@H]2[C@@H]([C@H]([C@@H](O[C@@H]2CO[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)C(=O)[O-])O)O)O)O)O)OC)NC(=O)C)O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('CN(CCCC(O)c1ccc[n+](c1)[C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C([O-])=O)N=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('C1(O)[C@H](O)[C@@H](O[C@@H]2O[C@@H](C)[C@@H]([C@H]([C@H]2O)O)O)[C@H](O)[C@H](O1)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('[H][C@]12CC[C@]3(C)[C@@H](CC[C@@]3([H])[C@]1([H])CCc1cc(O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)C([O-])=O)ccc21)OC1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1NC(C)=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('[H][C@]12CC[C@]3(C)[C@@H](CC[C@@]3([H])[C@]1([H])CCc1cc(O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)C([O-])=O)ccc21)O[C@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1NC(C)=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('CC1=C(C=C)\\\\C(NC1=O)=C/c1[nH]c(Cc2[nH]c(\\\\C=C3NC(=O)C(C=C)=C\\\\3C)c(C)c2CCC([O-])=O)c(CCC(=O)O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C([O-])=O)c1C', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@@H]1[C@@H](COP([O-])(=O)OP([O-])(=O)O[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C([O-])=O)O[C@H]([C@@H]1O)n1ccc(=O)[nH]c1=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('[C@@H]([C@H](COP([O-])(=O)O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O[C@H]2O[C@@H]([C@H]([C@@H]([C@H]2O)O)O)C(=O)[O-])NC([C@@H](*)O)=O)(O)[C@@H](*)O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('Cc1cn([C@H]2C[C@H](O)[C@@H](COP([O-])(=O)OP([O-])(=O)OC3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)C([O-])=O)O2)c(=O)[nH]c1=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('[C@@H]1(O[C@@H]([C@@H]([C@@H]([C@H]1O)O)O)C(=O)[O-])O[C@H]2[C@H](OC([C@@H]([C@H]2O)O)O)C(=O)[O-]', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('[H][C@@]12C[C@](C)(CC[C@]1(C)CC[C@]1(C)C2=CC(=O)[C@]2([H])[C@@]3(C)CC[C@H](O[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)C([O-])=O)C([O-])=O)C(C)(C)[C@]3([H])CC[C@@]12C)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('C1[C@]2([C@](/C(=C/C=C/3\\\\C([C@H](C[C@@H](C3)O)O)=C)/CC1)(CC[C@@]2([C@H](C)CCCC(O[C@@H]4O[C@@H]([C@H]([C@@H]([C@H]4O)O)O)C(=O)[O-])(C)C)[H])[H])C', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O1[C@H](C([O-])=O)[C@H]([C@H](O)[C@H]([C@@H]1O[C@@H]2C[C@H](N(C)C2=O)C=3C=NC=CC3)O)O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O1[C@H](OP(OP(=O)(OC[C@H]2O[C@@H](N3C=CC(NC3=O)=O)[C@@H]([C@@H]2O)O)[O-])(=O)[O-])[C@H](O)[C@@H](O)[C@H](O)[C@@H]1C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC[C@@]2(C[C@@H](C1)O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C([O-])=O)[H])[H])(CC[C@]4([H])[C@@H](O)C)[H])C)[H])C', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('OC1O[C@@H]([C@H](O[C@@H]2OC(=C[C@H](O)[C@H]2O)C([O-])=O)[C@H](O)[C@H]1O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('CC1=C(C=C)\\\\C(NC1=O)=C/c1[nH]c(Cc2[nH]c(\\\\C=C3NC(=O)C(C=C)=C\\\\3C)c(C)c2CCC(=O)O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C([O-])=O)c(CCC(=O)O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C([O-])=O)c1C', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@@H]1[C@@H](O)[C@H](O[C@@H]2[C@@H](O)[C@H](O)[C@H](O[C@H]2Oc2cc([O-])c3c(c2)oc(cc3=O)-c2ccc(O)c(O)c2)C([O-])=O)O[C@@H]([C@H]1O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@H]1[C@@H](O[C@@H]([C@@H](O)[C@@H]1O)C([O-])=O)Oc1cc2oc(cc(=O)c2c(O)c1O)-c1ccccc1', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('C1[C@@H]([C@H]([C@H]([C@@H]1O)C/C=C\\\\CCCCC)/C=C/[C@@H](CCCC([O-])=O)O[C@@H]2O[C@H](C([O-])=O)[C@H]([C@@H]([C@H]2O)O)O)O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('[K+].[K+].C[C@]12CC[C@@](C)(C[C@H]1C1=CC(=O)[C@@H]3[C@@]4(C)CC[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)C([O-])=O)C([O-])=O)C(C)(C)[C@@H]4CC[C@@]3(C)[C@]1(C)CC2)C(O)=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('C1[C@]2([C@]3([C@@](C4=C(C=C(O)C=C4)CC3)(CC[C@@]2([C@@H](O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C([O-])=O)[C@@H]1O)C)[H])[H])[H]', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@@H]1[C@@H](O)[C@H](Oc2ccccc2C(O)=O)O[C@@H]([C@H]1O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('[C@@H]1(O)[C@H](C(=O)[O-])O[C@@H](O)[C@H](O)[C@H]1O', 'Found "
               "beta-D-glucuronoside(1-) structure'), "
               "('OC1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C([O-])=O', 'Found "
               "beta-D-glucuronoside(1-) structure'), "
               "('Nc1nc2n(cnc2c(=O)[nH]1)[C@@H]1O[C@H](COP([O-])(=O)OP([O-])(=O)OC2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)C([O-])=O)[C@@H](O)[C@H]1O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@@H]1[C@@H](O)[C@H](O[C@@H]([C@@H]1O)C([O-])=O)OP([O-])([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@@H]1[C@@H](O)[C@H](Oc2cc([O-])c3c(c2)oc(cc3=O)-c2ccc(O)c(O)c2)O[C@@H]([C@H]1O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('COc1c(O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C([O-])=O)cc2oc(cc(=O)c2c1O)-c1ccccc1', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('C1[C@@]2([C@]3(CC[C@]4([C@]([C@@]3(CC[C@@]2(C[C@@H](C1)O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C([O-])=O)[H])[H])(CCC4=O)[H])C)[H])C', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('[C@@H]1([C@H]([C@@H]([C@H]([C@@H](O1)O[C@@H]2[C@H](C(O[C@@H]([C@@H]2O)COS([O-])(=O)=O)O)NC(C)=O)O)O)O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('[H][C@@]12CC(C)(C)[C@@H](O)[C@@H](O)[C@]1(C)CC[C@]1(C)C2=CC[C@]2([H])[C@@]3(C)CC[C@H](O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)C([O-])=O)[C@](C)(CO)[C@]3([H])CC[C@@]12C', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)O)O[C@H]2[C@@H]([C@H]([C@@H](O[C@@H]2CO[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)C(=O)[O-])O)O)O)O)O)OC)NC(=O)C)O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@@H]1[C@@H](O)[C@H](O[C@@H]2[C@@H](O)[C@H](O)[C@H](O[C@H]2Oc2cc([O-])c3c(c2)oc(cc3=O)-c2ccc(O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)C([O-])=O)c(O)c2)C([O-])=O)O[C@@H]([C@H]1O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@@H]1[C@@H](COP([O-])(=O)OP([O-])(=O)OC2O[C@H]([C@@H](O)[C@H](O)[C@H]2O)C([O-])=O)O[C@H]([C@@H]1O)n1ccc(=O)[nH]c1=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('[H][C@]1(CCCN1C)c1ccc[n+](c1)[C@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('[Na+].C[C@]12CC[C@H]3[C@@H](CCc4cc(O)ccc34)[C@@H]1CC[C@@H]2O[C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@@H]1[C@@H](O)[C@H](O)[C@H](O[C@H]1Oc1cc2oc(cc(=O)c2c(O)c1O)-c1ccc(O)cc1)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O1[C@@H]([C@H]([C@@H]([C@H]([C@@H]1O[C@@H]2[C@@]3([C@]([C@]4([C@](CC3)([C@@]5([C@](C[C@@H](CC5)O)(CC4)[H])C)[H])[H])(CC2)[H])C)O)O)O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O[C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C([O-])=O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)O)O[C@H]2[C@@H]([C@H]([C@@H](O[C@@H]2CO[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)C(=O)[O-])O)O)O)O)O)OCCC[NH3+])NC(=O)C)O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('OC1O[C@@H]([C@H](O)[C@H](O)[C@H]1O)C([O-])=O', 'Found "
               "beta-D-glucuronoside(1-) structure'), "
               "('[H][C@@]12CC(C)(C)C[C@@H](O)[C@]1(C)CC[C@]1(C)C2=CC[C@]2([H])[C@@]3(C)CC[C@H](O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)C([O-])=O)[C@](C)(CO)[C@]3([H])CC[C@@]12C', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('COc1c(C)c2COC(=O)c2c(O)c1C\\\\C=C(/C)CCC(=O)O[C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('Nc1nc2n(cnc2c(=O)[nH]1)[C@@H]1O[C@H](COP([O-])(=O)OP([O-])(=O)O[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)C([O-])=O)[C@@H](O)[C@H]1O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@@H]1O[C@@H]([C@H](O)[C@H](O)[C@H]1O)C([O-])=O', 'Found "
               "beta-D-glucuronoside(1-) structure'), "
               "('C1[C@]2([C@](/C(=C/C=C/3\\\\C(CC[C@@H](C3)O)=C)/CC1)(CC[C@@]2([C@H](C)CCCC(O[C@@H]4O[C@@H]([C@H]([C@@H]([C@H]4O)O)O)C(=O)[O-])(C)C)[H])[H])C', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('[Na+].[Na+].O[C@H]1O[C@@H]([C@H](O[C@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)C([O-])=O)[C@H](O)[C@H]1O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O1[C@@H]2[C@]3([C@]([C@]4([C@](C2)([C@H](CC4)C(=O)CO)C1O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)C([O-])=O)[H])(CCC=6[C@@]3(CCC(=O)C6)C)[H])[H]', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('S(OC1=CC=C(C=2C(=O)C=3C(OC2)=CC(O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)C([O-])=O)=CC3[O-])C=C1)(O)(=O)=O.[Na+].[Na+]', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('C1[C@@H]([C@H]([C@H]([C@@H]1O)/C=C/[C@H](CCCCC)O[C@@H]2O[C@H](C([O-])=O)[C@H]([C@@H]([C@H]2O)O)O)C/C=C\\\\CCCC([O-])=O)O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C([O-])=O', 'Found "
               "beta-D-glucuronoside(1-) structure'), "
               "('COc1c(O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C([O-])=O)cc(O)c2c1oc(cc2=O)-c1ccccc1', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('Cc1cn([C@H]2C[C@H](O)[C@@H](COP([O-])(=O)OP([O-])(=O)OC3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)C([O-])=O)O2)c(=O)[nH]c1=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C/CC\\\\C(C)=C/CC\\\\C(C)=C/CC\\\\C(C)=C/CC\\\\C(C)=C/CC\\\\C(C)=C/CC\\\\C(C)=C/CC\\\\C(C)=C/COP([O-])(=O)OP([O-])(=O)O[C@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O[C@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]3O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)C([O-])=O)[C@H]2O)[C@H](O)[C@H]1O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('C1[C@]2([C@](/C(=C/C=C/3\\\\C(CC[C@@H](C3)O[C@@H]4O[C@@H]([C@H]([C@@H]([C@H]4O)O)O)C(=O)[O-])=C)/CC1)(CC[C@@]2([C@H](C)CCCC(C)(C)O)[H])[H])C', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('OC[C@H]1O[C@@H](Oc2cc3c(O)cc(O)cc3[o+]c2-c2ccc(O)c(O)c2)[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C([O-])=O)[C@@H](O)[C@@H]1O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@@H]1[C@@H](COP([O-])(=O)OP([O-])(=O)O[C@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)C([O-])=O)O[C@H]([C@@H]1O)n1ccc(=O)[nH]c1=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@H]1[C@@H](O[C@@H]([C@@H](O)[C@@H]1O)C([O-])=O)Oc1cc(O)c2c(c1)oc(cc2=O)-c1ccc(O)c(O)c1', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('C(CCC)C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCC(O[C@@H]1O[C@H](C([O-])=O)[C@H]([C@@H]([C@H]1O)O)O)=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@H]1[C@H](O[C@H]2[C@@H](O[C@@H]([C@@H](O)[C@@H]2O)C([O-])=O)Oc2cc(O)c3c(c2)oc(cc3=O)-c2ccc(O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3O)C([O-])=O)c(O)c2)O[C@@H]([C@@H](O)[C@@H]1O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('[H][C@@]12CC(C)(C)CC(=O)[C@]1(C)CC[C@]1(C)C2=CC[C@]2([H])[C@@]3(C)CC[C@H](O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)C([O-])=O)[C@](C)(CO)[C@]3([H])CC[C@@]12C', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@H]1[C@H](O[C@H]2[C@@H](O[C@@H]([C@@H](O)[C@@H]2O)C([O-])=O)Oc2cc(O)c3c(c2)oc(cc3=O)-c2ccc(O)c(O)c2)O[C@@H]([C@@H](O)[C@@H]1O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@@H]1[C@@H](O)[C@@H](O[*])O[C@@H]([C@H]1O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@H]1O[C@@H]([C@H](O)[C@H](O)[C@H]1O)C([O-])=O', 'Found "
               "beta-D-glucuronoside(1-) structure'), "
               "('OC1O[C@@H]([C@H](O[C@H]2OC(=C[C@H](O)[C@H]2O)C([O-])=O)[C@H](O)[C@H]1O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@@H]1[C@@H](O)C(O[C@@H]([C@H]1O)C([O-])=O)OP(O)(O)=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@H]1O[C@@H]([C@H](O[C@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)C([O-])=O)[C@H](O)[C@H]1O)C([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@@H]1[C@@H](O)[C@H](O[C@@H]([C@H]1O)C([O-])=O)OP([O-])([O-])=O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('OC[C@H]1O[C@@H](Oc2cc3c([O-])cc([O-])cc3[o+]c2-c2ccc(O)c(O)c2)[C@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C([O-])=O)[C@@H](O)[C@@H]1O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O=C1[C@@]2([C@]([C@]3([C@@]([C@@]4(C(=CC3)C[C@@H](O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)C(=O)[O-])CC4)C)(CC2)[H])[H])(CC1)[H])C', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('COc1cc(cc(OC)c1O[C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C([O-])=O)[C@H]1[C@@H]2[C@H](COC2=O)[C@H](O[C@@H]2O[C@@H]3CO[C@@H](C)O[C@H]3[C@H](O)[C@H]2O)c2cc3OCOc3cc12', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@@H]1[C@@]2([C@]([C@]3([C@](CC2)([C@@]4([C@](C[C@@H](CC4)O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)C([O-])=O)O)O)O)(CC3)[H])C)[H])[H])(CC1)[H])C', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('[C@H]1([C@H](C(O[C@@H]([C@@H]1OS([O-])(=O)=O)CO)O)NC(C)=O)O[C@H]2[C@@H]([C@H]([C@@H]([C@@H](O2)C([O-])=O)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)OS([O-])(=O)=O)O[C@H]4[C@@H]([C@H]([C@@H]([C@@H](O4)C([O-])=O)O)O)O)NC(C)=O)O)O', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('C1[C@@]2([C@]3(C(C[C@]4([C@]([C@@]3(CC[C@@]2(C[C@@H](C1)O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C([O-])=O)[H])[H])(CC[C@@]4(C([O-])=O)O)[H])C)=O)[H])C', "
               "'Found beta-D-glucuronoside(1-) structure'), "
               "('O[C@@H]1O[C@H](COS([O-])(=O)=O)[C@@H](O)[C@H](OC2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)C([O-])=O)[C@H]1NS([O-])(=O)=O', "
               "'Found beta-D-glucuronoside(1-) structure')]\n"
               'False negatives: '
               "[('C1[C@]2([C@]3([C@@](C4=C(C(=C(O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)C(=O)[O-])O)O)O)C=C4)O)CC3)(CC[C@@]2(C(=O)C1)C)[H])[H])[H]', "
               "'Missing required structural features of "
               "beta-D-glucuronoside(1-)'), "
               "('C1=CC(CN2C(=NC(=C2CO)Cl)CCCC)=CC=C1C3=CC=CC=C3C4=NN(N=N4)[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)C([O-])=O)O)O)O', "
               "'Missing required structural features of "
               "beta-D-glucuronoside(1-)')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 4,
    'num_false_positives': 96,
    'num_true_negatives': 183780,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.04,
    'recall': 0.8,
    'f1': 0.07619047619047618,
    'accuracy': 0.9994724849223139}