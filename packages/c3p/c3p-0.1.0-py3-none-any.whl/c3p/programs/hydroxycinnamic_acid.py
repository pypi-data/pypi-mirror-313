"""
Classifies: CHEBI:24689 hydroxycinnamic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroxycinnamic_acid(smiles: str):
    """
    Determines if a molecule is a hydroxycinnamic acid (cinnamic acid with one or more hydroxy substituents).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydroxycinnamic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Pattern 1: phenyl-CH=CH-C(=O)OH (free acid)
    pattern1 = Chem.MolFromSmarts('[cH,c]1[cH,c][cH,c][cH,c][cH,c][cH,c]1[CH,C]=[CH,C]C(=O)O')
    
    # Pattern 2: phenyl-CH=CH-C(=O)OR (ester)
    pattern2 = Chem.MolFromSmarts('[cH,c]1[cH,c][cH,c][cH,c][cH,c][cH,c]1[CH,C]=[CH,C]C(=O)[O;!$(O[H])]')
    
    # Pattern 3: phenyl-CH=CH-C(=O)N (amide)
    pattern3 = Chem.MolFromSmarts('[cH,c]1[cH,c][cH,c][cH,c][cH,c][cH,c]1[CH,C]=[CH,C]C(=O)N')

    matches = []
    if mol.HasSubstructMatch(pattern1):
        matches.extend(mol.GetSubstructMatches(pattern1))
    if mol.HasSubstructMatch(pattern2):
        matches.extend(mol.GetSubstructMatches(pattern2))
    if mol.HasSubstructMatch(pattern3):
        matches.extend(mol.GetSubstructMatches(pattern3))

    if not matches:
        return False, "No cinnamic acid core structure found"

    # For each match, check if the phenyl ring has hydroxy substituents
    for match in matches:
        phenyl_atoms = match[0:6]  # First 6 atoms form the phenyl ring
        
        # Check for hydroxy groups on phenyl ring
        hydroxy_count = 0
        for atom_idx in phenyl_atoms:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O':
                    # Check if this oxygen is part of a hydroxy group
                    if neighbor.GetTotalNumHs() == 1 and len([n for n in neighbor.GetNeighbors() if n.GetSymbol() != 'H']) == 1:
                        hydroxy_count += 1
                    # Check for deprotonated hydroxy groups
                    elif neighbor.GetFormalCharge() == -1 and len([n for n in neighbor.GetNeighbors() if n.GetSymbol() != 'H']) == 1:
                        hydroxy_count += 1
        
        if hydroxy_count > 0:
            if mol.HasSubstructMatch(pattern1):
                return True, f"Hydroxycinnamic acid (free acid) with {hydroxy_count} hydroxy group(s)"
            elif mol.HasSubstructMatch(pattern2):
                return True, f"Hydroxycinnamic acid ester with {hydroxy_count} hydroxy group(s)"
            else:
                return True, f"Hydroxycinnamic acid amide with {hydroxy_count} hydroxy group(s)"

    return False, "Cinnamic acid structure found but no hydroxy substituents on phenyl ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24689',
                          'name': 'hydroxycinnamic acid',
                          'definition': 'Any member of the class of  cinnamic '
                                        'acids carrying one or more hydroxy '
                                        'substituents.',
                          'parents': ['CHEBI:23252']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.060606060606060615 is too low.\n'
               "True positives: [('COc1cc(\\\\C=C/C(O)=O)ccc1O', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O(C1=C(O)C=C(C=C1)C=CC(O)=O)C', 'Hydroxycinnamic acid with 1 "
               "hydroxy group(s)'), "
               "('C\\\\C(=C(\\\\[H])/CC=1C=C(C=CC1O)\\\\C(\\\\[H])=C(\\\\[H])/C(=O)O)\\\\CO', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@@H]([C@@H](C)C=2C1=C(O)C(=CC2)/C=C/C(=O)O)C', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)')]\n"
               'False positives: '
               "[('O1C(CC2=CC3=C(OC(C=C3)(C)C)C=C2)(C(=C(OC)C1=O)C4=CC(O)=C(O)C=C4)C(OC)=O', "
               "'Hydroxycinnamic acid with 2 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OCC)(CC2=CC3=C(OC(C)(C)C(C3)O)C=C2)C(=C1O)C4=CC=C(O)C=C4', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O1[C@]2(C[C@]3(N([C@@](C2)(C=4C(=CC(OC)=C(OC)C4)C=5C=C(C=CC1=O)C=CC5O)[H])CCCC3)[H])[H]', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('S(=O)(=O)(OC=1C(=O)O[C@](C1C2=CC=C(O)C=C2)(C(=O)OC)CC3=CC(=C(O)C=C3)CC=C(C)C)O', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1OCC2=C1CC[C@@H](C)C3=C2C=C(O)C(=C3)C', 'Hydroxycinnamic "
               "acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@H](CC2=CC3=C(OC(C)(C)[C@H](C3)O)C=C2)C(=C1O)C4=CC=C(O)C=C4', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@@](OC)(CC2=CC=C(O)C=C2)C(=C1O)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C(O)/C(/NC(=O)CCCCCCCC)=C/C1=CC=C(O)C=C1', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('S(=O)(=O)(OC1=C(C=C(C[C@]2(OC(=O)C(=C2C3=CC=C(O)C=C3)O)C(=O)OC)C=C1)CC=C(C)C)O', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](O)(CC2=CC=C(O)C=C2)C(=C1O)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('OC(=O)C(\\\\O)=C\\\\c1ccc(O)cc1', 'Hydroxycinnamic acid with "
               "1 hydroxy group(s)'), "
               "('O=C1O[C@](O)(C(=O)O)C(=C1CC2=CC3=C(OC(C)(C)CC3)C=C2)C4=CC=C(O)C=C4', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O/C(=C\\\\C2=CC(=C(O)C=C2)CC=C(C)C)/C(=C1)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1OC=C[C@H]([C@@]2(C1=C(O)C3=C(C=C(C)C=C3O)O2)C(=O)OC)O', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1OCCC2=CC(OC3=CC=C(C[C@]14OC(=O)C(=C4C5=CC=C(O)C=C5)O)C=C3)=C(O)C=C2', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1OC(=O)C(=C1C2=CC=C(O)C=C2)CC3=CC(=C(O)C=C3)CC=C(C)C', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('C[C@H]1C[C@@H](C)\\\\C=C(C)\\\\C[C@H](C)C(=O)N[C@@H](C)C(=O)N(C)[C@H](Cc2c(Br)[nH]c3ccccc23)C(=O)N\\\\C(=C/C(=O)O1)c1ccc(O)c(O)c1', "
               "'Hydroxycinnamic acid with 2 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC(=C(O)C=C2)CCC(O)(C)C)C(=C1O)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC2=C(O)C=C(C=C2)/C=C/C(O)=O)C(O)=O', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](O)(CC2=CC(=C(O)C=C2)CC=C(C)C)C(=C1)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O/C(=C\\\\C2=CC3=C(OC(C)(C)CC3)C=C2)/C(=C1)C4=CC=C(O)C=C4', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O1C(C(O)C(O)C(O)C1OC2=C(O)C=C(C=C2)/C=C/C(O)=O)CO', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C(O)C1=CC2=C(C(O)=CC(=C2CC1)C)C(C)C', 'Hydroxycinnamic "
               "acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC(=C(O)C=C2)C[C@H](O)C(O)(C)C)C(=C1O)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC(=C(O)C=C2)CCC(O)(C)C)C(=C1OC)C3=CC(O)=C(O)C=C3', "
               "'Hydroxycinnamic acid with 2 hydroxy group(s)'), "
               "('O1C(C2=CC(O)=C(O)C=C2)=C/C(=C/C3=CC(O)=CC(O)=C3)/C1=O', "
               "'Hydroxycinnamic acid with 2 hydroxy group(s)'), "
               "('O=C1OC(CCCCCCC)=NC1=CC2=CC=C(O)C=C2', 'Hydroxycinnamic acid "
               "with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=C(O)C(=C(OC)C=C2)CC=C(C)C)C(=C1O)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C(OC)C1=C(O)C2=C([C@H](O)[C@H](C)OC2)C(=C1C=C(OC)C(=O)O)C=3C=4C(C(O)=C5C3[C@H](OC(=O)C)[C@H](C)OC5)=C(OC)C=C(C4)OC', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@H](OC)C(=C1CC2=CC(=C(O)C=C2)CC=C(C)C)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1OCC=2C(O)=CC=C(C2C=C1)CC=C(C)C', 'Hydroxycinnamic acid "
               "with 1 hydroxy group(s)'), "
               "('O=C1O[C@](OC)(CC2=CC=C(O)C=C2)C(=C1O)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('COc1ccc2OC[C@H]([C@H](OS([O-])(=O)=O)c2c1)c1cc(\\\\C=C\\\\C(O)=O)cc(OC)c1O', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C/1OC(C2=CC(O)=C(O)C=C2)C(\\\\C1=C/C3=CC(O)=C(O)C=C3)C(=O)O', "
               "'Hydroxycinnamic acid with 2 hydroxy group(s)'), "
               "('BrC1=CC(C\\\\2=C(C(O/C2=C\\\\C3=CC(Br)=C(O)C(Br)=C3)=O)C(=O)C4=CC(Br)=C(O)C(Br)=C4)=CC(Br)=C1O', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC(=C(O)C=C2)CC=C(C)C)C(=C1OC)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC=C(O)C=C2)C(=C1OC)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](O)(C(=O)OCC)C(=C1CC2=CC3=C(OC(C)(C)CC3)C=C2)C4=CC=C(O)C=C4', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('Oc1ccc(\\\\C=C2\\\\C=C(OC2=O)c2ccc(O)c(O)c2)cc1O', "
               "'Hydroxycinnamic acid with 2 hydroxy group(s)'), "
               "('O=C1OC(=O)C(=C1C2=CC=C(O)C=C2)CC3=CC4=C(OC(C)(C)CC4)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('C1(O)=C([C@@](C([O-])=O)(OC1=O)CC2=CC=C(C=C2)O)C3=CC=C(C=C3)O', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@H](CC2=CC3=C(OC(C3)C(O)(C)C)C=C2)C(=C1O)C4=CC=C(O)C=C4', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC(OC)=C(O)C(=C2)CC=C(C)C)C(=C1O)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@H](O)C(=C1CC2=CC3=C(OC(C)(C)CC3)C=C2)C4=CC=C(O)C=C4', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1OC(=O)C(=C1C2=CC=C(O)C=C2)CC3=CC(=C(O)C=C3)CCC(O)(C)C', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC(=C(O)C=C2)C[C@H](O)C(O)(C)C)C(=C1OCC)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC=2C=C(C=CC2O)/C=C/C(O)=O)C(O)=O', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('C(/C(=C/C1=CC=C(C=C1)O)/N)(O)=O', 'Hydroxycinnamic acid with "
               "1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OCC)(CC2=CC(=C(O)C=C2)CC=C(C)C)C(=C1O)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O1C(C(C(=O)C=2C1=C3C(OC(C=C3)(C)C)=C(C2O)/C(/C4=CC=CC=C4)=C\\\\C(O)=O)C)C', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1OC(CCC/C=C\\\\CCCCCC)=NC1=CC2=CC=C(O)C=C2', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O1[C@@](CC2=CC=C(O)C(=C2)CC=C(C)C)(C(=C(O)C1=O)C3=CC=C(O)C=C3)C(OC)=O', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O(C=1C(O)=C(/C(=C\\\\C2=CC(OC)=C(O)C=C2)/C(=O)O)C=C(C1)/C=C/C(=O)O)C', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC3=C(OC(C)(C)C(C3)O)C=C2)C(=C1O)C4=CC=C(O)C=C4', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C(O)/C(/NC(=O)CCCCCCC(C)C)=C/C1=CC=C(O)C=C1', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('[H][C@]12C[C@@]3([H])CCCCN3[C@@]([H])(C1)C1=CC(OC)=C(OC)C=C1C1=CC(=CC=C1O)\\\\C=C/C(=O)O2', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC3=C(OC(C)(C)[C@H](C3)O)C=C2)C(=C1OC)C4=CC=C(O)C=C4', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('[K+].COc1ccc2OC[C@H]([C@H](OS([O-])(=O)=O)c2c1)c1cc(\\\\C=C\\\\C(O)=O)cc(OC)c1O', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC3=C(OC(C)(C)CC3)C=C2)C(=C1O)C4=CC=C(O)C=C4', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](O)(C(=O)OC)C(=C1CC2=CC3=C(OC(C)(C)CC3)C=C2)C4=CC=C(O)C=C4', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1OC(=O)C(=C1C2=CC=C(O)C=C2)CC3=CC(=C(O)C=C3)C[C@@H]4OC4(C)C', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC(=C(O)C=C2)C[C@H](O)C(=C)C)C(=C1O)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OCCC2=CC=C(O)C=C2)(CC3=CC=C(O)C=C3)C(=C1O)C4=CC=C(O)C=C4', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C/1O[C@H](C)C\\\\C1=C\\\\C2=C(O)C=C(O)C=C2C', "
               "'Hydroxycinnamic acid with 2 hydroxy group(s)'), "
               "('O=C1O[C@@](O)(C(=O)OC)C(=C1CC2=CC(=C(O)C=C2)CC=C(C)C)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C(O)/C(/NC(=O)CCCCCCCCCCC)=C/C1=CC(=C(O)C=C1)C', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC3=C(O[C@H](C3)C(O)(C)C)C=C2)C(=C1O)C4=CC=C(O)C=C4', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1OC(=O)C(=C1C2=CC=C(O)C=C2)CC(C)C', 'Hydroxycinnamic acid "
               "with 1 hydroxy group(s)'), "
               "('O=C1O[C@@H](C=2C(O)=C(O)C(=CC2C1=C3C(=O)C=C(O)C4=C3C=C5[C@@H](O)C(=C)OC(C5=C4O)=O)O)CCCCCCC', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('ClC1=C(O)C2=C(C=CC(OC2)=O)C=C1', 'Hydroxycinnamic acid with "
               "1 hydroxy group(s)'), "
               "('O1C(CC2=CC(=C(O)C=C2)CC=C(C)C)(C(C3=CC(=C(O)C(O)=C3)CC=C(C)C)=C(OC)C1=O)C(OC)=O', "
               "'Hydroxycinnamic acid with 2 hydroxy group(s)'), "
               "('O=C(O)/C(/NC(=O)/C=C/CCCCCCCCC)=C\\\\C1=CC(=C(O)C=C1)C', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC(=C(OCC=C(C)C)C=C2)CC=C(C)C)C(=C1OC)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1OC(CCCCCCCCCC)=NC1=CC2=CC=C(O)C=C2', 'Hydroxycinnamic "
               "acid with 1 hydroxy group(s)'), "
               "('COc1ccc2OC[C@H]([C@H](OS(O)(=O)=O)c2c1)c1cc(\\\\C=C\\\\C(O)=O)cc(OC)c1O', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC(=C(O)C=C2)CC=C(C)C)C(=C1OC([C@@H](O)CC3=C(O)C=CC(=C3)C[C@]4(OC(=O)C(=C4C5=CC=C(O)C=C5)O)C(=O)OC)(C)C)C6=CC=C(O)C=C6', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('[H][C@]12CC[C@]34OC(=O)[C@@](O)([C@@]3([H])[C@]1(C)CCCC2(C)C)C12Oc3cc(OC)c(C(C)=O)c(O)c3C=C1C(=O)O[C@@]42[H]', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC3=C(OC(C)(C)C=C3)C=C2)C(=C1O)C4=CC=C(O)C=C4', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC(=C(O)C=C2)C[C@@H](O)C(O)(C)C)C(=C1OC)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('Oc1cccc2C=CC(=O)OCc12', 'Hydroxycinnamic acid with 1 hydroxy "
               "group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC3=C(OC(C3)C(O)(C)C)C=C2)C(=C1O)C4=CC(=C(O)C=C4)CC=C(C)C', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1OC=C(C)C([C@@]2(C1=C(O)C3=C(C=CC=C3O)O2)C(=O)OC)=O', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C(O)/C(/NC(=O)CCCCCCCCC)=C/C1=CC=C(O)C=C1', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('ClC1=C(O)C=C(/C=C(\\\\NC(=O)[C@@H](NC(=O)C[C@@H](N)CCCCN)C(O)(C)C)/C(=O)O)C=C1O', "
               "'Hydroxycinnamic acid with 2 hydroxy group(s)'), "
               "('O(C=1C(O)=C(C2=C(O)C(OC)=CC(=C2)/C=C/C(O)=O)C=C(C1)/C=C(\\\\OC3=C(OC)C=C(C=C3)/C=C/C(O)=O)/C(O)=O)C', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC(=C(O)C=C2)CCC(OC)(C)C)C(=C1O)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('Oc1ccc(cc1O)\\\\C=C1/C=C(OC1=O)c1ccc(O)c(O)c1', "
               "'Hydroxycinnamic acid with 2 hydroxy group(s)'), "
               "('O=C1O[C@@H](CC(=O)O)C(=C1)C2=C(O)C(OC)=C(C3=CC=C(O)C=C3)C=C2OC', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C(O)/C(=C/C1=CC(O)=C(O[C@@H]2O[C@H]([C@@H](O)C)[C@H]([C@@H]2O)O)C=C1)/C', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OCC)(CC2=CC3=C(O[C@H](C3)C(O)(C)C)C=C2)C(=C1O)C4=CC=C(O)C=C4', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O(C(CC1=CC(O)=C(O)C=C1)C(O)=O)C(=O)/C=C/C2=CC(O/C(=C\\\\C3=CC(O)=C(O)C=C3)/C(O)=O)=C(O)C=C2', "
               "'Hydroxycinnamic acid with 2 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC(=C(O)C=C2)CC=C(C)C)C(=C1OCC)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O1C2=C(C(O)=C(C(O)=C2)/C=C/C(O)=O)C(=O)C=C1C3=CC(O)=C(O)C=C3', "
               "'Hydroxycinnamic acid with 2 hydroxy group(s)'), "
               "('O=C1O[C@H](O)C(=C1C)C2=CC=C(O)C=C2', 'Hydroxycinnamic acid "
               "with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=C(C=C(O)C(=C2)CC=C(C)C)CC=C(C)C)C(=C1OC)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1OC=C(C)[C@H]([C@@]2(C1=C(O)C3=C(C=CC=C3O)O2)C(=O)OC)O', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1O[C@](C(=O)OC)(CC2=CC(=C(O)C=C2)C[C@H](O)C(O)(C)C)C(=C1OC)C3=CC=C(O)C=C3', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('O=C1OC(CCCCCCCCC)=NC1=CC2=CC=C(O)C=C2', 'Hydroxycinnamic "
               "acid with 1 hydroxy group(s)'), "
               "('O1[C@@](CC2=CC=C(O)C=C2)(C(=C(O)C1=O)C3=CC=C(O)C=C3)C(OC)=O', "
               "'Hydroxycinnamic acid with 1 hydroxy group(s)'), "
               "('Oc1ccc(\\\\C=C2/CC(OC2=O)c2ccc(O)c(O)c2)cc1O', "
               "'Hydroxycinnamic acid with 2 hydroxy group(s)')]\n"
               'False negatives: '
               "[('O=C(N(CCCCN(CCCN)C(=O)/C=C/C1=CC=C(O)C=C1)CCCNC(=O)/C=C/C2=CC=C(O)C=C2)/C=C/C3=CC=C(O)C=C3', "
               "'No cinnamic acid core structure found'), "
               "('OC=1C=C(C=CC1O)/C=C/C(OC=C)=O', 'No cinnamic acid core "
               "structure found'), ('O=C(NCCCCN)C=CC1=CC(O)=C(O)C=C1', 'No "
               "cinnamic acid core structure found'), "
               "('O(C1=CC(/C=C\\\\C(=O)NCCCCN)=CC(OC)=C1O)C', 'No cinnamic "
               "acid core structure found'), "
               "('O(C1C(O)C(O)C=C(C1)C(O)=O)C(=O)/C=C/C2=CC(O)=C(O)C=C2', 'No "
               "cinnamic acid core structure found'), "
               "('OC(CCN)CNC(=O)/C=C/C1=CC(OC)=C(O)C=C1', 'No cinnamic acid "
               "core structure found'), "
               "('O1C(C(O)C(O)C(O)C1O)COC(=O)/C=C/C2=CC(OC)=C(O)C=C2', 'No "
               "cinnamic acid core structure found'), "
               "('O=C(O)C1=C(O)C(=C(C)C(=C1O)C)/C=C/C(=O)C', 'No cinnamic acid "
               "core structure found'), ('O(C1=C(C=CC(OC)=C1OC)/C=C/C(O)=O)C', "
               "'Cinnamic acid structure found but no hydroxy substituents on "
               "phenyl ring'), "
               "('OC[C@H]1O[C@@H](Oc2ccc(\\\\C=C\\\\C(O)=O)cc2)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Cinnamic acid structure found but no hydroxy substituents on "
               "phenyl ring'), "
               "('O(CCCCCCCCCCCCCCCCCCCCCCCCCCOC(=O)/C=C/C1=CC(O)=C(O)C=C1)C(=O)/C=C/C2=CC(O)=C(O)C=C2', "
               "'No cinnamic acid core structure found'), "
               "('S(OC1=C(OC)C=CC(=C1)/C=C/C(O)=O)(O)(=O)=O', 'Cinnamic acid "
               "structure found but no hydroxy substituents on phenyl ring'), "
               "('O=C(OC)/C=C/C1=CC(OC)=C(OCC2=CC=C(OCC=C=C)C=C2)C=C1', 'No "
               "cinnamic acid core structure found'), "
               "('O=C(/C=C\\\\C1=C(C(O)=CC=C1)CO)[C@@H](O)C', 'No cinnamic "
               "acid core structure found'), "
               "('O1[C@@H](OCC(C2(O)CC(OC2)=O)C)[C@H](O)[C@@H](O)[C@H](O)[C@H]1COC(=O)/C=C/C3=CC(O)=C(O)C=C3', "
               "'No cinnamic acid core structure found'), "
               "('C1(C(O)C(CO)OC(C1O)OC=2C(=CC=C(/C=C/C(=O)O)C2)OC)O', "
               "'Cinnamic acid structure found but no hydroxy substituents on "
               "phenyl ring'), "
               "('O=C1OC(=CC(=C1/C(/C(=O)OC)=C/C2=CC(O)=C(O)C=C2)O)/C=C/C3=CC(O)=C(O)C=C3', "
               "'No cinnamic acid core structure found'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](OCCC2=CC(O)=C(O)C=C2)[C@@H]1O)COC(=O)/C=C/C3=CC(O)=C(O)C=C3)[C@@H]4O[C@H]([C@H](O)[C@@H](O)[C@H]4O)C', "
               "'No cinnamic acid core structure found'), "
               "('COc1cc(\\\\C=C\\\\C(C)=O)ccc1O', 'No cinnamic acid core "
               "structure found'), "
               "('O(CCCCCCCCCCCCCCCCCCCCCCCC)C(=O)/C=C/C1=CC(O)=C(O)C=C1', 'No "
               "cinnamic acid core structure found'), "
               "('C1=CC(=C(C=C1C=C(C#N)C(=O)N)O)O', 'No cinnamic acid core "
               "structure found'), "
               "('O(CC[N+](C)(C)C)C(=O)C=CC1=CC(O)=C(O)C=C1', 'No cinnamic "
               "acid core structure found'), "
               "('C1CC1NC(=O)COC(=O)C=CC2=CC3=C(C=C2)OCO3', 'No cinnamic acid "
               "core structure found'), "
               "('[H][C@]1(O[C@H](COC(=O)\\\\C=C\\\\c2ccc(O)c(O)c2)[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1OC=C[C@@]2([H])[C@H](OC(=O)\\\\C=C\\\\c3ccc(O)c(O)c3)[C@]3([H])O[C@]3(CO)[C@@]12[H]', "
               "'No cinnamic acid core structure found')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 19,
    'num_false_positives': 100,
    'num_true_negatives': 20858,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.15966386554621848,
    'recall': 0.6785714285714286,
    'f1': 0.25850340136054417,
    'accuracy': 0.9948060611836462}