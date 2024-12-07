"""
Classifies: CHEBI:17478 aldehyde
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_aldehyde(smiles: str):
    """
    Determines if a molecule contains an aldehyde group (RC(=O)H).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains aldehyde group, False otherwise
        str: Reason for classification
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return False, "Invalid SMILES string"
            
        # SMARTS patterns for aldehyde group
        # Pattern 1: Standard aldehyde [CH](=O)[#6]
        # Pattern 2: Explicit hydrogen notation [CH1](=O)[#6]
        # Pattern 3: Aldehyde with formal charge preservation [CH]([O])[#6]
        patterns = [
            '[CH](=O)[#6]',
            '[CH1](=O)[#6]',
            '[CH]([O])[#6]'
        ]
        
        total_matches = set()
        for pattern in patterns:
            pat = Chem.MolFromSmarts(pattern)
            matches = mol.GetSubstructMatches(pat)
            total_matches.update(matches)
            
        if len(total_matches) > 0:
            if len(total_matches) == 1:
                return True, "Contains 1 aldehyde group"
            else:
                return True, f"Contains {len(total_matches)} aldehyde groups"
                
        # Additional check for edge cases with alternative representations
        for atom in mol.GetAtoms():
            if (atom.GetAtomicNum() == 6 and  # Carbon
                atom.GetTotalNumHs() == 1 and  # One hydrogen
                atom.GetFormalCharge() == 0 and  # Neutral
                len([b for b in atom.GetBonds() if b.GetBondType() == Chem.BondType.DOUBLE]) == 1):  # One double bond
                
                # Check if double bonded to oxygen
                for bond in atom.GetBonds():
                    if (bond.GetBondType() == Chem.BondType.DOUBLE and 
                        mol.GetAtomWithIdx(bond.GetOtherAtomIdx(atom.GetIdx())).GetAtomicNum() == 8):
                        return True, "Contains 1 aldehyde group"
                
        return False, "No aldehyde groups found"
        
    except Exception as e:
        return None, f"Error processing molecule: {str(e)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17478',
                          'name': 'aldehyde',
                          'definition': 'A compound RC(=O)H, in which a '
                                        'carbonyl group is bonded to one '
                                        'hydrogen atom and to one R group.',
                          'parents': ['CHEBI:36586']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.6578073089700996 is too low.\n'
               "True positives: [('CC1C(C=O)=CNC=C1C=O', 'Contains 2 aldehyde "
               "groups'), ('O=CC1=C(O)C=CC(=C1CC[C@@H](O)[C@H](O)C)CC=C(C)C', "
               "'Contains 1 aldehyde group'), ('O=CCCC/C=C/C=C/C', 'Contains 1 "
               "aldehyde group'), "
               "('O=C/C(=C/CCCCCCCCCCCCCC)/CCCCC/C=C\\\\C/C=C\\\\CCCCC', "
               "'Contains 1 aldehyde group'), "
               "('OC(=O)c1cc(O)c(C(=O)c2c(O)cccc2O)c(C=O)c1', 'Contains 1 "
               "aldehyde group'), "
               "('O=C1[C@@H]([C@@](/C=C/C(=C/CC2=C(O)C(=C(C)C=C2O)C=O)/C)([C@H](C)CC1)C)C', "
               "'Contains 1 aldehyde group'), ('C(C=1C=CC(=CC1)N(C)C)(=O)[H]', "
               "'Contains 1 aldehyde group'), ('[H]C(=O)CCC(O)=O', 'Contains 1 "
               "aldehyde group'), ('O=CCCC=C', 'Contains 1 aldehyde group'), "
               "('[H]C(=O)\\\\C=C\\\\C(C(O)=O)=C(\\\\O)C(O)=O', 'Contains 1 "
               "aldehyde group'), ('[H]C(=O)C1CCCCC1', 'Contains 1 aldehyde "
               "group'), ('O=CC(CCCCCCCCC)C', 'Contains 1 aldehyde group'), "
               "('C12C(C3C(C(CC3)*)(C)CC1)CCC4C2(CCC[C@@H]4C=O)C', 'Contains 1 "
               "aldehyde group'), ('O=C/C(=C/C=1N=COC1)/[C@@H](O)C', 'Contains "
               "1 aldehyde group'), ('O=CCC/C=C/CCC=O', 'Contains 2 aldehyde "
               "groups'), ('O(C=1C(=CC(OC)=C(OC)C1)/C=C\\\\C=O)C', 'Contains 1 "
               "aldehyde group'), ('[H]C(=O)c1ccc(CO)o1', 'Contains 1 aldehyde "
               "group'), "
               "('C[C@@H]([C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)C=C[C@]4(C)[C@H]3CC[C@]12C=O)[C@H]1CC(C)=C(C)C(=O)O1', "
               "'Contains 1 aldehyde group'), ('S(C(CC=O)C)C', 'Contains 1 "
               "aldehyde group'), "
               "('S(=O)(=O)(O[C@H](CC=CC1=C(C(O)=CC=C1)C=O)CC)O', 'Contains 1 "
               "aldehyde group'), "
               "('COc1cc(C=O)cc2[C@@H](CO)[C@@H](Oc12)c1cc(OC)c(O[C@H](CO)[C@@H](O)c2ccc(O)c(OC)c2)c(OC)c1', "
               "'Contains 1 aldehyde group'), "
               "('O[C@@H](CCCC(O)=O)\\\\C=C/C=C/C=C/[C@H](O)C\\\\C=C/CCCCC=O', "
               "'Contains 1 aldehyde group'), ('O=C(CCCCN)[H]', 'Contains 1 "
               "aldehyde group'), ('OC(=O)c1ccc(C=O)cc1O', 'Contains 1 "
               "aldehyde group'), ('O=CC(CCCC)CC', 'Contains 1 aldehyde "
               "group'), ('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC=O', 'Contains 1 "
               "aldehyde group'), ('OCC(CC=O)C(O)=O', 'Contains 1 aldehyde "
               "group'), ('O=CCC/C=C/C=C', 'Contains 1 aldehyde group'), "
               "('[H]C(=O)[C@@H](O)[C@@H](O)CC(=O)C(O)=O', 'Contains 1 "
               "aldehyde group'), ('O=C(NCCCCCN1C(=CC=C1)C=O)C', 'Contains 1 "
               "aldehyde group'), "
               "('[H][C@@]12CCC(C)=C[C@]1([H])[C@@]([H])(CC[C@H]2C)[C@@H](C)C=O', "
               "'Contains 1 aldehyde group'), "
               "('CC1(C)CC[C@@]2(CC[C@]3(C)C(C=C[C@@H]4[C@@]5(C)CC[C@@H](O)[C@@](C)(C=O)[C@@H]5CC[C@@]34C)=C2C1)C(O)=O', "
               "'Contains 1 aldehyde group'), ('C(/C=C\\\\CCC)=O', 'Contains 1 "
               "aldehyde group'), ('[H]C(=O)\\\\C=C\\\\C([H])=O', 'Contains 2 "
               "aldehyde groups'), "
               "('CC12CCC3C(C1(CCC2C4=CC(=O)OC4)O)CCC5(C3(CCC(C5)O)C=O)O', "
               "'Contains 1 aldehyde group'), "
               "('O=C1[C@@H]([C@]([C@H](C)CC1)(C[C@@H](OC(=O)C)/C(=C/CC2=C(O)C(=C(C)C=C2O)C=O)/C)C)C', "
               "'Contains 1 aldehyde group'), "
               "('ClC1=C(O)C(=C(O)C(=C1C)C=O)C/C=C(/[C@H](OC(=O)CCC)C[C@]2([C@@H](C(=O)CC[C@@H]2C)C)C)\\\\C', "
               "'Contains 1 aldehyde group'), ('[H]C(=O)CCCCCCCCCCCCCCC', "
               "'Contains 1 aldehyde group'), "
               "('C\\\\C=C1\\\\CN2[C@H]3Cc4c([nH]c5ccccc45)[C@@H]2C[C@@H]1[C@@H]3C=O', "
               "'Contains 1 aldehyde group'), ('O=CCCCCCCCCC/C=C\\\\CC', "
               "'Contains 1 aldehyde group'), "
               "('CC(CC/C=C(\\\\CC/C=C(\\\\CCC(=O)[H])/C)/C)=O', 'Contains 1 "
               "aldehyde group'), ('OC(=O)CCCCCCCCCCCCCCCCCCCCC=O', 'Contains "
               "1 aldehyde group'), ('O=C\\\\C=C\\\\C=C\\\\C/C=C\\\\CCCCC', "
               "'Contains 1 aldehyde group'), ('[H]C(=O)C#C[*]', 'Contains 1 "
               "aldehyde group'), ('P(OCC=1C(=C(O)C(=NC1)C)C=O)(O)(O)=O.O', "
               "'Contains 1 aldehyde group'), "
               "('[H][C@@]1(CC[C@H](C)[C@@]1([H])C=O)C(=C)C=O', 'Contains 2 "
               "aldehyde groups'), ('O=CCC/C=C\\\\CC', 'Contains 1 aldehyde "
               "group'), ('O=CCCCCCCCCCC/C=C\\\\CCC', 'Contains 1 aldehyde "
               "group'), ('N1=C(C2=NC=CC(=C2)C)C=C(C=C1)C([H])=O', 'Contains 1 "
               "aldehyde group'), ('O=CCCCC/C=C/C=C/C=C/C=C/CC', 'Contains 1 "
               "aldehyde group'), "
               "('O=C/C(=C/CCCCCCCCCCCCCC)/CCCCC/C=C\\\\CCCCCCCC', 'Contains 1 "
               "aldehyde group'), ('[H]C(=O)CCCCCCC([H])=C([H])C', 'Contains 1 "
               "aldehyde group'), ('O=CCCC=C=C', 'Contains 1 aldehyde group'), "
               "('[H][C@@]12CC(C)(C)CC[C@@]1(CC[C@]1(C)C2=CC[C@]2([H])[C@@]3(C)CC[C@H](O)[C@@](C)(C=O)[C@]3([H])CC[C@@]12C)C(O)=O', "
               "'Contains 1 aldehyde group'), ('O=C(/C=C/C(=O)C=O)C', "
               "'Contains 1 aldehyde group'), ('C=C(C)C=O', 'Contains 1 "
               "aldehyde group'), "
               "('C1=C(C=C2C(=C1OC)O[C@H]([C@@H]2C=O)C3=CC=C(C(=C3)OC)O)/C=C/C(O)=O', "
               "'Contains 1 aldehyde group'), "
               "('O=CCC\\\\C=C\\\\C=C/CCCCCCCCC', 'Contains 1 aldehyde "
               "group'), ('CCCC(C)CC=O', 'Contains 1 aldehyde group'), "
               "('C12=NC=C(N=C2C(=NC(=N1)N)N)C=O', 'Contains 1 aldehyde "
               "group'), "
               "('[N+]([O-])(=O)C1=C2C(=C3C(=C1)C(OC)=CC=C3)C=4OCOC4C=C2C(O[C@@H]5CC(=CCCC(=CCCC(=C5)C([H])=O)C)C)=O', "
               "'Contains 1 aldehyde group'), ('CC[C@H](C)C(=O)[H]', 'Contains "
               "1 aldehyde group'), "
               "('CC(=O)O[C@H]1CC[C@]2(C=O)[C@H]3CC[C@@]4(C)[C@@H](CCC4=O)[C@@H]3CC=C2C1', "
               "'Contains 1 aldehyde group'), "
               "('O=C/C=C/C=C/C=C/C=C/C=C/C=C/C=C/C=C/C=C/C', 'Contains 1 "
               "aldehyde group'), "
               "('[H]C(=O)\\\\C=C(/C)CC\\\\C=C(/C)CCC=C(C)C', 'Contains 1 "
               "aldehyde group'), ('O=CC=1N(C=CC1)C', 'Contains 1 aldehyde "
               "group'), "
               "('C[C@@H]1C[C@@H](OC(C)=O)[C@H](O)[C@H](O[C@H]2CC[C@]3(C=O)[C@H]4[C@H](O)C(=O)[C@]5(C)[C@H](CC[C@]5(O)[C@@H]4CC[C@]3(O)C2)c2ccc(=O)oc2)O1', "
               "'Contains 1 aldehyde group'), "
               "('CC(C)=CCc1c(O)cc2Oc3c(C=O)c(O)c(Cl)c(C)c3C(=O)Oc2c1C', "
               "'Contains 1 aldehyde group'), ('O=CCC(CC(C)(C)C)C', 'Contains "
               "1 aldehyde group'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)O[C@H]2[C@@H]([C@@H](C(=CO2)C(OC)=O)CC=O)C=C', "
               "'Contains 1 aldehyde group'), "
               "('CC(C)[C@@H]1C[C@@H](O)[C@H]2[C@]1(CC[C@@]1(C)[C@@H]3[C@@H](O)C[C@H]4C(C)(C)[C@H](CC[C@]4(C)C3=CC[C@]21C)O[C@@H]1O[C@H](CO[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@@H](O)[C@H](O)[C@H]1O)C=O', "
               "'Contains 1 aldehyde group'), "
               "('[H]C(=O)[C@H]1C(=CC[C@@]2([H])[C@]3(C)CC[C@@]4([H])C(C)(C)CCC[C@]4(C)[C@@]3([H])C[C@H](OC(C)=O)[C@]12C)C([H])=O', "
               "'Contains 2 aldehyde groups'), ('O=Cc1ccco1', 'Contains 1 "
               "aldehyde group'), "
               "('CC1(C)CC[C@]2(C=O)[C@H](O)C[C@]3(C)[C@@H]([C@@H]2C1)C(=O)C[C@@H]1[C@@]2(C)CC[C@H](O[C@@H]4OC[C@H](O[C@@H]5O[C@H](CO)[C@@H](O)[C@H](O)[C@H]5O)[C@H](O)[C@H]4O[C@@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@H]4O)C(C)(C)[C@@H]2CC[C@@]31C', "
               "'Contains 1 aldehyde group'), "
               "('[H][C@@]12C[C@@]3([H])C(C)(C)O[C@@](C\\\\C=C(\\\\C)C=O)(C1=O)[C@]31Oc3c(CC=C(C)C)c4OC(C)(C)C=Cc4c(O)c3C(=O)C1=C2', "
               "'Contains 1 aldehyde group'), "
               "('[H][C@]12[C@H](O)[C@]34C[C@@H](C[C@@H](OC(C)=O)[C@@]3([H])[C@@]1(CCCC2(C)C)COC4=O)C(=C)C=O', "
               "'Contains 1 aldehyde group'), ('CC(C=O)C1CCC(C)=CC1', "
               "'Contains 1 aldehyde group'), "
               "('N[C@@H]1C[C@H](N)[C@@H](O[C@H]2O[C@H](C=O)[C@@H](O)[C@H](O)[C@H]2N)[C@H](O)[C@H]1O', "
               "'Contains 1 aldehyde group'), "
               "('Cc1c(Cl)c(O)c(C=O)c2Oc3cc4OC(C)(C)CC(=O)c4c(C)c3OC(=O)c12', "
               "'Contains 1 aldehyde group'), ('O=C\\\\C=C\\\\CCCCCCCCCCC', "
               "'Contains 1 aldehyde group'), "
               "('N[C@@H]1C[C@H](N)[C@@H](O[C@H]2O[C@H](C=O)[C@@H](O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O', "
               "'Contains 1 aldehyde group'), ('CC(=O)\\\\C=C\\\\C=C(/C)C=O', "
               "'Contains 1 aldehyde group'), ('[H]C(=O)C(O)CCCCCCCCCCCCCCCC', "
               "'Contains 1 aldehyde group'), "
               "('[H][C@@]12C[C@H](O)CC[C@]1(C)[C@@]1([H])C[C@H](O)[C@]3(C)[C@]([H])(CC[C@@]3([H])[C@]1([H])[C@H](O)C2)[C@H](C)CCC(O)C(C)C=O', "
               "'Contains 1 aldehyde group'), ('[H]C(=O)CCCCCCCCC(O)=O', "
               "'Contains 1 aldehyde group'), ('O=CCCCCCC', 'Contains 1 "
               "aldehyde group'), "
               "('[H][C@@]12CCC3=C(CC[C@]4(C)[C@]([H])(CC[C@@]34[H])[C@H](C)CCC=C(C)C)[C@@]1(C)CC[C@H](O)C2C=O', "
               "'Contains 1 aldehyde group'), ('O1C(C1CC=O)CCCCC', 'Contains 1 "
               "aldehyde group'), ('O=C\\\\C=C\\\\C=C\\\\C=C\\\\C=C\\\\C', "
               "'Contains 1 aldehyde group'), ('OC=1C=C(NC1C=O)C=2NC=CC2', "
               "'Contains 1 aldehyde group'), ('O1C(C1C=CC=O)CCCCC', 'Contains "
               "1 aldehyde group'), ('[H]C(=O)C([H])=C([H])CCC', 'Contains 1 "
               "aldehyde group'), ('O=C/C=C\\\\CCCCCCC', 'Contains 1 aldehyde "
               "group'), ('O=CCCCCCCCCC/C=C/CC', 'Contains 1 aldehyde group'), "
               "('[H]C(=O)[C@@H](N)Cc1c[nH]cn1', 'Contains 1 aldehyde group'), "
               "('CC(C)=CC(=O)c1c(O)cc2Oc3c(C=O)c(O)cc(C)c3C(=O)Oc2c1C', "
               "'Contains 1 aldehyde group'), "
               "('[H]C(=O)C(C)CCC[C@@H](C)[C@@]1([H])CC[C@@]2([H])[C@]3([H])[C@H](O)C[C@]4([H])C[C@H](O)CC[C@]4(C)[C@@]3([H])C[C@H](O)[C@]12C', "
               "'Contains 1 aldehyde group'), "
               "('C=1(C=C(C(=C(C1C)O)C=O)CC(CCCCCCCCC)=O)O', 'Contains 1 "
               "aldehyde group'), ('OC1=C(C(C)(C)C)C=C(C=C1C(C)(C)C)C=O', "
               "'Contains 1 aldehyde group')]\n"
               'False positives: '
               "[('O=C1OC2=C(C(C(=O)O)=CC(=C2)OC)OC3=C1C(=CC(=C3C=O)O)C', "
               "'Contains 1 aldehyde group'), "
               "('O=C(C1=C2O[C@]3(OC[C@@H]([C@H]3CC2=C(C)C=C1O)C)C)C4=C(C(OC)=CC(=C4)O)C=O', "
               "'Contains 1 aldehyde group'), "
               "('OC1=C(C(=C(CC/C(=C/CC2=C(O)C=CC(O)=C2)/C)C(=C1)C)C)C=O', "
               "'Contains 1 aldehyde group'), "
               "('O=C1C=CC(=CC([C@@H](OC(=O)C[C@H]([C@@H]([C@H]([C@H](C[C@H]1C)CC=O)OC2OC(C(OC3OC(C(OC(=O)CC(C)C)C(C3)(O)C)C)C(C2O)N(C)C)C)C)OC(=O)C)CC)COC4OC(C(O)C(C4OC)OC)C)C', "
               "'Contains 1 aldehyde group'), "
               "('O1C(CCC=2C1=C(C(=CC2OC)COC(=O)CCCCCCCCCCCCCCC)C=O)(CC(=O)C=C(C)C)C', "
               "'Contains 1 aldehyde group'), "
               "('[H]C([H])([C@@]([H])(O)C=O)[C@@]([H])(O)[C@@]([H])(C)O', "
               "'Contains 1 aldehyde group'), "
               "('CC(C)=CCc1c(O)c(C=O)cc2c3ccccc3[nH]c12', 'Contains 1 "
               "aldehyde group'), ('O=CC1=C2C(OC(=C2)C)=CC(=C1)O', 'Contains 1 "
               "aldehyde group'), ('S(CC1=C(OC)C=CC(=C1)C=O)CC=2OC=CC2', "
               "'Contains 1 aldehyde group'), "
               "('O=CC1=C(OC)C2=C(C=C(C)OC2)C=C1O', 'Contains 1 aldehyde "
               "group'), "
               "('O=C1C=C(C)[C@@H]2[C@H]1C(=CC[C@H]3[C@@H]([C@H](/C=C\\\\[C@H](O)C(O)(C)C)C)CC[C@@]3(C2)C)C=O', "
               "'Contains 1 aldehyde group'), "
               "('CC(=O)O[C@H]1CC[C@]2(C=O)[C@H]3CC[C@]4(C)[C@H](CC[C@]4(O)[C@@H]3CC[C@]2(O)C1)c1ccc(=O)oc1', "
               "'Contains 1 aldehyde group'), "
               "('ON1CC(CC2=CC=CC=C2)=C(C=C1)C=O', 'Contains 1 aldehyde "
               "group'), ('OC(=O)CCC/C=C\\\\CC/C=C/C=O', 'Contains 1 aldehyde "
               "group'), ('[H]C(=O)[C@@H](N)CCC([O-])=O', 'Contains 1 aldehyde "
               "group'), ('O=Cc1c2ccc(cc3ccc(cc4ccc(cc5ccc1[nH]5)n4)[nH]3)n2', "
               "'Contains 1 aldehyde group'), "
               "('O=C1OC2=C(C(=C(O)C(=C2C)C(=O)O)CO)OC3=C1C(=CC(=C3C=O)O)C', "
               "'Contains 1 aldehyde group'), ('OC(=O)CCCCCC=O', 'Contains 1 "
               "aldehyde group'), "
               "('OC1C2C3(C(C(CC3)C(CC(O)C=C(C)C)C)(CCC2(C4C(=C1)C(C(O)CC4)(C)C)C=O)C)C', "
               "'Contains 1 aldehyde group'), "
               "('[H]C(=O)C\\\\C=C/CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Contains 1 aldehyde group'), "
               "('[H][C@@]12CC[C@@]3([H])[C@@]4(CC[C@H](O)[C@@](C)(COC(C)=O)[C@H]4C=O)C(OC(=O)[C@]3(C1)C(=O)C2=C)C(C)=O', "
               "'Contains 1 aldehyde group'), "
               "('O=C1[C@]2([C@@H](C3=C([C@H](CO)C)CC[C@]3(CO)CC2)CC=C(C1)C=O)C', "
               "'Contains 1 aldehyde group'), "
               "('ClC/C(=C\\\\CCl)/CC/C=C(/C=O)\\\\C', 'Contains 1 aldehyde "
               "group'), "
               "('[H]C(=O)CCCC(=O)O[C@H](COC(=O)CCCCC)COP(O)(=O)OCC[N+](C)(C)C', "
               "'Contains 1 aldehyde group'), "
               "('C[C@@]1(CC[C@]23CO[C@@]4(CC[C@@H]5[C@@]6(C)CC[C@H](O[C@@H]7OC[C@H](O[C@@H]8O[C@H](CO)[C@@H](O)[C@H](O[C@@H]9O[C@H](CO)[C@@H](O)[C@H](O)[C@H]9O)[C@H]8O[C@@H]8OC[C@@H](O)[C@H](O)[C@H]8O)[C@H](O)[C@H]7O[C@@H]7O[C@H](CO)[C@@H](O)[C@H](O)[C@H]7O)C(C)(C)[C@@H]6CC[C@@]5(C)[C@]4(C)C[C@H]2O)[C@@H]3C1)C=O', "
               "'Contains 1 aldehyde group'), ('[H]C(=O)CP(O)([O-])=O', "
               "'Contains 1 aldehyde group'), "
               "('CO[C@H]1C[C@H](O[C@H]2CC[C@]3(C=O)[C@H]4CC[C@]5(C)[C@H](CC[C@]5(O)[C@@H]4CC[C@]3(O)C2)C2=CC(=O)OC2)O[C@H](C)[C@H]1O', "
               "'Contains 1 aldehyde group'), "
               "('CC(C)C[C@@H]1[C@H]2CC(C=C[C@@]2(C)Oc2c(C=O)c(O)c(C=O)c(O)c12)C(C)C', "
               "'Contains 2 aldehyde groups'), "
               "('O=C(OC1=C(C(O)=C(C(=O)O)C(=C1)C)C)C2=C(O)C(=C(OC)C=C2C)C=O', "
               "'Contains 1 aldehyde group'), "
               "('O=C(NC(C(=O)NC(C(=O)NC(C=O)C)CCC(=O)N)C1NC(=NCC1)N)NC(C(=O)O)CC(C)C', "
               "'Contains 1 aldehyde group'), "
               "('O1[C@@]23[C@@]([C@H]([C@@H](O)C12)C=4C=CC(OC4)=O)(CC[C@H]5[C@H]3CC[C@H]6[C@@]5(CC[C@H](O)C6)C=O)C', "
               "'Contains 1 aldehyde group'), "
               "('O=C(OC)CC(NC1=CC=C(C=O)C=C1)C(O)/C=C/C(O)C', 'Contains 1 "
               "aldehyde group'), "
               "('O=C(NC(C=O)CCCN=C(N)N)C1N(C(=O)C(NC(=O)C(OC(=O)C)CC2=CC=C(O)C=C2)CC(C)C)CCC1', "
               "'Contains 1 aldehyde group'), "
               "('O=C1O[C@H]([C@@H](O)CC)C[C@H]1C/C=C/C=O', 'Contains 1 "
               "aldehyde group'), "
               "('CCC1=C(C=O)C2=[N+]3C1=Cc1c(C)c4C(=O)[C-](C(=O)OC)C5=C6[C@@H](CCC(=O)OC\\\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)[C@H](C)C7=[N+]6[Mg--]3(n1c45)n1c(=C7)c(C)c(C=C)c1=C2', "
               "'Contains 1 aldehyde group'), "
               "('O=C1OC(=C)[C@H](C)C=2C1=C(O)C(=C(O)C2C=O)C', 'Contains 1 "
               "aldehyde group'), ('O=CC1=C(O)C=CC(=C1/C=C/CCCCC)OC', "
               "'Contains 1 aldehyde group'), ('O=C1C=2C(NC(=C1)C=O)=CC=CC2', "
               "'Contains 1 aldehyde group'), "
               "('[C@H]1(O[C@@](C[C@@H]([C@H]1NC(=O)C)O)(OCC2[C@@H]([C@@H]([C@H]([C@@H](O2)O[C@@H]3[C@H](O[C@H]([C@@H]([C@H]3O)NC(=O)C)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO)O[C@H]([C@H](O)CO)[C@@H]([C@@H](O)C=O)O)O)CO)O)O)O)C(=O)O)[C@@H]([C@@H](CO)O)O', "
               "'Contains 1 aldehyde group'), "
               "('O=C1N(C(=O)C2=CC=3[C@H](N2C1=O)[C@@H](OC(=O)C4=CC(OC5=C(OC)C=CC(=C5)C=O)=C(OC)C=C4)C=COC3)C', "
               "'Contains 1 aldehyde group'), ('O(C=1C(=CC=CC1)C=O)C', "
               "'Contains 1 aldehyde group'), "
               "('SC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)CNC(=O)[C@@H](NC(=O)CNC(=O)CNC(=O)[C@@H](NC(=O)CNC(=O)[C@@H](NC(=O)[C@@H](N)CCCCN)CC(=O)N)CC1=CC=C(O)C=C1)CO)CC(=O)N)CCCNC(=N)N)CC=2C3=C(C=CC=C3)NC2)C(C)C)CC=4NC=NC4)C(=O)NCC(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)NCC=O)C(C)C)[C@H](CC)C)C', "
               "'Contains 1 aldehyde group'), "
               "('ClC1=C(O)C=C(O)C(=C1C)C(=O)O[C@H]2[C@@]3(O)C(=C[C@@H]4CC([C@@H]([C@@H]4[C@@]3(C)C2)O)(C)C)C=O', "
               "'Contains 1 aldehyde group'), "
               "('[H]C(=O)CCC[C@H]([NH3+])C([O-])=O', 'Contains 1 aldehyde "
               "group'), ('Oc1cc([nH]c(=O)c1CCC=O)C([O-])=O', 'Contains 1 "
               "aldehyde group'), "
               "('O[C@@]12C3C([C@@]4([C@](O)(CC3)C[C@@H](OC5OC(C(OC(=O)C)C(OC)C5O)C)CC4)C=O)C(OC(=O)C)C[C@@]1([C@H](CC2)C=6COC(=O)C6)C', "
               "'Contains 1 aldehyde group'), ('O=CC1C(CCC1C(C)=C)C', "
               "'Contains 1 aldehyde group'), "
               "('[H][C@@](O)(CO)[C@]([H])(O)[C@]([H])(O)[C@@]([H])(O[C@@H]1O[C@@H](C)[C@@H](O)[C@@H](O)[C@@H]1O)C=O', "
               "'Contains 1 aldehyde group'), ('OCC(O)(CO)[C@@H](O)C=O', "
               "'Contains 1 aldehyde group'), "
               "('[C@H]1([C@@H](O[C@@H]([C@H]([C@@H]1O)O)O[C@H]2[C@@H](O[C@@H]([C@@H]([C@@H]2O)O)CO)OC3[C@H]([C@@H](O[C@@H]([C@H]3O)CO)O[C@H]4[C@H]([C@H](O[C@H]([C@@H]4C)OC([C@@H]([C@@H](O)C=O)O)[C@@H](CO)O)CO[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5NC(=O)C)O[C@@H]6O[C@H]([C@H]([C@H]([C@@H]6O)O)O)O)O[C@@H]7[C@@H]([C@H]([C@H]([C@H](O7)CO)O)O)O)CO)O)NC(=O)C)C)O', "
               "'Contains 1 aldehyde group'), "
               "('O=CC1=C2[C@@](CC([C@H]2[C@@H](O)C[C@H]1C)(C)C)(CO)C', "
               "'Contains 1 aldehyde group'), "
               "('O=CC1=C(C=C(O)C2=C1O[C@]3([C@@]4([C@H](C([C@H](O)[C@@H](C4)O)(C)C)CC[C@H]3C)C)C2)CO', "
               "'Contains 1 aldehyde group'), "
               "('S(OC)(=O)C=1NC=2C(C1C=O)=CC=CC2', 'Contains 1 aldehyde "
               "group'), "
               "('O([C@@H]1[C@]2([C@]3([C@@]([C@](CC3)([C@@H](C/C=C/C(O)(C)C)C)[H])(CC[C@]2([C@]4(C(=C1)C([C@@H](O)CC4)(C)C)[H])C=O)C)C)[H])[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)CO', "
               "'Contains 1 aldehyde group'), "
               "('O=C1C(\\\\C(=C/2\\\\N=C(C(C2CCC(O)=O)C)CC3NC(=O)C(=C3C)C=C)\\\\C=4NC(=C(C41)C)CC=5NC(=C(C5CC)C)C=O)C(OC)=O', "
               "'Contains 1 aldehyde group'), "
               "('ClC1=C(O)C(=C(OC)C=C1C)C(=O)C2=C(C(O)=CC(=C2CC=C(C)C)O)C=O', "
               "'Contains 1 aldehyde group'), "
               "('O=C(O[C@@H]1[C@H](OC)[C@H](O[C@H]([C@H]1O)OC[C@]23[C@@]4(C(C(C)C)=C[C@@H]2C[C@]4(C=O)[C@@H]5CC[C@H]([C@H]5C3)C)C(=O)O)C)/C(=C/C=C\\\\C)/C', "
               "'Contains 1 aldehyde group'), "
               "('C=C[C@H]1CN2CCc3c([nH]c4ccccc34)[C@@H]2C[C@@H]1CC=O', "
               "'Contains 1 aldehyde group'), ('OC(=O)C(=O)CC=O', 'Contains 1 "
               "aldehyde group'), "
               "('O=CC1=C(O)C(=CC2=C1CC[C@@H](O2)[C@H](O)C=CC)CC=C(C)C', "
               "'Contains 1 aldehyde group'), "
               "('P(OC[C@H](OC(=O)CCC(O)/C=C/C=O)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Contains 1 aldehyde group'), "
               "('C1CN(CCN1C2=CC=C(C=C2)C=O)[S+](=O)(C3=CC4=C(C=C3)NC(=O)C4)[O-]', "
               "'Contains 1 aldehyde group'), "
               "('O([C@H]1[C@@H](OC2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)[C@H](C[C@@H](O[C@@H]([C@H](O[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@@H](O)C=O)[C@H](O)CO)[C@@H]1O)CO)[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)CO)[C@H]4NC(=O)C)CO', "
               "'Contains 1 aldehyde group'), "
               "('[H][C@@](C)(O)[C@]([H])(N)[C@@](C)(O)[C@@]([H])(OC)C=O', "
               "'Contains 1 aldehyde group'), "
               "('O=C(O[C@@H]1C=C(C=O)[C@](O)(C=O)[C@@]2([C@@H]1C(CCC2)(C)C)C)/C=C/C=C/C=C/C', "
               "'Contains 2 aldehyde groups'), "
               "('O=CC=1C2=C([C@H]([C@@H](O)C[C@H]2O)C)N(C1)C', 'Contains 1 "
               "aldehyde group'), ('OC(=O)CCC/C=C\\\\C/C=C\\\\CC=O', 'Contains "
               "1 aldehyde group'), "
               "('CC[C@@]1(CN2CCC=3C4=CC=CC=C4NC3[C@@]2(C[C@@]1(CC=O)[H])[H])[H]', "
               "'Contains 1 aldehyde group'), "
               "('O=C1C23OC(C1C(O)C(=CC=CC4(C=C(C(C)CC45OC([O-])C(C5=O)C(O)C=CC6(C=C(C=O)C(C)CC67OC(C(C(C(=CC=CC8C9(C(C(C(C=CC2(C=C(C=O)C(C3)C)C)O)C(O9)[O-])=O)CC(C)C(=C8)CO[C@H]%10O[C@@H]([C@H](O)[C@@H]([C@H]%10O)O)CO)C)O)C7=O)[O-])C)CO[C@H]%11O[C@@H]([C@H](O)[C@@H]([C@H]%11O)O)CO)C)C)[O-]', "
               "'Contains 2 aldehyde groups'), "
               "('O=C1O[C@H](O)[C@@H]2[C@]13[C@@H](O)[C@@H](OC(=O)[C@H](O)CCCCCCCC)CC([C@@H]3CC=C2C=O)(C)C', "
               "'Contains 1 aldehyde group'), "
               "('O=C1N(C(=O)C2=CC=3[C@H](N2C1=O)[C@@H](OC(=O)C4=CC(OC5=C(O)C=CC(=C5)C=O)=C(OC)C=C4)C=COC3)C', "
               "'Contains 1 aldehyde group'), "
               "('S1CC(O)(N2C1=C(C=3C2=CC=CC3)C=O)C', 'Contains 1 aldehyde "
               "group'), "
               "('O=C1OC(CC2OC2C=CC(O)C(CC(C(C(C(C1)OC(=O)CC)OC)OC3OC(C(OC4OC(C(OC(=O)CC(C)C)C(C4)(O)C)C)C(C3O)N(C)C)C)CC=O)C)C', "
               "'Contains 1 aldehyde group'), "
               "('CC(C)(C)C1=CC(=CC(=C1)C=O)C(C)(C)C', 'Contains 1 aldehyde "
               "group'), ('O=C(O)C(=O)C=1C(=C[C@@H]2CC(C[C@@H]2C1C)(C)C)C=O', "
               "'Contains 1 aldehyde group'), "
               "('CCC(=O)O[C@H]1[C@H](C)O[C@H](C[C@@]1(C)O)O[C@@H]1[C@@H](C)O[C@@H](O[C@H]2[C@@H](CC=O)C[C@@H](C)[C@@H](O)\\\\C=C\\\\C=C\\\\C[C@@H](C)OC(=O)C[C@@H](OC(C)=O)[C@@H]2OC)[C@H](O)[C@H]1N(C)C', "
               "'Contains 1 aldehyde group'), "
               "('O=CC1=C(O)C=CC=C1C=CCCC[C@@H](O)C', 'Contains 1 aldehyde "
               "group'), ('O(C1C(C2C(C(C(O)(CC2)C)C=O)(CC1)C)(C)C)C(=O)C', "
               "'Contains 1 aldehyde group'), ('Cl\\\\C=C/C=O', 'Contains 1 "
               "aldehyde group'), "
               "('O=C[C@]12[C@@H](O[C@H](C(O)(C)C)C[C@H]1O)CC[C@]3([C@H]2CC[C@@H]4[C@@]3(C=5NC=6C=CC=CC6C5C4)C)C', "
               "'Contains 1 aldehyde group'), "
               "('O=CC1=C(O)C=CC2=C1[C@@](O)(C3=C4O[C@H](C(O)(C)C)COC4=CC(=C3)C)[C@H](C(=C)C)C2', "
               "'Contains 1 aldehyde group'), "
               "('O=C(O[C@H]1[C@H](O)C([C@@H]2CC[C@H]([C@]3([C@]2(C1)C)OC=4C=C(CO)C(=C(C4C3)O)C=O)C)(C)C)C', "
               "'Contains 1 aldehyde group'), ('O=CC1(C2(C3C2CC1C3)C)C', "
               "'Contains 1 aldehyde group'), "
               "('O=C(NC(C=O)CCCN=C(N)N)[C@H](NC(=O)C(NC(=O)C(O)CC1=CC=C(O)C=C1)CCC2=CC=CC=C2)[C@@H](CC)C', "
               "'Contains 1 aldehyde group'), "
               "('O=CC1=CCC2C3=C(C(C)C)CC[C@]3(C)CC[C@]2([C@H]([C@H]1OC)O)C', "
               "'Contains 1 aldehyde group'), "
               "('O1C(OC2=C(CCC=O)C=CC=C2O)C(O)C(O)C(O)C1C(O)=O', 'Contains 1 "
               "aldehyde group'), ('O=C(O)[C@H](N)C1=CC(O)=C(C=O)C=C1', "
               "'Contains 1 aldehyde group'), "
               "('O=[N+]([O-])[C@@]1([C@H](NC(=O)OC)[C@H](O[C@H](C1)O[C@H]2C(=C[C@@H]3[C@@]4(OC(=O)C(C4=O)=C([C@]5([C@H](C(=CC2)C)C=C[C@@H]6[C@@H](O[C@@H]7O[C@@H]([C@@H](OC(=O)C)[C@H](C7)O[C@H]8O[C@@H]([C@@H](O)CC8)C)C)[C@H](C)C[C@@H]([C@H]56)C)C)O)CC(C=O)=C[C@@H]3O)C)C)C', "
               "'Contains 1 aldehyde group'), "
               "('C=1(C(=C(C(=C(C1Cl)C)C=O)O)C/C=C(/CC/C=C(/[C@H](C[C@H]2C(C)(C)O2)O)\\\\C)\\\\C)[O-]', "
               "'Contains 1 aldehyde group'), "
               "('O=C1C=CC(=CC(C(OC(=O)CC(C(C(C(CC1C)CC=O)OC2OC(C(OC3OC(C(O)C(C3)(O)C)C)C(C2O)N(C)C)C)C)O)CC)COC4OC(C(O)C(C4OC)OC)C)C.O=C(O)C(O)C(O)C(=O)O', "
               "'Contains 1 aldehyde group'), "
               "('O=C1[C@H]2C(=CC[C@H]3C([C@H](/C=C\\\\C=C(C)C)C)CC[C@@]3(C[C@@H]2[C@@](C1)(O)C)C)C=O', "
               "'Contains 1 aldehyde group'), ('O=C(C(NCC(O)=O)CCCCC)C=O', "
               "'Contains 1 aldehyde group'), "
               "('O[C@H]1[C@H]([C@H](O[C@H]([C@@H]1O)O[C@@H]2[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]2O)O)CO)CO)O[C@H]3[C@@H]([C@H]([C@@H](O)[C@H](O3)C=O)O)NC(C)=O', "
               "'Contains 1 aldehyde group'), ('OCC(CC=O)C([O-])=O', 'Contains "
               "1 aldehyde group'), "
               "('O=C1NC=2C(C(=O)[C@H]3OC3(C)C)=CC=CC2[C@]14[C@](C=O)([C@H]5C[C@H]6C[C@H](OC(=O)C)C[C@@H](N6C[C@@]5(C4)NC)C)C', "
               "'Contains 1 aldehyde group'), "
               "('O1[C@](O[C@@H]2[C@@H](O)[C@@H](O[C@@H]([C@@H]2O)CO)O[C@@H]([C@H](O[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@H](O)CO)[C@@H](NC(=O)C)C=O)(C[C@H](O)[C@@H](NC(=O)C)[C@@]1([C@H](O)[C@H](O)CO)[H])C(O)=O', "
               "'Contains 1 aldehyde group'), "
               "('O=CC1=C(O)C(=CC(=C1C#CC(=C)C)O)CC=C(C)C', 'Contains 1 "
               "aldehyde group'), ('O=CC1=C(CC[C@@H]2[C@@]1(CCCC2(C)C)C)CO', "
               "'Contains 1 aldehyde group'), ('[H]C(CS([O-])=O)=O', 'Contains "
               "1 aldehyde group'), "
               "('O=CC1=C(C=C2O[C@](CC[C@@H](O)C(O)(C)C)(C)[C@H]3[C@H]4C2=C1O[C@H]4[C@@](O)(CC3)C)C=O', "
               "'Contains 2 aldehyde groups')]\n"
               'False negatives: '
               "[('C(/C=[N+]\\\\1/C(CCC1)C([O-])=O)=C\\\\C=2C=C(C(=C(C2)OC)O)OC', "
               "'No aldehyde groups found'), "
               "('[C@H](C(NC)=O)(NC([C@H](CCCC=1C=CC=CC1)[C@@H](N(O)C=O)C)=O)C(C)(C)C', "
               "'No aldehyde groups found'), "
               "('C(=C/[NH+]1C(CCC1)C([O-])=O)\\\\C=C2C=C(C(C(=C2)OC)=O)OC', "
               "'No aldehyde groups found')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 100,
    'num_false_positives': 100,
    'num_true_negatives': 61,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.5,
    'recall': 0.9803921568627451,
    'f1': 0.662251655629139,
    'accuracy': 0.6121673003802282}