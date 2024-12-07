"""
Classifies: CHEBI:24698 hydroxyflavone
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroxyflavone(smiles: str):
    """
    Determines if a molecule is a hydroxyflavone (flavone with one or more hydroxy groups).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydroxyflavone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for flavone core
    # More comprehensive pattern that matches the basic flavone skeleton
    flavone_pattern = Chem.MolFromSmarts('c1c(c2occ(=O)cc2)cccc1')
    
    # Alternative patterns to catch different representations
    alt_pattern1 = Chem.MolFromSmarts('O=C1C=C(Oc2[c]cccc2)c2ccccc12')
    alt_pattern2 = Chem.MolFromSmarts('c1cc2oc(-[c]3ccccc3)c(=O)cc2cc1')
    alt_pattern3 = Chem.MolFromSmarts('c1c2c(=O)cc(oc2ccc1)-[c]1ccccc1')
    
    # Check if any of the flavone patterns match
    is_flavone = any([
        mol.HasSubstructMatch(p) for p in [flavone_pattern, alt_pattern1, alt_pattern2, alt_pattern3]
        if p is not None
    ])
    
    if not is_flavone:
        return False, "No flavone core structure found"
    
    # Check for hydroxyl groups
    hydroxy_pattern = Chem.MolFromSmarts('[OH]')
    if not mol.HasSubstructMatch(hydroxy_pattern):
        return False, "No hydroxyl groups found"

    # Count hydroxyl groups
    num_hydroxy = len(mol.GetSubstructMatches(hydroxy_pattern))
    
    # Get ring systems
    ring_info = mol.GetRingInfo()
    ring_atoms = set()
    for ring in ring_info.AtomRings():
        ring_atoms.update(ring)
    
    # Check if any hydroxyl group is attached to a ring atom
    hydroxy_matches = mol.GetSubstructMatches(hydroxy_pattern)
    ring_hydroxy = False
    
    for match in hydroxy_matches:
        oxygen = match[0]
        for neighbor in mol.GetAtomWithIdx(oxygen).GetNeighbors():
            if neighbor.GetIdx() in ring_atoms:
                ring_hydroxy = True
                break
        if ring_hydroxy:
            break
    
    if ring_hydroxy:
        return True, f"Hydroxyflavone with {num_hydroxy} hydroxyl group(s)"
    else:
        return False, "No hydroxyl groups attached to ring system"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24698',
                          'name': 'hydroxyflavone',
                          'definition': 'Any flavone in which one or more ring '
                                        'hydrogens are replaced by hydroxy '
                                        'groups.',
                          'parents': ['CHEBI:24043', 'CHEBI:33822']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'True positives: []\n'
               'False positives: []\n'
               'False negatives: '
               "[('C=1(C(=C(C(=C2C1OC(=CC2=O)C3=CC=C(C(=C3)OC)O)O)[C@@H]4OC[C@@H]([C@@H]([C@H]4O)O)O)O)[C@H]5OC[C@@H]([C@@H]([C@H]5O)O)O', "
               "'No flavone core structure found'), "
               "('O[C@H]1[C@H](Oc2cc(O)cc3oc(-c4cc(O)c(O)c(O)c4)c(O)c(=O)c23)O[C@@H]([C@@H](O)[C@@H]1O)C(O)=O', "
               "'No flavone core structure found'), "
               "('COc1cc2oc(cc(=O)c2c(O)c1OC)-c1ccc(O)c(O)c1', 'No flavone "
               "core structure found'), "
               "('COc1ccc(cc1OC)-c1cc(=O)c2c(O)c(OC)c(O)cc2o1', 'No flavone "
               "core structure found'), "
               "('COc1cc2oc(-c3ccc(O)cc3O)c(CC=C(C)C)c(=O)c2c(O)c1\\\\C=C\\\\C(C)C', "
               "'No flavone core structure found'), "
               "('Oc1ccc2c(c1)oc(-c1cc(O)c(O)c(O)c1)c(O)c2=O', 'No flavone "
               "core structure found'), "
               "('[H][C@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)c1c(O)c(O)c2oc(cc(=O)c2c1O)-c1ccc(O)cc1', "
               "'No flavone core structure found'), "
               "('OC[C@H]1O[C@H]([C@H](O)[C@@H](O)[C@@H]1O)c1c(O)cc2oc(cc(=O)c2c1O)-c1ccc(O)cc1', "
               "'No flavone core structure found'), "
               "('COc1cc(\\\\C=C\\\\C(=O)OC[C@H]2O[C@@H](O[C@@H]3[C@@H](O)[C@H](O)[C@@H](CO)O[C@H]3c3c(O)cc4oc(cc(=O)c4c3O)-c3ccc(O)cc3)[C@H](O)[C@@H](O)[C@H]2O)cc(OC)c1O', "
               "'No flavone core structure found'), "
               "('COc1cc2oc(cc(=O)c2c(OC)c1O)-c1ccc(O)cc1', 'No flavone core "
               "structure found'), "
               "('[C@H]1(O[C@H]([C@@H]([C@H]([C@H]1O)O)O)C)O[C@H]2[C@@H](O[C@@H]([C@H]([C@@H]2O)O)CO)OC3=CC4=C(C(C=C(O4)C5=CC(=C(C(=C5)OC)O)OC)=O)C(=C3)O', "
               "'No flavone core structure found'), "
               "('O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC2=C(OC=3C(C2=O)=C(O)C=C(O)C3)C4=CC=C(O)C=C4)CO[C@@]5(O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)CO)[H]', "
               "'No flavone core structure found'), "
               "('CC(C)=CCc1c(O)c(CC=C(C)C)c2oc(-c3ccc(C[C@H](O)C(C)=C)c(O)c3)c(O)c(=O)c2c1O', "
               "'No flavone core structure found'), "
               "('COc1cc(\\\\C=C\\\\C(=O)OC[C@H]2OC(Oc3cc(O)c4c(c3)oc(cc4=O)-c3cc(OC)c(O)c(OC)c3)[C@H](O)[C@@H](O)[C@@H]2O)cc(OC)c1O', "
               "'No flavone core structure found'), "
               "('O[C@H]1[C@H](Oc2c(oc3cc(O)cc(O)c3c2=O)-c2cc(O)c(O)c(O)c2)O[C@@H]([C@@H](O)[C@@H]1O)C(O)=O', "
               "'No flavone core structure found'), "
               "('COc1cc(cc(O)c1OC)-c1oc2cc(O)cc(O)c2c(=O)c1OC', 'No flavone "
               "core structure found'), "
               "('COc1cc(O)c2c(c1)oc(-c1cc(O)c(OC)cc1O)c(OC)c2=O', 'No flavone "
               "core structure found'), "
               "('COC1=CC(O)=C2C(=O)C=C(OC2=C1)C1=CC(OC)=C(O)C=C1', 'No "
               "flavone core structure found'), "
               "('COc1cc(c(O)cc1O)-c1cc(=O)c2c(O)c(OC)c(OC)cc2o1', 'No flavone "
               "core structure found'), "
               "('COc1cc(ccc1O)-c1cc(=O)c2c(O)cc(O[C@@H]3O[C@H](CO[C@@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@H]4O)[C@@H](O)[C@H](O)[C@H]3O)cc2o1', "
               "'No flavone core structure found'), "
               "('COc1c(O)cc(O)c2c1oc(-c1ccc(O)c(O)c1)c(O)c2=O', 'No flavone "
               "core structure found'), "
               "('C=1(C(=C(C(=C2C1OC(=C(C2=O)*)C3=C(C(=C(C(=C3*)*)*)*)*)*)*)*)O', "
               "'No flavone core structure found'), "
               "('COc1cc(O)c2c(c1)oc(cc2=O)-c1ccc(O)cc1', 'No flavone core "
               "structure found'), "
               "('C[C@H]1Oc2cc(O)c3c(oc(-c4ccc(O)cc4O)c(CC=C(C)C)c3=O)c2C1(C)C', "
               "'No flavone core structure found'), "
               "('OC[C@H]1O[C@@H](Oc2ccc(cc2O)-c2cc(=O)c3c(O)cc(O)cc3o2)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'No flavone core structure found'), "
               "('COc1cc(ccc1O)-c1cc(=O)c2c(O)c([C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O[C@@H]3OC[C@H](O)[C@H](O)[C@H]3O)c(O)cc2o1', "
               "'No flavone core structure found'), "
               "('Oc1ccc(cc1)-c1cc(=O)c2ccc(O)cc2o1', 'No flavone core "
               "structure found'), "
               "('O1C(C2=CC(=CC=C2)C(=O)C3=CC=CC=C3)=C(O)C(=O)C=4C1=CC(O)=CC4O', "
               "'No flavone core structure found'), "
               "('OC[C@H]1O[C@@H](O[C@H]2[C@@H](O[C@H](CO)[C@@H](O)[C@@H]2O)Oc2c(oc3cc(O)cc(O)c3c2=O)-c2ccc(O)cc2)[C@H](O[C@@H]2O[C@H](COC(=O)\\\\C=C\\\\c3ccc(O)cc3)[C@@H](O)[C@H](O)[C@H]2O)[C@@H](O)[C@@H]1O', "
               "'No flavone core structure found'), "
               "('CC(C)=CCc1c(oc2c3C=CC(C)(C)Oc3cc(O)c2c1=O)-c1ccc(O)cc1O', "
               "'No flavone core structure found'), "
               "('COc1cc(O)c2c(c1)oc(-c1cc(O)c(OC)c(OC)c1)c(OC)c2=O', 'No "
               "flavone core structure found'), "
               "('COc1cc(O)c2c(c1)oc(-c1ccc(O)c(O)c1)c(O)c2=O', 'No flavone "
               "core structure found'), "
               "('COc1cc(ccc1O)-c1cc(=O)c2c(O)c(OC)c(O)cc2o1', 'No flavone "
               "core structure found'), "
               "('C1=2C(OC(=CC1=O)C3=CC(=C(C=C3)O)O)=CC(=C(C2O)[C@H]4[C@@H]([C@H]([C@H](CO4)O)O)O[C@H]5[C@@H]([C@H]([C@@H]([C@@H](CO)O5)O)O)O)O', "
               "'No flavone core structure found'), "
               "('C[C@@H]1O[C@@H](Oc2cc(O)c3c(c2)oc(-c2ccc(O)cc2)c(O[C@@H]2O[C@@H](C)[C@H](O)[C@@H](O)[C@H]2O)c3=O)[C@H](O)[C@H](O)[C@H]1O', "
               "'No flavone core structure found'), "
               "('COc1ccc(c(C\\\\C=C(/C)CCC=C(C)C)c1O)-c1oc2cc(O)cc(O)c2c(=O)c1O', "
               "'No flavone core structure found'), "
               "('COC=1C=C(C=C(C1O)OC)C2=CC(C3=C(C=C(C=C3O2)O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O)O)O)O)=O', "
               "'No flavone core structure found'), "
               "('C1=C(C=C(C2=C1OC(=C(C2=O)O[C@H]3[C@@H]([C@@H]([C@H]([C@@H](O3)C)O)O)O)C4=CC=C(C(=C4)O)O)O)O[C@H]5[C@@H]([C@@H]([C@H]([C@@H](O5)C)O)O)O', "
               "'No flavone core structure found'), "
               "('C1=C(C=C(C2=C1OC(=C(C2=O)OC)C3=CC(=C(C(=C3)OC)O)OC)O)O', 'No "
               "flavone core structure found'), "
               "('O[C@H]1[C@@H](COC(=O)c2ccc(O)cc2)O[C@@H](Oc2c(oc3cc(O)cc(O)c3c2=O)-c2ccc(O)c(O)c2)[C@H](O)[C@H]1O', "
               "'No flavone core structure found'), "
               "('Oc1ccc(cc1)-c1cc(=O)c2c(O)c(Oc3ccc(cc3)-c3cc(=O)c4c(O)cc(O)cc4o3)c(O)cc2o1', "
               "'No flavone core structure found'), "
               "('OC[C@H]1O[C@H](Oc2cc(cc(O)c2O)-c2oc3cc(O)cc(O)c3c(=O)c2O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'No flavone core structure found'), "
               "('COc1cc(\\\\C=C\\\\C(=O)OCC2OC(Oc3cc4oc(cc(=O)c4c(O)c3[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)-c3ccc(O)cc3)[C@H](O)[C@@H](O)[C@@H]2O)ccc1O', "
               "'No flavone core structure found'), "
               "('Oc1ccc(cc1OS(O)(=O)=O)-c1oc2cc(OS(O)(=O)=O)cc(O)c2c(=O)c1OS(O)(=O)=O', "
               "'No flavone core structure found')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 44,
    'num_false_positives': 100,
    'num_true_negatives': 12910,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.3055555555555556,
    'recall': 1.0,
    'f1': 0.46808510638297873,
    'accuracy': 0.9923395127930137}