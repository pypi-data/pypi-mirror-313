"""
Classifies: CHEBI:24697 hydroxyflavanone
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroxyflavanone(smiles: str):
    """
    Determines if a molecule is a hydroxyflavanone (flavanone with one or more hydroxy substituents).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydroxyflavanone, False otherwise 
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Flavanone core structure pattern
    # Chroman-4-one fused with phenyl at position 2
    flavanone_pattern = Chem.MolFromSmarts('[#6]1-[#6]-[#6](=O)-c2c(O1)cccc2')
    
    # Check for flavanone core
    if not mol.HasSubstructMatch(flavanone_pattern):
        return False, "Does not contain flavanone core structure"
    
    # Check for hydroxy groups
    hydroxy_pattern = Chem.MolFromSmarts('[OH]')
    hydroxy_matches = mol.GetSubstructMatches(hydroxy_pattern)
    
    if not hydroxy_matches:
        return False, "No hydroxy substituents found"

    # Get core atoms
    core_match = mol.GetSubstructMatch(flavanone_pattern)
    core_atoms = set(core_match)

    # Count hydroxy groups attached to core structure
    core_hydroxy_count = 0
    for match in hydroxy_matches:
        oh_atom = mol.GetAtomWithIdx(match[0])
        for neighbor in oh_atom.GetNeighbors():
            if neighbor.GetIdx() in core_atoms or any(n.GetIdx() in core_atoms for n in neighbor.GetNeighbors()):
                core_hydroxy_count += 1
                break
    
    if core_hydroxy_count == 0:
        return False, "No hydroxy groups attached to flavanone core"
        
    return True, f"Hydroxyflavanone with {core_hydroxy_count} hydroxy group(s) attached to core"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24697',
                          'name': 'hydroxyflavanone',
                          'definition': 'A member of the class of flavanones '
                                        'that consists of flavanone with one '
                                        'or more hydroxy substituents.',
                          'parents': ['CHEBI:28863', 'CHEBI:33822']},
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
               'False positives: '
               "[('ClC1=C(O)C2=C(OC3C=C(O)C=C(C3C2=O)C(=O)OC)C=C1C', "
               "'Hydroxyflavanone with 2 hydroxy group(s)'), "
               "('O=C1C2=C(OC3C1C(C(=O)OC)=CC(O)=C3)C=C(C)C=C2OC', "
               "'Hydroxyflavanone with 1 hydroxy group(s)'), "
               "('ClC1=C2OC3C=C(O)C=C(C3C(C2=C(O)C=C1C)=O)C(=O)O', "
               "'Hydroxyflavanone with 3 hydroxy group(s)'), "
               "('ClC1=C2OC3C=C(O)C=C(C3C(C2=C(OC)C=C1C)=O)C(=O)OC', "
               "'Hydroxyflavanone with 1 hydroxy group(s)'), "
               "('ClC1=C2OC3C=C(O)C=C(C3C(C2=C(O)C=C1C)=O)C(=O)OC', "
               "'Hydroxyflavanone with 2 hydroxy group(s)'), "
               "('ClC1=C2OC3C=C(O)C=C(C3C(C2=C(O)C(=C1C)Cl)=O)C(=O)O', "
               "'Hydroxyflavanone with 3 hydroxy group(s)')]\n"
               'False negatives: '
               "[('O1C2=C(C(C[C@]1(C3=CC=CC=C3)O)=O)C(=CC(=C2)O)O', 'Does not "
               "contain flavanone core structure'), "
               "('CC(C)=CCCC1(C)Oc2c(O)ccc([C@@H]3CC(=O)c4c(O3)cc(O)c(CC=C(C)C)c4O)c2C=C1', "
               "'Does not contain flavanone core structure'), "
               "('CC(C)=CCc1cc2C(=O)C[C@H](Oc2c(CC=C(C)C)c1O)c1ccc2OC(C)(C)C=Cc2c1', "
               "'Does not contain flavanone core structure'), "
               "('OC[C@H]1O[C@@H](Oc2ccc3C(=O)C[C@H](Oc3c2)c2ccc(O)c(O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)c2)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Does not contain flavanone core structure'), "
               "('O[C@@H]1CO[C@H](O[C@H]2[C@H](Oc3cc(O)cc(O)c3C2=O)c2ccc(O)c(O)c2)[C@@H](O)[C@@H]1O', "
               "'Does not contain flavanone core structure'), "
               "('CC(C)=CCOc1ccc(cc1)[C@@H]1CC(=O)c2c(O)cc(O)cc2O1', 'Does not "
               "contain flavanone core structure'), "
               "('Oc1ccc(cc1)[C@@H]1CC(=O)c2c(O)cc(O)cc2O1', 'Does not contain "
               "flavanone core structure'), "
               "('OC(=O)CCC\\\\C=C\\\\C(c1ccccc1)c1c(O)cc2OC(CC(=O)c2c1O)c1ccccc1', "
               "'Does not contain flavanone core structure'), "
               "('OC(=O)CCCC(\\\\C=C\\\\c1ccccc1)c1c(O)cc2OC(CC(=O)c2c1O)c1ccccc1', "
               "'Does not contain flavanone core structure'), "
               "('Oc1ccc2C(=O)CC(Oc2c1O)c1ccccc1', 'Does not contain flavanone "
               "core structure'), ('Oc1cc(O)cc(c1)C1CC(=O)c2c(O)cc(O)cc2O1', "
               "'Does not contain flavanone core structure'), "
               "('COc1ccc(O)c(c1)[C@@H]1CC(=O)c2c(O)c(C)c(O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)c(C)c2O1', "
               "'Does not contain flavanone core structure'), "
               "('O[C@@H]1CO[C@@H](O[C@H]2[C@@H](Oc3cc(O)cc(O)c3C2=O)c2ccc(O)c(O)c2)[C@H](O)[C@H]1O', "
               "'Does not contain flavanone core structure'), "
               "('O1C2=C(C(C(C1(C3=C(C(=C(C(=C3*)*)*)*)*)O)*)=O)C(=C(C(=C2*)*)*)*', "
               "'Does not contain flavanone core structure'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\Cc1c(O)c(O)ccc1[C@@H]1CC(=O)c2c(O1)cc1OC(C)(C)C(O)Cc1c2O', "
               "'Does not contain flavanone core structure'), "
               "('O[C@@H]1[C@@H](Oc2cc(O)cc(O)c2C1=O)c1ccc(O)c(O)c1', 'Does "
               "not contain flavanone core structure'), "
               "('Oc1cccc(c1)[C@@H]1CC(=O)c2ccccc2O1', 'Does not contain "
               "flavanone core structure'), "
               "('O[C@@H]1[C@H](Oc2c([C@H]3[C@@H](Oc4cc(O)cc(O)c4C3=O)c3ccc(O)c(O)c3)c(O)cc(O)c2C1=O)c1ccc(O)c(O)c1', "
               "'Does not contain flavanone core structure'), "
               "('COc1ccc(cc1O)-c1cc(=O)c2c(O)cc(O[C@@H]3O[C@H](CO[C@@H]4O[C@@H](C)[C@H](O)[C@@H](O)[C@H]4O)[C@@H](O)[C@H](O)[C@H]3O)cc2o1', "
               "'Does not contain flavanone core structure'), "
               "('CC(C)=CCc1c(O)c2OC(C)(C)C=Cc2cc1[C@@H]1CC(=O)c2c(O)cc(O)c(CC=C(C)C)c2O1', "
               "'Does not contain flavanone core structure'), "
               "('COc1cc(ccc1O)[C@@H]1CC(=O)c2c(O)cc(O)cc2O1', 'Does not "
               "contain flavanone core structure'), "
               "('O[C@@H]1CO[C@H](O[C@@H]2[C@H](Oc3cc(O)cc(O)c3C2=O)c2ccc(O)c(O)c2)[C@@H](O)[C@@H]1O', "
               "'Does not contain flavanone core structure')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 19,
    'num_false_positives': 100,
    'num_true_negatives': 23553,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.15966386554621848,
    'recall': 0.8636363636363636,
    'f1': 0.2695035460992908,
    'accuracy': 0.995649419218585}