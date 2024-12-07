"""
Classifies: CHEBI:25036 lignan
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem.Draw import IPythonConsole

def is_lignan(smiles: str):
    """
    Determines if a molecule is a lignan based on structural characteristics.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a lignan, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for presence of aromatic rings
    ring_info = mol.GetRingInfo()
    aromatic_rings = []
    for ring in ring_info.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if any(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)
                
    if len(aromatic_rings) < 2:
        return False, "Requires at least 2 aromatic rings"
        
    # Check for presence of phenol or methoxy groups on aromatic rings
    has_phenol_or_methoxy = False
    for ring in aromatic_rings:
        ring_atoms = set(ring)
        for atom_idx in ring:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O':
                    if neighbor.GetTotalNumHs() == 1 or any(n.GetSymbol() == 'C' and n.GetDegree() == 1 for n in neighbor.GetNeighbors()):
                        has_phenol_or_methoxy = True
                        break
                        
    if not has_phenol_or_methoxy:
        return False, "Requires at least one phenol or methoxy group on aromatic ring"
    
    # Check molecular weight range typical for lignans (adjusted range)
    mol_wt = Chem.Descriptors.ExactMolWt(mol)
    if mol_wt < 200 or mol_wt > 1000:  # Increased upper limit
        return False, f"Molecular weight {mol_wt:.1f} outside typical lignan range"
    
    # Count number of oxygen atoms (lignans typically have multiple oxygens)
    oxygen_count = len([atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'O'])
    if oxygen_count < 3:  # Reduced minimum oxygen requirement
        return False, "Insufficient oxygen atoms for typical lignan structure"
    
    # Count carbons to check for potential C6-C3 units
    carbon_count = len([atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'C'])
    if carbon_count < 15:  # Adjusted minimum for basic lignan skeleton
        return False, "Insufficient carbons for lignan skeleton"
    
    # Check for presence of aliphatic carbons connecting aromatic rings
    aliphatic_carbons = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and not atom.GetIsAromatic():
            aromatic_neighbors = sum(1 for n in atom.GetNeighbors() if n.GetIsAromatic())
            if aromatic_neighbors > 0:
                aliphatic_carbons.append(atom.GetIdx())
                
    if len(aliphatic_carbons) < 2:
        return False, "Missing characteristic lignan carbon framework"
        
    return True, "Contains required lignan structural features: phenylpropanoid units and characteristic oxygenation pattern"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25036',
                          'name': 'lignan',
                          'definition': 'Any phenylpropanoid  derived from '
                                        'phenylalanine via dimerization of '
                                        'substituted cinnamic alcohols, known '
                                        'as monolignols, to a dibenzylbutane '
                                        'skeleton. Note that while individual '
                                        'members of the class have names '
                                        'ending ...lignane, ...lignene, '
                                        '...lignadiene, etc., the class names '
                                        'lignan, neolignan, etc., do not end '
                                        'with an "e".',
                          'parents': ['CHEBI:26004']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.2962962962962963 is too low.\n'
               'True positives: '
               "[('COc1cc(OC)c2cc3C(C)OC(C)Cc3c(-c3ccc4cc5CC(C)(O)CC(=O)c5c(O)c4c3O)c2c1', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C[C@H]([C@@](O)(CC2=CC(OC)=C(O)C=C2)C1=O)CC3=CC(OC)=C(O)C=C3', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('COc1ccc(cc1O)[C@H]1OC[C@H]2[C@@H]1CO[C@@H]2c1ccc(OC)c(O)c1', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('[H][C@]12CO[C@H](c3ccc(O)c(OC)c3)[C@@]1([H])CO[C@@H]2c1ccc(O)c(OC)c1', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('[H][C@]12COC(=O)[C@]1([H])Cc1cc(OC)c(O)cc1[C@@H]2c1ccc(O)c(OC)c1', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), ('CC(Cc1ccc(O)c(O)c1)C(C)Cc1ccc(O)c(O)c1', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('COc1cc(ccc1O)[C@@H]1OC[C@H](Cc2cc(OC)c(O)c(OC)c2)[C@H]1C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('COc1cc(ccc1O)[C@H]1OC[C@H]2[C@@H]1CO[C@@H]2c1cc(OC)c(O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)c(OC)c1', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O(CC1C(CC=2C(C1C3=CC(OC)=C(O)C(OC)=C3)=C(OC)C(O)=C(OC)C2)CO)C4OC(C(O)C(O)C4O)CO', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C(C2(OC(=O)C)C(C(OC2)C3=CC(OC)=C(O)C=C3)C1)C4=CC(OC)=C(O)C=C4', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('COc1cc(ccc1O)[C@H](O)[C@H]1CO[C@@H]([C@H]1CO)c1ccc(O)c(OC)c1', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('COc1cc(cc(OC)c1O[C@@H](CO)[C@@H](O)c1ccc(O)cc1)-c1cc(=O)c2c(O)cc(O)cc2o1', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('COC=1C=C(C=C(C1O)OC)C(C2COC(C3=CC(=C(C(=C3)OC)OC(C(C=4C=CC(=C(C4)OC)O)O)CO)OC)C2COC(C5=CC=C(C=C5)O)=O)O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('COc1cc(ccc1O)[C@H](O)[C@H](CO)Oc1c(OC)cc(O)cc1OC', 'Contains "
               'required lignan structural features: phenylpropanoid units, '
               "phenol groups, and characteristic oxygenation pattern'), "
               "('O1C(C(O)C2=CC3=C(C=4C=5C(C(O)=C6C4CC(C)OC6)=C(OC)C=C(C5)OC)C(OC)=CC(=C3C(=C2C1)O)OC)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C(CC2=C(C=3C=4C(C(O)=C5C3CC(C)OC5)=C(OC)C=C(C4)OC)C6=CC(OC)=CC(=C6C(=C2C1)O)OC)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C[C@@H]([C@@H](CC2=C(O)C=CC(O)=C2)C1=O)CC3=CC(O)=CC=C3', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C(C2C(C(OC2)C3=CC(OC)=C(O)C=C3)C1)C4=CC(OC)=C(OC5OC(C(O)C(O)C5O)CO)C=C4', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('COc1cc(cc(OC)c1O)[C@@H]1[C@@H](CO[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@@H](CO)Cc2cc(OC)c(O)c(OC)c12', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('COc1cc(C[C@]2(O)[C@@H](Cc3ccc(OC)c(OC)c3)COC2=O)ccc1O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('C1=C2OCOC2=CC(=C1)[C@]3(OC[C@]4([C@@]3(CO[C@@]4(C5=CC=C(C(=C5)O)O)[H])[H])[H])[H]', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('COc1cc(cc(OC)c1O)[C@H]1[C@@H](CO[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@@H](CO)Cc2cc(OC)c(O)c(OC)c12', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C(C2(O)C(C(OC2)C3=CC(OC)=C(O)C=C3)C1)C4=CC(OC)=C(OC5OC(C(O)C(O)C5O)CO)C=C4', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('COc1cc(ccc1O)[C@@H]1O[C@@H]([C@@H](C)[C@@H]1C)c1ccc(OC)c(OC)c1', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern')]\n"
               'False positives: '
               "[('CC(C)=CCc1ccc(O)c2c1oc1cc(C)c3OC[C@@H]([C@@H](O)c3c1c2=O)C(C)=C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C(O)=CC=2O[C@]3([C@H](O)C[C@@H]4[C@](OC=5C=C(O)C(C=C(C5C4)C)=O)(CC=CC(C[C@H]3CC2C(=C1)C)(C)C)C)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C2=C(O)C=CC3=C2[C@@H](C=4C=5C(=C(O)C=CC5)C(=CC34)O)[C@H](C1)O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('COC(=O)c1c(O)cc2cc3C(=O)c4cc(OC)cc(O)c4C(=O)c3c(O)c2c1C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('OC1=CC=C2C3(OC(C4=C3C=C(C=C4)C(*)=O)=O)C=5C(OC2=C1)=CC(=CC5)O.OC6=CC=C7C8(OC(C9=C8C=CC(=C9)C(*)=O)=O)C=%10C(OC7=C6)=CC(=CC%10)O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C(C2=C(OC=3C(C2=O)=C(O)C=C(O)C3)C4=C1C=C(O)C=C4)C=C(C)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C(C1=C2OC(C=CC2=CC=C1O)(C)C)C3=C(O)C=C(C)C(=C3C=O)OC', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1NC=2C(=O)C3=C(O)C(=C(O)C(=C3C(C2)=O)C(=O)C(=CC4C(O)O[C@@H]([C@@H]([C@@H]([C@@H]([C@H]([C@H](C=CC=C1CO)C)O)C)O)C)[C@H](C)[C@H]4O)C)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C2=C(O)C=3C(=CC(OC)=C(C3C)C(=O)OC)C=C2C(=O)[C@]4([C@]1(O)C(OC)=CC(=O)[C@@H]4OC)O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('P(O[C@H](C(=O)N[C@H]([C@]1(OC(=O)C2=C(C1)C=CC=C2O)[H])CC(C)C)[C@@H](O)[C@@H](N)CC(=O)N)(O)(O)=O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1[C@@H]([C@@H](O)CC2=C1C=C(OC)C=C2OC)C3=CC(OC)=C(O)C=C3', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('OC(=O)CCc1cc2c(-c3cc(ccc3C(O)=O)C(O)=O)c3cc(CCC(O)=O)c(=O)cc3oc2cc1O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1[C@@H]([C@H](O)[C@H](O)[C@@H](O)C1OC2=C(OC=3C(C2=O)=C(O)C=C(O)C3)C4=CC(OC)=C(O)C=C4)CO[C@@]5(O[C@H]([C@H](O)[C@@H](O)[C@H]5O)C)[H]', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('CC(C)=CCc1c(oc2c(c(O)cc(O)c2c1=O)C(C)(C)C=C)-c1ccc(O)cc1O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C2=C(O)C3=C(O)C=C(C)C=C3[C@@H]([C@]24C=C[C@H]1C5=C6O[C@@](C(=O)OC)([C@H]7OC(=O)CC7)CC(C6=C(O)C=C5C4)=O)O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C2=C(C=3C(=O)C=4C=CC=C(C4C3C(=C2)O)O)[C@@H](OC(=O)C(C)C)[C@@H]([C@H]1C)O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C(OC2=C(OC3=C(C2=O)C(OC)=CC(O)=C3)C4=CC(O)=C(O)C=C4)C(O)C(O)C(O)C1', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('N(C=1C=2C(C(=CC1)/N=N/C=3C=4C(C=C(C3)S(=O)(=O)O)=CC(=CC4O)S(=O)(=O)O)=CC=CC2S(=O)(=O)O)C5=CC=CC=C5', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('[Na+].[Na+].[Na+].Oc1ccc(cc1C([O-])=O)C(=C1C=CC(=O)C(=C1)C([O-])=O)c1ccc(O)c(c1)C([O-])=O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC2=C(O)C=C(C=C2)COC(=O)C3=CC(O)=C(O)C=C3)CO', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('C1(C[C@@H](CC=2C1=C(C=3C(=C4[C@@]5(C=CO[C@@]5(OC4=CC3C2O)[H])[H])O)O)O)=O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('COc1cccc2C(=O)c3c(O)c4C[C@](O)(C[C@H](O[C@H]5C[C@H](N)[C@@H](O)[C@H](C)O5)c4c(O)c3C(=O)c12)C(=O)CO', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C(O)=C(O)C=2C=3O[C@@H](C)C(C3C(=C4C2C1=C(OC)C=C4C)O)(C)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C(C=CC=2C1=C(CC(O)C(C)=C)C(O)=C3C2OC=C(C3=O)C4=CC=C(O)C=C4)(C)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('COc1c(C)c(O)c(Cc2c(O)c(C)c(OC)c(C(=O)C(C)C)c2O)c(O)c1C(=O)C(C)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('CC(C)=CCc1c(O)c(O)c(O)c2oc3cc4OC(Cc4c(O)c3c(=O)c12)C(C)=C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C=2C3=C(O)C=C(C)C=C3[C@@H](OC)[C@@H](C2C(=O)C4=C1C=CC(=C4O)[C@@H]5O[C@@H]([C@@H](O)[C@@H](C5)O[C@@H]6O[C@H]([C@@H](O[C@@H]7O[C@@H]([C@@H](O)[C@@H](C7)O)C)CC6)C)C)OC', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C(=O)C([C@H](CC)C2=CC=CC=C2)=C(O)C3=C1C=CC(O)=C3', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('S(OC=1C=C(C=2OC3=C(C(O)=C(C4OC(C(=O)C(O)C4OC5OC(C(O)C(O)C5O)C)C)C(O)=C3)C(=O)C2)C=CC1O)(O)(=O)=O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C2=C(C(=CC(=C2)OC3=CC(O)=CC(=C3)C)C)[C@H]4OCC=5C4=C1C=CC5', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C(CC2=CC3=C(OC(C=C3)(C)C)C=C2)(C(=C(OC)C1=O)C4=CC(O)=C(O)C=C4)C(OC)=O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1[C@@H](O)C2=C(O)C=C3C=4C=CC(=C5C4C(C3=C2[C@@H]6[C@H]1O6)=CC=C5O)O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C(C2C(C=3C1=CC(=CC3O)CCCCC)C=C(CC2)C(O)=O)(C)C', 'Contains "
               'required lignan structural features: phenylpropanoid units, '
               "phenol groups, and characteristic oxygenation pattern'), "
               "('O=C1C2=C(C(O)=CC=C2CC(C1)(O)C)[C@@H]3O[C@@H](OC)C4=C3C=CC=C4OC', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C(C1=C(C(O)=CC=C1CC=C(C)C)C=O)C2=C(O)C(OC[C@H](O)C(O)(C)C)=CC(=C2)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1O[C@](C(=O)OCC)(CC2=CC3=C(OC(C)(C)C(C3)O)C=C2)C(=C1O)C4=CC=C(O)C=C4', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C2=C(O)C(=CC=C2C(=O)C3=C1C=C(OC)C4=C3C(=O)C[C@@](O)(C)C4)[C@@H]5O[C@@H]([C@H]6O[C@@H]7O[C@@H](C)C(C[C@@H]7O[C@@H]6C5)=O)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('OC[C@@H]1O[C@@H](O[C@@H]2[C@H](Oc3cc(O)cc(O)c3C2=O)c2ccc(O)c(O)c2)[C@H](O)[C@H]1O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('OC[C@H]1O[C@H]([C@H](O)[C@@H](O)[C@@H]1O)c1c(O)cc(O)c2c1oc1cc(O)c(O)cc1c2=O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1OC(C2=C(O)C(=CC3=C2C(=O)C=C(N)C3=O)C)=C(C)C=C1C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C(OC=2C(=C3OC(C=CC3=C4OC(=O)C=C(C24)C5=CC=C(O)C=C5)(C)C)C(=O)C(C)C)C(O)C(O)C(O)C1C(O)=O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C(C(O)(C)C)CC2=C1C=C3OC(=O)C(=CC3=C2OC)C4=C(O)C=C(O)C=C4', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('Oc1ccc(cc1)[C@@H]1Oc2cc(O)cc(O)c2C(=O)[C@H]1c1c(O)cc(O)c2c1oc(cc2=O)-c1ccc(O)cc1', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('S(C1=C(NC)C(=O)C=2C=C3C[C@H](CC(=O)O)O[C@@H](C3=C(C2C1=O)O)CCC(C)C)CC(NC(=O)C)C(=O)O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('C1[C@]2([C@]3([C@@](C4=C(C=C(O)C=C4)CC3)(CC[C@@]2([C@@H](O)[C@@H]1O[C@@H]5O[C@@H]([C@H]([C@@H]([C@H]5O)O)O)C(O)=O)C)[H])[H])[H]', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('OC1(C2=C(C(=O)C3=C1C=C(OC)C=C3O)C(O)=CC(=C2)C)CC=C(C)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('ClC1=C(OC)C=C(O)C2=C1[C@](O[C@@H]3O[C@H]([C@H](OC)[C@](C3)(NO)C)C)([C@H]4C[C@@]5(O)[C@H](N(C)C)C(=O)C(=C([C@]5(C(C4=C2O)=O)O)O)C(=O)N)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C2=C3C(O[C@@]45C=6C(=C(O)C=CC6O[C@@]3(O4)[C@@H](C1)O)C(=O)CC5)=CC=C2', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C2=C(OC3=C1C4=C(OC[C@@H]([C@H]4O)C(=C)C)C(=C3)C)C(=CC=C2O)CC(=O)C(C)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1N(O)C=C(C2=CC=C(O[C@H]3OC([C@H](OC)[C@@H](C3O)O)CO)C=C2)C(=C1C4OC(CCC4C)C)O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('C[C@@H]1O[C@@H](Oc2cc(O)c3c(c2)oc(-c2ccc(O)cc2)c(O[C@@H]2O[C@@H](C)[C@H](O)[C@@H](O)[C@H]2O)c3=O)[C@H](O)[C@H](O)[C@H]1O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C(CC(=O)C=2C(O)=C3C(CC(OC3=CC12)=O)C4=CC=CC=C4)C5=CC=C(O)C=C5', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1O[C@H](C2=C(O)C=CC(=C2)O)C=C1CC/C=C(\\\\CO)/CC/C=C(/COC(=O)/C=C\\\\C3=CC=C(O)C=C3)\\\\C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C2=C(C(O)=C(CC=C(C)C)C(O)=C2)C(=O)C=C1C3=CC(CC=C(C)C)=C(O)C=C3', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('N1(CCC2=C(C(CC3=C(C1)C(=C(C=C3)O)OC)=O)C=C4C(=C2)OCO4)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C2=C(C(O)=C(C3=C(O)C=4C(=O)[C@H]5[C@@H](C[C@H](C)O[C@@H]5C)[C@H](C4C=C3OC)O)C(=C2)OC)C(=O)[C@H]6[C@@]1(O)C[C@H](C)O[C@@H]6C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C(OC)C1=C(O)C2=C(OC(C)=C[C@@]2([C@@H]3[C@@]4(OC=5C=C(C)C(=C(C5[C@H]3C=6C(O)=CC(=CC6O4)C)O)C(=O)OC)C)C)C=C1C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('C1(C(=C([C@H]([C@@]2(C[C@@]3(CC4=C(C=C(C(=C4C(C3=C([C@]12O)O)=O)O)NC(C[NH2+]C(C)(C)C)=O)N(C)C)[H])[H])[NH+](C)C)[O-])C(=O)N)=O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C2=C(O[C@@H](C1)C[C@@H](O)C)C=C(O)C=C2CC(=O)OCC(C)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('CC(C)=CCc1c(O)c(CC=C(C)C)c2O[C@@H](CC(=O)c2c1O)c1cc(O)cc(O)c1', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\Cc1c(O)c2C[C@H](O)C(C)(C)Oc2c2c1oc1ccc(O)cc1c2=O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C(OC)=C(OC2=C1C(O)=C(OC)C(=C2C)OC)C3=CC=C(O)C=C3', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C(C2OC3=C(C2O)C=4N(C=5C(C(=O)C4C(O)=C3)=CC=CC5)C)(C1)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C(C1=C2OC(C=CC2=CC=C1OC)(C)C)C3=C(O)C=C(C)C4=C3[C@@H](O)[C@@H](C(=C)C)CO4', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('C1(C=C(CC=2C1=C(C=3C(=C4[C@@]5(C=CO[C@@]5(OC4=CC3C2O)[H])[H])O)O)O)=O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C2=C(OC3=C1C(=CC(=C3)O)C)C=C(O)C=C2CC(=O)C[C@H](O)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C(OCC1=CC(O)=C([C@@](O)(CCCC(C)C)C)C=C1)C2=CC(O)=C([C@@](O)(CCCC(C)C)C)C=C2', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C(C1C(CC(=CC1C=2C(O)=C(OC)C(=CC2O)/C=C/C3=C(O)C=C(O)C=C3)C)C4=C(O)C=C(O)C=C4)C5=C(O)C(=C(O)C=C5)CC=C(C)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1NCC2=C1C=C(O)C3=C2OC(C=C3)(CC/C=C(\\\\CCC(O)C(O)(C)C)/C)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C(OC1=C(C(O)=C(O)C2=C1OC=3C=C(O)C(=CC23)O)C4=CC=C(O)C=C4)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('[H]C1C[C@H](C)OC(=O)C[C@@H](NC(=O)[C@@H](Cc2c(Br)[nH]c3ccccc23)N(C)C(=O)[C@H](C)NC(=O)[C@@H](C)C\\\\C(C)=C\\\\1)c1ccc(O)cc1', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C2=C(C(=O)C(OC)=C1C3=CC=4OCOC4C=C3)C(O)=CC(OCC=C(C)C)=C2OC', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C2=C(C(=O)C=3C1=C(O)C=CC3)C4=C(C(=O)[C@@](O)(C(C)C)CC4=O)C=C2O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C(OC1=C(C(O)=C(C(=O)OC)C(=C1C)C)C)C2=C(O)C(=C(O)C(=C2C)C)C=O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C=2C(C(O)=C(/C(/C3=CC=CC=C3)=C/C(=O)C)C1=O)=CC=CC2', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C(O)=C(C(=O)C(=C1C2=CC=C(OC)C=C2)O)C3=CC=C(O)C=C3', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O(C=1C(C2=C(O)C3=C(C(=O)C2=O)C(O)=CC=C3)=C(C=C(C1)C)C(O)=O)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=CN/C=C/C1=CC(=C(O)C=C1)C2=C(O)C=CC(=C2)/C=C/NC=O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1OC2=C(C(=CC(=C2C)O)C)OC3=C1C(=CC(=C3CC4=C(OC)C=C(O)C=C4C)O)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('C1(=C(CC=C(C)C)C(=C(C(=O)/C=C/C2=CC=C(C=C2)O)C(=C1)O)O)OC', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C2=C(C(=O)C=3C1=C(O)C4=C([C@@H](C(=O)OC)[C@@](O)(CC)C[C@@H]4OC5OC(C(OC6OC(C7OC8OC(C)C(CC8OC7C6)=O)C)CC5)C)C3)C(O)=CC=C2O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1N[C@H](C(=O)N[C@H](C(=O)NC(C(=O)N[C@H](C(=O)O)CO)CCCN=C(N)N)[C@H](O)C2=C(O)C=CC(C3=CC(C[C@@H]1N)=C(O)C=C3)=C2)C[C@@H](O)CN', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C(C(O)CC2=C1C=C(O)C=3OC4=C(C(=O)C23)C(O)=C(C(O)=C4)CC=C(C)C)(C)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C(OC2=C(O)C(=[N+]([O-])C=C2)C3=[N+]([O-])C=CC(=C3O)OC4OC(C(O)C(C4O)O)CO)C(O)C(O)C(C1CO)O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C2=C(OC3=C1C4=C(OC[C@H]([C@H]4O)C(=C)C)C(=C3)C)C(=CC=C2O)[C@@H](O)[C@@H](O)C(O)(C)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1OC(=CC(=C1C2=C(C=C(O)C(=C2)O)C=CC=3OC(=O)C=C(C3)O)O)C=CC4=CC(O)=C(O)C=C4', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('C1OC(C2COC(C12)C3=CC(=C(C(=C3)OC)O)OC)C4=CC=C(C(=C4)OC)OC(C(C=5C=C(C(=CC5)O)OC)O)CO', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C2=C(C(=O)C=3C1=C(O)C=CC3)C=4C(=O)C[C@@H](C)CC4C=C2O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C(C=2C(OC)=CC(O)=C(O)C2)=C(OC)C(=O)C3=C1C=C(O)C(OC)=C3O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1OC(=CC=2C1=C(O)C(=C(O)C2)C(=O)C3=C(O)C=C(OC)C=C3C(=O)OC)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), ('O=C(OC1=CC(O)=CC(=C1)CCC)C2=C(O)C=C(OC)C=C2CCC', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('[H][C@@]12Cc3ccc(OC)c(OC)c3CN1CCc1cc(OC)c(O)cc21', 'Contains "
               'required lignan structural features: phenylpropanoid units, '
               "phenol groups, and characteristic oxygenation pattern'), "
               "('O1[C@@H](OC2=C(O)C(=C(O)C=C2C3=CC=C(OC)C=C3)C4=CC=C(OC)C=C4)[C@H](O)[C@@H](O)[C@@H]([C@H]1CO)O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1C2=C(C(=O)C=3C1=C(O)C4=C([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](C5)N(C)C)C)C[C@]([C@@H]4O)(O)CC)C3)C(O)=CC=C2O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O=C1NC=C(C2=CC=C(O)C=C2)C(=C1C(=O)[C@@H]3C=C([C@H]4CC[C@@H](C[C@@H]4[C@H]3/C=C/CO)C)C)O', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('COC1=CC(=CC(=C1O)OC)C=C2C(=O)NC(=O)N(C2=O)C3=CC=CC=C3', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('ClC1=C2OC=3N(C(Cl)=CC3C(C2=C(O)C(=C1)C)=O)[C@@H]4C=C([C@@H](OC)[C@@H]([C@H]4O)O)CO', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O(C=1C=C(C(C(C)C)(CCCN(CCC2=CC(OC)=C(OC)C=C2)C)C#N)C=CC1O)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O[C@@H]2OC[C@@H](O)[C@H](O)[C@H]2O)[C@@H]1OC3=C(OC=4C(C3=O)=C(O)C=C(O)C4)C5=CC=C(O)C=C5)CO[C@@H]6O[C@H]([C@H](O)[C@@H](O)[C@H]6O)C', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern'), "
               "('O1C(C(O)C(C=2C=3OC(C(O)CC3C(O)=CC2O)C4=CC(O)=C(O)C=C4)C=5C1=CC(O)=CC5O)C6=CC=C(O)C=C6', "
               "'Contains required lignan structural features: phenylpropanoid "
               'units, phenol groups, and characteristic oxygenation '
               "pattern')]\n"
               'False negatives: '
               "[('O1[C@@H](OC2=C(OC)C=C([C@H]3OC[C@@H]4[C@@H]3CO[C@H]4C5=CC(OC)=C(O[C@@H]6O[C@@H]([C@@H](O)[C@@H]([C@H]6O)O)CO)C(=C5)OC)C=C2OC)[C@H](O)[C@@H](O)[C@@H]([C@H]1CO)O', "
               "'Requires at least one phenol group'), "
               "('C1OC(C2COC(C12)C3=CC(=C(C(=C3)OC)O)OC)C4=CC(=C(C(=C4)OC)OC(C(C=5C=C(C(=C(C5)OC)OC(C(C=6C=C(C(=CC6)O)OC)O)CO)OC)O)CO)OC', "
               "'Molecular weight 840.3 outside typical lignan range'), "
               "('COc1cc(cc(OC)c1OC(C)=O)C1OCC2C1COC2c1cc(OC)c(OC(C)=O)c(OC)c1', "
               "'Requires at least one phenol group'), "
               "('O(C=1C=C(C[C@@H]([C@@H](CC2=CC(OC)=C(OC)C=C2)C)C)C=CC1OC)C', "
               "'Requires at least one phenol group'), "
               "('COc1cc(cc2OCOc12)[C@@H]1O[C@H]([C@H](C)[C@H]1C)c1cc(OC)c2OCOc2c1', "
               "'Requires at least one phenol group'), "
               "('O(CC(C(COC1OC(C(O)C(O)C1O)CO)CC2=CC(OC)=C(O)C=C2)CC3=CC(OC)=C(O)C=C3)C4OC(C(O)C(O)C4O)COC(=O)CC(O)(CC(O)=O)C', "
               "'Molecular weight 830.3 outside typical lignan range'), "
               "('O1CC2=C(C=3C(C(OC)=C2C1=O)=CC=4OCOC4C3)C5=CC=6OCOC6C=C5', "
               "'Requires at least one phenol group'), "
               "('COc1ccc(cc1OC)[C@H]1O[C@H]([C@H](C)[C@@H]1C)c1ccc2OCOc2c1', "
               "'Requires at least one phenol group'), "
               "('COC[C@H]1O[C@@H](O[C@@H]2CO[C@@H](O[C@@H]3[C@@H](CO)O[C@@H](Oc4c5COC(=O)c5c(-c5ccc6OCOc6c5)c5cc(OC)c(OC)cc45)[C@H](O)[C@H]3O)[C@H](OC)[C@H]2OC)[C@H](OC)[C@H]1OC', "
               "'Requires at least one phenol group'), "
               "('Oc1ccc(CC(=C)C(=C)Cc2ccc(O)cc2)cc1', 'Insufficient oxygen "
               "atoms for typical lignan structure'), "
               "('O[C@@H]([C@H]1COC(=O)[C@@H]1C(=O)c1ccc2OCOc2c1)c1ccc2OCOc2c1', "
               "'Requires at least one phenol group'), "
               "('C[C@@H]1[C@@H](C)[C@@H](O[C@H]1c1ccc2OCOc2c1)c1ccc2OCOc2c1', "
               "'Requires at least one phenol group'), "
               "('COc1ccc(C[C@H]2COC(=O)[C@]2(O)Cc2ccc(O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)c(OC)c2)cc1OC', "
               "'Requires at least one phenol group'), "
               "('COc1cc(cc(OC)c1OC)[C@H]1[C@@H]2[C@H](COC2=O)Cc2c1cc1OCOc1c2OC', "
               "'Requires at least one phenol group')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 33,
    'num_false_positives': 100,
    'num_true_negatives': 998,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.24812030075187969,
    'recall': 0.868421052631579,
    'f1': 0.38596491228070173,
    'accuracy': 0.9075704225352113}