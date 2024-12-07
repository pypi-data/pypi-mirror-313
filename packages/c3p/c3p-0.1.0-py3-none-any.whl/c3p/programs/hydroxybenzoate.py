"""
Classifies: CHEBI:24675 hydroxybenzoate
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroxybenzoate(smiles: str):
    """
    Determines if a molecule is a hydroxybenzoate (benzoate derivative with carboxylate and at least one hydroxy group).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydroxybenzoate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylate group attached to aromatic ring
    carboxylate_pattern = Chem.MolFromSmarts('c-C(=O)[O-]')
    if not mol.HasSubstructMatch(carboxylate_pattern):
        return False, "No carboxylate group directly attached to aromatic ring"

    # Count carboxylate groups attached to aromatic rings
    carboxylate_matches = mol.GetSubstructMatches(carboxylate_pattern)
    if len(carboxylate_matches) != 1:
        return False, "Must have exactly one carboxylate group"

    # Get the aromatic carbon attached to carboxylate
    carboxylate_carbon = carboxylate_matches[0][0]

    # Find the aromatic ring containing the carboxylate
    rings = mol.GetRingInfo()
    carboxylate_ring = None
    for ring in rings.AtomRings():
        if carboxylate_carbon in ring:
            ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in ring_atoms):
                if all(mol.GetAtomWithIdx(i).GetSymbol() == 'C' for i in ring):
                    carboxylate_ring = set(ring)
                    break

    if not carboxylate_ring:
        return False, "Carboxylate not attached to benzene ring"

    # Check for hydroxyl groups
    hydroxyl_pattern = Chem.MolFromSmarts('[cH0]-[OH]')
    if not mol.HasSubstructMatch(hydroxyl_pattern):
        return False, "No hydroxyl group found"

    # Count hydroxyl groups on the aromatic system
    hydroxyl_matches = mol.GetSubstructMatches(hydroxyl_pattern)
    hydroxyl_count = 0
    hydroxyl_on_ring = False

    for match in hydroxyl_matches:
        aromatic_carbon = match[0]
        if aromatic_carbon in carboxylate_ring:
            hydroxyl_on_ring = True
            hydroxyl_count += 1

    if not hydroxyl_on_ring:
        return False, "No hydroxyl group on same ring as carboxylate"

    return True, f"Hydroxybenzoate with {hydroxyl_count} hydroxyl group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24675',
                          'name': 'hydroxybenzoate',
                          'definition': 'Any benzoate derivative carrying a '
                                        'single carboxylate group and at least '
                                        'one hydroxy substituent.',
                          'parents': ['CHEBI:22718', 'CHEBI:36059']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.13333333333333333 is too low.\n'
               "True positives: [('C=1(C=C(C(=C(C1)Br)O)O)C([O-])=O', "
               "'Hydroxybenzoate with 2 hydroxyl group(s)'), "
               "('COC1=C(O)C=CC(\\\\C=C\\\\C(=O)NC2=CC=C(O)C=C2C([O-])=O)=C1', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('Nc1c(O)cccc1C([O-])=O', 'Hydroxybenzoate with 1 hydroxyl "
               "group(s)'), "
               "('COc1cc(cc(C\\\\C=C(/C)CC\\\\C=C(/C)CC\\\\C=C(/C)CC\\\\C=C(/C)CC\\\\C=C(/C)CC\\\\C=C(/C)CC\\\\C=C(/C)CCC=C(C)C)c1O)C([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('C=1C(=CC(=C(O)C1OC)OC)C([O-])=O', 'Hydroxybenzoate with 1 "
               "hydroxyl group(s)'), ('[O-]C(=O)C1=CC=CC(=C1O)Cl', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)')]\n"
               'False positives: '
               "[('C=1(C(=CC(O)=CC1)C([O-])=O)NC(/C=C/C2=CC=C(O)C=C2)=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('O.O.[Na+].[Na+].Oc1ccc(cc1C([O-])=O)\\\\N=N\\\\c1ccc(cc1)C(=O)NCCC([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('C1(=C(C(=CC(=C1)O)O)C([O-])=O)/C=C/CCCC(=O)CCC[C@@H](O)C', "
               "'Hydroxybenzoate with 2 hydroxyl group(s)'), "
               "('Cc1cccc2c(cc(O)cc12)C([O-])=O', 'Hydroxybenzoate with 1 "
               "hydroxyl group(s)'), "
               "('C=1(C2=C(C(=CC1C(=O)[O-])Cl)C[C@H](OC2=O)C)O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('C=1(C(=C2C(C3=C(C=C(O)C(C([O-])=O)=C3C)C(C2=C(O)C1[O-])=O)=O)O)[C@@H]4O[C@@H]([C@H](C([C@H]4O)=O)O)CO', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('C=1C(=C2C(C3=C(C=C(O)C(C([O-])=O)=C3C)C(C2=CC1O)=O)=O)O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('[H][C@@]12CCC(C)=C[C@@]1([H])c1c(O)c(C([O-])=O)c(CCCCC)cc1OC2(C)C', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\Cc1cc(ccc1O)C([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\Cc1cc(ccc1O)C([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('[Ca+2].O1[C@]([C@H](O)[C@@H](O)[C@H](O)[C@H]1CO)(C2=C3C(=C([O-])C=C2)C(=O)C4=C(C3=O)C=C(C=C4O)C([O-])=O)[H]', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('Oc1ccc(C([O-])=O)c(O)n1', 'Hydroxybenzoate with 2 hydroxyl "
               "group(s)'), "
               "('C(C\\\\C(=C\\\\CC\\\\C(=C\\\\CC\\\\C(=C\\\\CC\\\\C(=C\\\\CC1=CC(=CC(=C1N)O)C([O-])=O)\\\\C)\\\\C)\\\\C)\\\\C)/C=C(/CCC=C(C)C)\\\\C', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('[Na+].[H][C@@]1(O[C@@](CC)(C[C@@H]1C)[C@@]1([H])CC[C@](O)(CC)[C@H](C)O1)[C@@H](CC)C(=O)[C@@H](C)[C@@H](O)[C@H](C)CCC1=C(C([O-])=O)C(O)=C(C)C=C1', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('[Na+].[Na+].[Na+].CC1=C\\\\C(C=C(C([O-])=O)C1=O)=C(\\\\c1cc(C)c(O)c(c1)C([O-])=O)c1ccccc1S([O-])(=O)=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('OC1C=Cc2c(O)cc(nc2C1O)C([O-])=O', 'Hydroxybenzoate with 1 "
               "hydroxyl group(s)'), "
               "('OC(=O)C(=O)CCc1c(O)cc([nH]c1=O)C([O-])=O', 'Hydroxybenzoate "
               "with 1 hydroxyl group(s)'), "
               "('Oc1cc([nH]c(=O)c1CCC=O)C([O-])=O', 'Hydroxybenzoate with 1 "
               "hydroxyl group(s)'), ('C=1C=C(C=C(C1O)OC)C([O-])=O.[Na+]', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('C(C=1C=CC(=CC1)O)([O-])=O.[Na+]', 'Hydroxybenzoate with 1 "
               "hydroxyl group(s)'), ('Cc1ncc(cc1O)C([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('Oc1ccc([nH]1)C([O-])=O', 'Hydroxybenzoate with 1 hydroxyl "
               "group(s)'), ('Oc1cc(O)c(C([O-])=O)c(OC(=O)c2ccc(O)c(O)c2)c1', "
               "'Hydroxybenzoate with 2 hydroxyl group(s)'), "
               "('Cc1cccc2c(C([O-])=O)c(O)ccc12', 'Hydroxybenzoate with 1 "
               "hydroxyl group(s)'), "
               "('Cc1c(C([O-])=O)c(O)cc2cc3Cc4cc(O)cc(O)c4C(=O)c3c(O)c12', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('C1(C(=O)[O-])=CC(=C(C(=C1)O)O)O.[Na+]', 'Hydroxybenzoate "
               "with 3 hydroxyl group(s)'), ('Oc1c(ccc2ccccc12)C([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('[H]C(=CC(=O)C([O-])=O)c1c(O)cc(nc1O)C([O-])=O', "
               "'Hydroxybenzoate with 2 hydroxyl group(s)'), "
               "('C1(=C(C=CC(=C1O)Cl)Cl)C([O-])=O', 'Hydroxybenzoate with 1 "
               "hydroxyl group(s)'), ('[Na+].Nc1ccc(C([O-])=O)c(O)c1', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('C=1(C(=C2C(C3=C(C=C(O)C(C([O-])=O)=C3C)C(C2=CC1[O-])=O)=O)O)[C@@H]4O[C@@H]([C@H]([C@@H]([C@H]4O)O)O)CO', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('C=1(C([O-])=O)C=CC(=C(C1O)N)OC', 'Hydroxybenzoate with 1 "
               "hydroxyl group(s)'), ('Oc1cccc2c(O)cc(nc12)C([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('Oc1cc(C([O-])=O)c(O)c2ccccc12', 'Hydroxybenzoate with 2 "
               "hydroxyl group(s)'), ('C1(=CC=C(C=C1NC(C)=O)C([O-])=O)O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('Cc1c(C([O-])=O)c(O)cc2cc3C(=O)c4cc([O-])cc(O)c4C(=O)c3c(O)c12', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('[NH3+]C(CC(=O)c1cccc2oc3cc(=O)c4nc(cc(O)c4c3nc12)C([O-])=O)C([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('C1(=C(C=CC=C1)O)C(=O)[O-].C[N+](CCO)(C)C', 'Hydroxybenzoate "
               "with 1 hydroxyl group(s)'), "
               "('C1(=CN=C(C(=C1C(=O)[O-])O)C)C=O', 'Hydroxybenzoate with 1 "
               "hydroxyl group(s)'), "
               "('[NH3+]C(CC(=O)c1cccc2Oc3cc(O)c4nc(cc(O)c4c3Nc12)C([O-])=O)C([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('COc1cc(C)c2ccc(O)c(C([O-])=O)c2c1', 'Hydroxybenzoate with 1 "
               "hydroxyl group(s)'), ('[Na+].C=1C(=CC(=C(O)C1OC)OC)C([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('Cc1cc(O)cc2c(C([O-])=O)c(O)ccc12', 'Hydroxybenzoate with 1 "
               "hydroxyl group(s)'), ('Cc1ncc(C([O-])=O)c(CO)c1O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('[Na+].OC1=C(C=C(/N=N/C2=CC=C(N)C=C2)C=C1)C([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('COc1cc(cc(O)c1O)C([O-])=O', 'Hydroxybenzoate with 2 hydroxyl "
               "group(s)'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\Cc1cc(ccc1O)C([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('Oc1ccc(cn1)C([O-])=O', 'Hydroxybenzoate with 1 hydroxyl "
               "group(s)'), ('Oc1cc(cc(O)c(=O)c1)C([O-])=O', 'Hydroxybenzoate "
               "with 2 hydroxyl group(s)'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\Cc1cc(ccc1O)C([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('C=1C(=C2C(C3=C(C=C(O)C(C([O-])=O)=C3C)C(C2=C(O)C1O)=O)=O)O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('Oc1ccccc1C([O-])=O.C[NH+](C)CCOC(c1ccccc1)c1ccccc1', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('[Na+].Oc1ccccc1C([O-])=O', 'Hydroxybenzoate with 1 hydroxyl "
               "group(s)'), ('Oc1ccc2c(O)cc(nc2c1O)C([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('Oc1ccc(cc1C([O-])=O)\\\\N=N\\\\c1ccc(cc1)C(=O)NCCC([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('CC1=CC(=C(C)C(=C1C(=O)OC=2C=C(C)C(=C(C2C)O)C(=O)[O-])O)O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('COc1cc(O)cc(C([O-])=O)c1C(=O)c1c(O)cc(C)cc1O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('OC(=O)C(=O)\\\\C=C\\\\c1c(O)cc([nH]c1=O)C([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('Cc1c(C([O-])=O)c(O)cc2cc3C(=O)c4cc(O)cc(O)c4C(=O)c3c(O)c12', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('C1=2C(=C(C=C3C(N(C(C(=CC=C1)C23)=O)C=4C=CC(=C(C4)C(=O)[O-])O)=O)S([O-])(=O)=O)N.[Na+].[Na+]', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('C1(=C(C2=C(C=CC=C2)C(=C1CC=C(C)C)O)O)C(=O)[O-]', "
               "'Hydroxybenzoate with 2 hydroxyl group(s)'), "
               "('Cc1ncc(CO)c(C([O-])=O)c1O', 'Hydroxybenzoate with 1 hydroxyl "
               "group(s)'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\CC\\\\C(C)=C\\\\Cc1cc(ccc1O)C([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('[Na+].OC1=C(C=C(O)C=C1)C([O-])=O', 'Hydroxybenzoate with 2 "
               "hydroxyl group(s)'), "
               "('CC1=CC(=C(C=O)C(=C1C(=O)OC=2C=C(C)C(=C(C2C)O)C(=O)[O-])O)O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('COc1cc(O)cc(C([O-])=O)c1C(=O)c1c(O)cc(C)cc1[O-]', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('CCCCCc1cc(O)cc(O)c1C([O-])=O', 'Hydroxybenzoate with 2 "
               "hydroxyl group(s)'), ('C=1(C=CC(=CC1C(=O)[O-])O)N', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('C(C=1C(O)=C2C(CC(C)OC2=O)=CC1)([O-])=O', 'Hydroxybenzoate "
               "with 1 hydroxyl group(s)'), "
               "('[Na+].O1C(CC(C1C(CC)C(=O)C(C(O)C(CCC2=C(C(O)=C(C=C2)C)C([O-])=O)C)C)C)(C3OC(C(O)(CC3)CC)C)CC', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('Cc1cc(O)cc(O)c1C(=O)Oc1cc(C)c(C([O-])=O)c(O)c1', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('C=1(C(=C2C(C3=C(C=C(O)C(C([O-])=O)=C3C)C(C2=C(O)C1[O-])=O)=O)O)[C@@H]4O[C@@H]([C@H]([C@@H]([C@H]4O)O)O)CO', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('Oc1cc(nc2ccccc12)C([O-])=O', 'Hydroxybenzoate with 1 "
               "hydroxyl group(s)'), "
               "('CC1=CC(=C(CO)C(=C1C(=O)OC=2C=C(C)C(=C(C2C)O)C(=O)[O-])O)O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('CCCCCC1=CC2=C(C=CC(C)(CCC=C(C)C)O2)C(O)=C1C([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('[H][C@@]1(O[C@@](CC)(C[C@@H]1C)[C@@]1([H])CC[C@](O)(CC)[C@H](C)O1)[C@@H](CC)C(=O)[C@@H](C)[C@@H](O)[C@H](C)CCC1=C(C([O-])=O)C(O)=C(C)C=C1', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)'), "
               "('OC(=O)CCc1c(O)cc([nH]c1=O)C([O-])=O', 'Hydroxybenzoate with "
               "1 hydroxyl group(s)'), ('Oc1cc(cc([O-])c(=O)c1)C([O-])=O', "
               "'Hydroxybenzoate with 1 hydroxyl group(s)')]\n"
               'False negatives: []',
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 6,
    'num_false_positives': 60,
    'num_true_negatives': 183809,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.09090909090909091,
    'recall': 1.0,
    'f1': 0.16666666666666669,
    'accuracy': 0.9996736913664174}