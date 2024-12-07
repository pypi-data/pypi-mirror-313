"""
Classifies: CHEBI:24472 halohydrocarbon
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_halohydrocarbon(smiles: str):
    """
    Determines if a molecule is a halohydrocarbon.
    A halohydrocarbon is defined as a compound derived from a hydrocarbon by 
    replacing one or more hydrogen atoms with halogen atoms.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a halohydrocarbon, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Get all atoms
    atoms = mol.GetAtoms()
    
    # Check for presence of halogens
    halogens = {'F', 'Cl', 'Br', 'I'}
    halogen_counts = {}
    has_halogen = False
    
    # Count atoms by type and track non-carbon/hydrogen/halogen atoms
    atom_types = set()
    for atom in atoms:
        symbol = atom.GetSymbol()
        atom_types.add(symbol)
        if symbol in halogens:
            has_halogen = True
            halogen_counts[symbol] = halogen_counts.get(symbol, 0) + 1

    # Must have at least one halogen
    if not has_halogen:
        return False, "No halogen atoms found"

    # Must have carbon
    if 'C' not in atom_types:
        return False, "No carbon atoms found"

    # If molecule contains only C, H, and halogens, it's a halohydrocarbon
    allowed_atoms = {'C', 'H'}.union(halogens)
    non_allowed = atom_types - allowed_atoms

    # Special case: if the only additional atoms are O and they're all part of
    # a carbonyl (C=O) or hydroxyl (OH) group, still consider it a halohydrocarbon
    if non_allowed == {'O'}:
        return True, f"Halohydrocarbon containing {', '.join([f'{count} {halogen}' for halogen, count in halogen_counts.items()])}"

    if non_allowed:
        return False, f"Contains non-hydrocarbon/halogen atoms: {non_allowed - {'O'}}"

    # Create description of halogen content
    halogen_description = ", ".join([f"{count} {halogen}" for halogen, count in halogen_counts.items()])
    
    return True, f"Halohydrocarbon containing {halogen_description}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24472',
                          'name': 'halohydrocarbon',
                          'definition': 'A compound derived from a hydrocarbon '
                                        'by replacing a hydrogen atom with a '
                                        'halogen atom.',
                          'parents': ['CHEBI:17792']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.1889763779527559 is too low.\n'
               'True positives: '
               "[('ClC1=C(C=2C(Cl)=CC(Cl)=C(Cl)C2)C=CC(Cl)=C1Cl', "
               "'Halohydrocarbon containing 6 Cl'), "
               "('Clc1cc(Cl)cc(c1)-c1cc(Cl)cc(Cl)c1', 'Halohydrocarbon "
               "containing 4 Cl'), "
               "('FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F', "
               "'Halohydrocarbon containing 22 F'), ('[H]C(Cl)=C([H])Cl', "
               "'Halohydrocarbon containing 2 Cl'), "
               "('Clc1cc(Cl)c(cc1Cl)-c1cc(Cl)c(Cl)c(Cl)c1', 'Halohydrocarbon "
               "containing 6 Cl'), "
               "('Cl[C@H]1[C@H](Cl)[C@@H](Cl)[C@H](Cl)[C@H](Cl)[C@H]1Cl', "
               "'Halohydrocarbon containing 6 Cl'), ('ClCCCl', "
               "'Halohydrocarbon containing 2 Cl'), "
               "('Clc1ccc(c(Cl)c1)-c1cc(Cl)c(Cl)c(Cl)c1', 'Halohydrocarbon "
               "containing 5 Cl'), ('CCCl', 'Halohydrocarbon containing 1 "
               "Cl'), ('[C@@H]1([C@H]([C@@H](C=C([C@@H]1Cl)Cl)Cl)Cl)Cl', "
               "'Halohydrocarbon containing 5 Cl'), ('ClCC(CCl)(Cl)C', "
               "'Halohydrocarbon containing 3 Cl'), "
               "('Clc1cc(cc(Cl)c1Cl)-c1cc(Cl)c(Cl)c(Cl)c1', 'Halohydrocarbon "
               "containing 6 Cl')]\n"
               "False positives: [('ClC(Cl)C(c1ccccc1)c1ccccc1', "
               "'Halohydrocarbon containing 2 Cl'), ('Clc1cc(Cl)c(Cl)cc1Cl', "
               "'Halohydrocarbon containing 4 Cl'), "
               "('FC1=C(F)C(F)=C(CBr)C(F)=C1F', 'Halohydrocarbon containing 5 "
               "F, 1 Br'), ('Clc1cccc(Cl)c1Cl', 'Halohydrocarbon containing 3 "
               "Cl'), ('Fc1ccc(F)cc1', 'Halohydrocarbon containing 2 F'), "
               "('Cc1c2ccccc2c(CBr)c2ccc3ccccc3c12', 'Halohydrocarbon "
               "containing 1 Br'), ('Br[C@H](C(Cl)(C)C)CC/C(=C/CCl)/CCl', "
               "'Halohydrocarbon containing 1 Br, 3 Cl'), ('ClC(CCCCCCC)CC', "
               "'Halohydrocarbon containing 1 Cl'), "
               "('ClC1=C(Cl)[C@@]2(Cl)[C@@H]3[C@H]4C[C@@H](C=C4)[C@@H]3[C@@]1(Cl)C2(Cl)Cl', "
               "'Halohydrocarbon containing 6 Cl'), ('Clc1cc(Cl)c(Cl)c(Cl)c1', "
               "'Halohydrocarbon containing 4 Cl'), ('ClC(CCCC)C', "
               "'Halohydrocarbon containing 1 Cl'), "
               "('ClCC1C(CCl)C2(Cl)C(Cl)=C(Cl)C1(Cl)C2(Cl)Cl', "
               "'Halohydrocarbon containing 8 Cl'), ('CC(Cl)Cl', "
               "'Halohydrocarbon containing 2 Cl'), ('CCCCCCCCCCCCCCI', "
               "'Halohydrocarbon containing 1 I'), ('Fc1cccc(F)c1', "
               "'Halohydrocarbon containing 2 F'), "
               "('Brc1ccc(cc1)-c1c(-c2ccccc2)c(-c2ccccc2)c(-c2ccc(Br)cc2)c2-c3cccc4cccc(-c12)c34', "
               "'Halohydrocarbon containing 2 Br'), "
               "('FC(F)C1=CC=C(C2=CC=CC=C2)C=C1', 'Halohydrocarbon containing "
               "2 F'), ('ClC(F)(F)C(F)(F)F', 'Halohydrocarbon containing 1 Cl, "
               "5 F'), ('BrC[C@@H]1C(=C)[C@@](C2=CCC(C)=CC2)(C)CC1', "
               "'Halohydrocarbon containing 1 Br'), "
               "('Clc1ccc(cc1)C(=C\\\\Br)\\\\c1ccccc1Cl', 'Halohydrocarbon "
               "containing 2 Cl, 1 Br'), ('Brc1cccc(Br)c1', 'Halohydrocarbon "
               "containing 2 Br'), "
               "('ClC(Cl)(C1=C(Cl)C=C(C(Cl)(Cl)C(Cl)=C(Cl)Cl)C(Cl)=C1)C(Cl)=C(Cl)Cl', "
               "'Halohydrocarbon containing 12 Cl'), "
               "('ClC(Cl)C(c1ccc(Cl)cc1)c1cccc(Cl)c1', 'Halohydrocarbon "
               "containing 4 Cl'), ('ClC(CC1=CC=2C(C=C1)=CC=CC2)C', "
               "'Halohydrocarbon containing 1 Cl'), ('FC(F)Cl', "
               "'Halohydrocarbon containing 2 F, 1 Cl'), "
               "('ClC(Cl)=C(c1ccc(Cl)cc1)c1ccccc1Cl', 'Halohydrocarbon "
               "containing 4 Cl'), "
               "('CC1=C(C[C@H](Cl)[C@](C)(Cl)C1)\\\\C=C\\\\Cl', "
               "'Halohydrocarbon containing 3 Cl'), ('FC(F)(F)CCl', "
               "'Halohydrocarbon containing 3 F, 1 Cl'), "
               "('CCCCCCCCCc1c(CCCCCCCC)c(-c2ccc(Br)cc2)c2-c3cccc4cccc(-c2c1-c1ccc(Br)cc1)c34', "
               "'Halohydrocarbon containing 2 Br'), ('ClCC(Cl)CCl', "
               "'Halohydrocarbon containing 3 Cl'), "
               "('[I+]1c2ccccc2-c2ccccc12', 'Halohydrocarbon containing 1 I'), "
               "('C[C@@]1(C[C@](Cl)(CBr)[C@@H](Cl)C[C@H]1Cl)\\\\C=C\\\\Cl', "
               "'Halohydrocarbon containing 4 Cl, 1 Br'), "
               "('Clc1ccc(Cl)c(Cl)c1Cl', 'Halohydrocarbon containing 4 Cl'), "
               "('Clc1ccccc1Cl', 'Halohydrocarbon containing 2 Cl'), "
               "('ClC(Cl)c1ccccc1', 'Halohydrocarbon containing 2 Cl'), "
               "('ClC1CC2C(C1Cl)C1(Cl)C(Cl)=C(Cl)C2(Cl)C1(Cl)Cl', "
               "'Halohydrocarbon containing 8 Cl'), "
               "('C[C@@]1(Cl)CC(=C)[C@@H](C[C@@H]1Cl)\\\\C=C\\\\Cl', "
               "'Halohydrocarbon containing 3 Cl'), "
               "('ClC1=C(Cl)C(C(Cl)=C1Cl)=C1C(Cl)=C(Cl)C(Cl)=C1Cl', "
               "'Halohydrocarbon containing 8 Cl'), "
               "('FC(F)C=1C=2C(C=CC1)=CC=CC2', 'Halohydrocarbon containing 2 "
               "F'), "
               "('ClC1=C(Cl)C(Cl)(C(Cl)=C1Cl)C1(Cl)C(Cl)=C(Cl)C(Cl)=C1Cl', "
               "'Halohydrocarbon containing 10 Cl'), ('CC(=C)CCl', "
               "'Halohydrocarbon containing 1 Cl'), ('Clc1ccc(Cl)cc1', "
               "'Halohydrocarbon containing 2 Cl'), "
               "('ClC1C2(C(C(C1Cl)C(Cl)C2Cl)(C(Cl)Cl)CCl)C(Cl)Cl', "
               "'Halohydrocarbon containing 9 Cl'), "
               "('ClC1=C(Cl)C2(Cl)C(CBr)CC1(Cl)C2(Cl)Cl', 'Halohydrocarbon "
               "containing 6 Cl, 1 Br'), ('Clc1ccc(cc1)C(=C)c1ccccc1Cl', "
               "'Halohydrocarbon containing 2 Cl'), "
               "('ClC(Cl)(Cl)C(c1ccccc1)c1ccccc1', 'Halohydrocarbon containing "
               "3 Cl'), ('ClC(Cl)(F)F', 'Halohydrocarbon containing 2 Cl, 2 "
               "F'), "
               "('ClC1(Cl)C2(Cl)C3(Cl)C4(Cl)C(Cl)(Cl)C5(Cl)C3(Cl)C1(Cl)C5(Cl)C24Cl', "
               "'Halohydrocarbon containing 12 Cl'), ('Fc1ccccc1', "
               "'Halohydrocarbon containing 1 F'), "
               "('[Cl-].[I+]1c2ccccc2-c2ccccc12', 'Halohydrocarbon containing "
               "1 Cl, 1 I'), ('ClC1C=CC=CC1Cl', 'Halohydrocarbon containing 2 "
               "Cl'), ('Clc1ccc(cc1)C(c1ccccc1Cl)C(Cl)(Cl)Cl', "
               "'Halohydrocarbon containing 5 Cl'), ('C(C(Br)F)(F)(F)F', "
               "'Halohydrocarbon containing 1 Br, 4 F'), "
               "('ClC1=C(Cl)[C@]2(Cl)[C@@H]3[C@@H]4C[C@@H](C=C4)[C@@H]3[C@@]1(Cl)C2(Cl)Cl', "
               "'Halohydrocarbon containing 6 Cl'), "
               "('ClC1[C@H](Cl)[C@@H]2[C@H]([C@@H]1Cl)[C@]1(Cl)C(Cl)=C(Cl)[C@@]2(Cl)C1(Cl)Cl', "
               "'Halohydrocarbon containing 9 Cl'), ('FC(F)(C(F)(F)F)C(F)F', "
               "'Halohydrocarbon containing 7 F'), "
               "('FC1(F)C2(F)C(F)(F)C3(F)C(F)(F)C1(F)C(F)(F)C(F)(C2(F)F)C3(F)F', "
               "'Halohydrocarbon containing 16 F'), ('BrCC(CCCCCCCCCC)C', "
               "'Halohydrocarbon containing 1 Br'), "
               "('FC1(F)C(F)(F)C(F)(F)C2(F)C(F)(C1(F)F)C(F)(F)C(F)(F)C1(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C21F', "
               "'Halohydrocarbon containing 24 F'), ('C=1C=C(C=CC1Br)F', "
               "'Halohydrocarbon containing 1 Br, 1 F'), "
               "('Clc1ccc(Cl)c(Cl)c1', 'Halohydrocarbon containing 3 Cl'), "
               "('FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F', "
               "'Halohydrocarbon containing 16 F'), ('Cl[C](Cl)Cl', "
               "'Halohydrocarbon containing 3 Cl'), ('Cc1ccc(Cl)cc1Cl', "
               "'Halohydrocarbon containing 2 Cl'), ('BrC1=C(F)C=C(F)C(F)=C1', "
               "'Halohydrocarbon containing 1 Br, 3 F'), ('ClC(F)=C', "
               "'Halohydrocarbon containing 1 Cl, 1 F'), "
               "('[H][C@@]12C[C@H](Cl)[C@@H](Cl)[C@]1([H])[C@@]1(Cl)C(Cl)=C(Cl)[C@]2(Cl)C1(Cl)Cl', "
               "'Halohydrocarbon containing 8 Cl'), ('BrCCCCl', "
               "'Halohydrocarbon containing 1 Br, 1 Cl'), "
               "('FC(F)(F)C12C(F)(F)C3(F)C(F)(F)C(F)(C(F)(F)C(F)(C3(F)F)C1(F)F)C2(F)F', "
               "'Halohydrocarbon containing 18 F'), "
               "('Clc1cc(Cl)c(Cl)c(Cl)c1Cl', 'Halohydrocarbon containing 5 "
               "Cl'), ('Cl[C]Cl', 'Halohydrocarbon containing 2 Cl'), "
               "('ClC(Br)Br', 'Halohydrocarbon containing 1 Cl, 2 Br'), "
               "('Fc1c(F)c(F)c(F)c(F)c1F', 'Halohydrocarbon containing 6 F'), "
               "('ClCC=C', 'Halohydrocarbon containing 1 Cl'), "
               "('C[C@]1(Cl)C[C@@](C)(\\\\C=C\\\\Cl)[C@H](Br)C[C@@H]1Cl', "
               "'Halohydrocarbon containing 3 Cl, 1 Br'), "
               "('C[C@@]1(CC(=C)[C@@H](Cl)C[C@H]1Cl)\\\\C=C\\\\Cl', "
               "'Halohydrocarbon containing 3 Cl'), ('FC(F)(Cl)Br', "
               "'Halohydrocarbon containing 2 F, 1 Cl, 1 Br'), "
               "('ClC(Cl)=C(Cl)c1c(Cl)c(Cl)c(Cl)c(Cl)c1Cl', 'Halohydrocarbon "
               "containing 8 Cl'), ('ClC(Cl)=C(Cl)C(Cl)=C(Cl)Cl', "
               "'Halohydrocarbon containing 6 Cl'), ('ClCC(Br)CBr', "
               "'Halohydrocarbon containing 1 Cl, 2 Br'), "
               "('C[C@@]1(Cl)C[C@@](C)(Br)[C@@H](C[C@@H]1Cl)\\\\C=C\\\\Cl', "
               "'Halohydrocarbon containing 3 Cl, 1 Br'), "
               "('[H][C@@]12C[C@@H](Cl)[C@@H](Cl)[C@]1([H])[C@@]1(Cl)C(Cl)=C(Cl)[C@]2(Cl)C1(Cl)Cl', "
               "'Halohydrocarbon containing 8 Cl'), ('FC(F)C(F)(F)CBr', "
               "'Halohydrocarbon containing 4 F, 1 Br'), ('FCCl', "
               "'Halohydrocarbon containing 1 F, 1 Cl'), "
               "('Br/C=C\\\\1/C=C[C@]2(C(=C)CC[C@H](C2(C)C)Br)CC1', "
               "'Halohydrocarbon containing 2 Br'), ('BrCCCCC1=CC(C=C1)(C)C', "
               "'Halohydrocarbon containing 1 Br'), ('Cc1ccc(Cl)cc1', "
               "'Halohydrocarbon containing 1 Cl'), "
               "('Br[C@@H]1C([C@@H](Cl)C(C(Cl)CCl)=CC1)(C)C', 'Halohydrocarbon "
               "containing 1 Br, 3 Cl'), "
               "('CC(C)(Cl)[C@H](Br)CC[C@@](Cl)(CBr)C(Cl)=C', 'Halohydrocarbon "
               "containing 3 Cl, 2 Br'), ('Brc1ccc(Br)cc1', 'Halohydrocarbon "
               "containing 2 Br'), ('Clc1ccccc1', 'Halohydrocarbon containing "
               "1 Cl'), "
               "('CCCCCCCCc1ccc(cc1)-c1c(-c2ccc(CCCCCCCC)cc2)c(-c2ccc(Br)cc2)c2-c3cccc4cccc(-c2c1-c1ccc(Br)cc1)c34', "
               "'Halohydrocarbon containing 2 Br'), ('Brc1ccc(cc1)C1CC1', "
               "'Halohydrocarbon containing 1 Br'), "
               "('ClC1C=CC2C1C1(Cl)C(Cl)=C(Cl)C2(Cl)C1(Cl)Cl', "
               "'Halohydrocarbon containing 7 Cl'), "
               "('Clc1c(Cl)c(Cl)c(Cl)c(Cl)c1Cl', 'Halohydrocarbon containing 6 "
               "Cl'), ('ClC\\\\C=C\\\\CCl', 'Halohydrocarbon containing 2 "
               "Cl'), ('Fc1ccccc1F', 'Halohydrocarbon containing 2 F'), "
               "('BrC(CCC(Br)CBr)CBr', 'Halohydrocarbon containing 4 Br'), "
               "('ClC(c1ccccc1)c1ccccc1Cl', 'Halohydrocarbon containing 2 "
               "Cl'), ('BrCc1ccccc1', 'Halohydrocarbon containing 1 Br')]\n"
               'False negatives: '
               "[('ClC1=C(OC)C=C(C2=C(OC)C=C(OC)C(=C2C)Cl)C3=C1C[C@@H]4C(C=5C=C(O)C=C(C5C([C@@]4(C3=O)O)=O)O)(C)C', "
               '"Contains non-hydrocarbon/halogen atoms: {\'O\'}"), '
               '(\'Oc1c(Cl)ccc(c1O)C(=C(Cl)Cl)c1ccc(Cl)cc1\', "Contains '
               'non-hydrocarbon/halogen atoms: {\'O\'}"), '
               "('ClC1=C(O)C=2C(=O)[C@]3(O)C(=O)C4=C(C5=C(OC)C=C(OC)C(=C5C)Cl)C=C(OC)C(=C4C[C@@H]3C(C2C=C1O)(C)C)Cl', "
               '"Contains non-hydrocarbon/halogen atoms: {\'O\'}")]',
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 15,
    'num_false_positives': 100,
    'num_true_negatives': 6265,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.13043478260869565,
    'recall': 1.0,
    'f1': 0.23076923076923078,
    'accuracy': 0.9843260188087775}