"""
Classifies: CHEBI:192499 anthoxanthin
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_anthoxanthin(smiles: str):
    """
    Determines if a molecule is an anthoxanthin (flavonoid pigment).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an anthoxanthin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Basic flavonoid core structure patterns
    flavonoid_core = [
        'O=C1CC(c2ccccc2)Oc2ccccc21',  # flavone
        'O=C1C(O)=C(c2ccccc2)Oc2ccccc21',  # flavonol
        'O=C1CC(Oc2ccccc2)c2ccccc21',  # isoflavone
        'O=C1C=C(c2ccccc2)Oc2ccccc21'  # basic chromone
    ]
    
    # Convert SMARTS patterns to RDKit molecules
    patterns = [Chem.MolFromSmarts(pattern) for pattern in flavonoid_core]
    
    # Check for basic flavonoid structure
    has_flavonoid_core = False
    for pattern in patterns:
        if pattern is not None and mol.HasSubstructMatch(pattern):
            has_flavonoid_core = True
            break
            
    if not has_flavonoid_core:
        return True, "Not a flavonoid structure"

    # Count hydroxyl groups
    oh_pattern = Chem.MolFromSmarts('[OH]')
    num_oh = len(mol.GetSubstructMatches(oh_pattern))

    # Count methoxy groups
    ome_pattern = Chem.MolFromSmarts('OC')
    num_ome = len(mol.GetSubstructMatches(ome_pattern))

    # Count carbonyls
    carbonyl_pattern = Chem.MolFromSmarts('C(=O)')
    num_carbonyls = len(mol.GetSubstructMatches(carbonyl_pattern))

    # Check for glycosylation
    glycoside_pattern = Chem.MolFromSmarts('[OH]C1OC(CO)C(O)C(O)C1O')
    is_glycosylated = mol.HasSubstructMatch(glycoside_pattern)

    # Check for aromatic rings
    ring_info = mol.GetRingInfo()
    aromatic_rings = sum(1 for ring in ring_info.AtomRings() 
                        if all(mol.GetAtomWithIdx(i).GetIsAromatic() for i in ring))

    # Specific criteria for anthoxanthin
    if (aromatic_rings >= 2 and 
        num_carbonyls >= 1 and 
        (num_oh + num_ome) >= 1):
        
        if is_glycosylated:
            return False, "Glycosylated anthoxanthin"
        elif num_oh >= 2:
            return False, "Anthoxanthin with multiple hydroxyl groups"
        elif num_ome >= 1:
            return False, "Anthoxanthin with methoxy substitution"
        else:
            return False, "Basic anthoxanthin structure"
    
    return True, "Not an anthoxanthin structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:192499',
                          'name': 'anthoxanthin',
                          'definition': 'are a type of flavonoid pigments in '
                                        'plants. Anthoxanthins are '
                                        'water-soluble pigments which range in '
                                        'color from white or colorless to a '
                                        'creamy to yellow, often on petals of '
                                        'flowers.',
                          'parents': ['CHEBI:47916']},
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
               "[('O1C2(C3C(C(C3C4=C1C=C(O)C(=C4)C5OC=6C(C(=O)C5)=C(O)C=C(O)C6)(C)C)CC2)C', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('COc1ccc(cc1)[C@@H]1CC(=O)c2c(O)c(C)c(O)c(C)c2O1', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('Oc1ccccc1Cc1ccc(O)c(Cc2ccc(O)c(Cc3c(O)c(Cc4cc(Cc5ccccc5O)ccc4O)c4O[C@@H](CC(=O)c4c3O)c3ccccc3)c2)c1', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(CC(=O)C2=C1C=CC(O)=C2O)C3=CC=C(OC)C=C3', 'Anthoxanthin "
               "with mixed hydroxyl/methoxy substitution'), "
               "('O1C(CC2=C3OC(CC(=O)C3=C(OC)C=C12)C4=CC=CC=C4)C(C)=C', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('C12=C(C(CC(C3=CC=C(O)C=C3)(O1)O)=O)C=CC(=C2)O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('COc1cc(O)c(C[C@@H](CC=C(C)C)C(C)=C)c2O[C@@H](CC(=O)c12)c1ccc(O)cc1O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(CC(=O)C=2C1=CC(OC(=O)C3=CC=CC=C3)=CC2O)C4=CC=CC=C4', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('O1C(CC(=O)C2=C1C(OC)=C(O)C=C2O)C3=CC(O)=C(O)C=C3', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('OC(=O)CCC[C@@H](\\\\C=C\\\\c1ccccc1)c1c(O)cc2O[C@H](CC(=O)c2c1O)c1ccccc1', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O([C@H]1C(O)[C@@H](O)C(O[C@H]1OC2=CC=C(C3OC4=C(C(=O)C3)C(O)=C(C=C4)CC=C(C)C)C=C2)C)[C@@H]5OC[C@@H](O)[C@H](O)C5O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C([C@@H](O)[C@H](O)C(O)[C@@H]1OC=2C=C(C3OC=4C(C(=O)C3)=C(O)C=C(OC)C4)C=CC2OC)CO', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(CC(=O)C2=C1C(CC=C(C)C)=C(O)C=C2)C3=CC=CC=C3', 'Basic "
               "anthoxanthin structure'), "
               "('O1C(C1CC=2C=C(C3OC=4C(C(=O)C3)=C(O)C=C(O)C4CC=C(C)C)C=CC2O)(C)C', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('C1C(OC2=CC(=CC(=C2C1=O)O)O)C3=CC(=C(C=C3)O)O', 'Anthoxanthin "
               "with multiple hydroxyl groups'), "
               "('O1C(C(CC2=C1C=C(O)C3=C2OC(CC3=O)C4=C(O)C=CC=C4O)CC=C(C)C)(C)C', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('CC(=C)C(O)CC\\\\C(C)=C\\\\Cc1c(O)cc2O[C@@H](CC(=O)c2c1O)c1ccc(O)c(O)c1', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('CC(C)=CCc1c(O)cc(O)c2C(=O)C[C@H](Oc12)c1ccc(O)cc1', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1[C@@H](CC(=O)C2=C1C(O)=C(O)C=C2O)C3=CC(CC=C(C)C)=C(O)C=C3', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('Oc1cc(O)c2C(=O)C[C@H](Oc2c1)c1ccc(O)c(O)c1', 'Anthoxanthin "
               "with multiple hydroxyl groups'), "
               "('Cc1c(O)c(C)c2O[C@@H](CC(=O)c2c1O)c1cc(O)ccc1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(CC(=O)C2=C1C(OC)=C(OC)C=C2O)C=3C(OC)=CC=CC3O', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('CC1[C@@H]([C@@H](C([C@@H](O1)OCC2[C@H]([C@H](C([C@@H](O2)OC3=CC(=C4C(=O)C[C@H](OC4=C3)C5=CC(=C(C=C5)OC)O)O)O)O)O)O)O)O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC2=CC=3O[C@@H](CC(=O)C3C=C2)C4=CC=C(O[C@@H]5O[C@@H]([C@@H](O)[C@H](O)[C@H]5O)CO)C=C4)CO', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O=C1C2=C(O)C(=C(OC)C=C2O[C@@H](C1)C3=C(O)C=C(O)C=C3)C[C@@H](C(=C)C)CC=C(C)C', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(CC(=O)C2=C1C=C(O)C=C2)C3=CC=C(O)C=C3', 'Anthoxanthin "
               "with mixed hydroxyl/methoxy substitution'), "
               "('O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC2=CC=C(C3OC=4C(C(=O)C3)=C(O)C=C(O)C4)C=C2)CO', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O=C1C2=C(O)C(=C(O)C=C2O[C@H](C1)C3=CC=C(O)C=C3)CC4=C(O)C=CC=C4', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O(C1C(O)C(O)C(OC1CO)OC2=CC=3OC(CC(=O)C3C(OC)=C2)C4=CC(O)=C(O)C=C4)C5OC(C(O)C(O)C5O)CO', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('Cc1c(O)cc(O)c2C(=O)C[C@H](Oc12)c1ccccc1O', 'Anthoxanthin "
               "with multiple hydroxyl groups'), "
               "('OC1C(OC2=C(C=CC(O)=C2)C1=O)C1=CC=C(O)C(O)=C1', 'Anthoxanthin "
               "with multiple hydroxyl groups'), "
               "('O(C1C(O)C(O)C(OC1OC2=CC=3OC(CC(=O)C3C=C2)C4=CC=C(O)C=C4)CO)C5OCC(O)(C5O)CO', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('CC(C)=CCC[C@]1(C)CCc2c(ccc(O)c2O1)[C@@H]1CC(=O)c2c(O1)cc(O)c(CC=C(C)C)c2O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('CC(=C)[C@H](CC=C(C)C)Cc1c(O)cc(O)c2C(=O)C[C@H](Oc12)c1ccc(O)cc1O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('CC(C)=CCOc1ccc(cc1)[C@@H]1CC(=O)c2c(O)cc(O)cc2O1', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('C1(C(C(C2(C(C1=O)C(C3=C(O2)C(=C(C4=C3OC(CC4=O)C5=CC=CC=C5)O)C)C(C)C)O)(C)C)=O)(C)C', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('O1C(C(O)C(=O)C2=C1C=C(O)C(OC)=C2O)C3=CC=C(OC)C=C3', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1[C@@](CC(=O)C=2C1=CC(O)=CC2O)(C=3C=C(C/C=C(/CCC=C(C)C)\\\\C)C(O)=CC3O)[H]', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('Cc1c(O)c(C)c2O[C@H]([C@H](O)C(=O)c2c1O)c1ccccc1', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1[C@H]([C@H](O)[C@@H](O)[C@@H](O)[C@@H]1OC=2C=C3OC(CC(=O)C3=C(O)C2)C4=CC=C(OC)C=C4)C', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1[C@](C(O)[C@@H](O)[C@H](O)C1CO)(C2=C(O)C3=C(O[C@@H](CC3=O)C4=CC(O)=C(O)C=C4)C=C2O)[H]', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(C1COC=2C=C3OC(CC(=O)C3=C(O)C2)C4=CC=CC=C4)(C)C', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('O1[C@@H](CC(=O)C2=C1C3=C(OC(C=C3)(C)C)C=C2)C4=CC(=C(O)C=C4)CC=C(C)C', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('OC1C(Oc2cc(O)cc(O)c2C1=O)c1cc(O)c(O)c(O)c1', 'Anthoxanthin "
               "with multiple hydroxyl groups'), "
               "('O1C(CC(=O)C2=C1C3=C(OC(C=C3)(C)C)C(=C2O)CC=C(C)C)C4=CC5=C(OC(C=C5)(C)C)C=C4', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('O1[C@]2(CC(C[C@]1(O)/C=C/C3=CC=CC=C3)C=4C=5O[C@H](CC(=O)C5C(O)=CC4OC(=O)CCC2)C6=CC=CC=C6)[H]', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('CC(C)=CCc1cc2C(=O)C[C@H](Oc2c(CC=C(C)C)c1O)c1ccc2OC(C)(C)C=Cc2c1', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('C=1(C=C2OC(C(C(C2=C(C1)O)=O)O)C=3C=CC(=CC3)O)OC4C(C(C(C(O4)CO)O)O)O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O[C@@H]1CO[C@@H](O[C@@H]2[C@H](Oc3cc(O)cc(O)c3C2=O)c2ccc(O)c(O)c2)[C@H](O)[C@H]1O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('OC[C@H]1O[C@@H](OC2=CC3=C(C(=O)C[C@H](O3)C3=CC(O)=C(O)C=C3)C(O)=C2)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('Cc1c(O)c2C(=O)C[C@H](Oc2c(C)c1O[C@@H]1O[C@H](COC(=O)c2ccc(O)cc2)[C@@H](O)[C@H](O)[C@H]1O)c1cc(O)ccc1O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1[C@@H](OC=2C([C@]3(OC4=C(C(=O)C3)C(O)=CC(OC)=C4OC)[H])=C(OC)C=CC2)C(O)[C@@H](O)[C@H](O)C1C(O)=O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(CC(=O)C=2C1=CC(O)=CC2O)C3=CC=C(OC)C=C3', 'Anthoxanthin "
               "with mixed hydroxyl/methoxy substitution'), "
               "('O[C@@H]1[C@H](Oc2cc([O-])cc(O)c2C1=O)c1ccc(O)c(O)c1', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C([C@@H](O)[C@H](O)C(O)[C@@H]1OC2=C(C=3O[C@@H](CC(=O)C3C(O)=C2)C4=CC=C(O)C=C4)CC=C(C)C)CO', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O[C@@H]1[C@H](Oc2cc(O)cc(O)c2C1=O)c1ccc(O)c(O)c1', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O(C1C(O)C(O)C(OC1CO)OC=2C3=C(OC(C(O)C3=O)C4=CC=CC=C4)C=C(O)C2)C5OC(C(O)C(O)C5O)CO', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('CC(C)=CCc1cccc([C@@H]2CC(=O)c3c(O)cc4OC(C)(C)C=Cc4c3O2)c1O', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('O1C(CC(=O)C2=C1C=C(O)C(CCC(O)(C)C)=C2O)C3=CC(O)=C(O)C=C3', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O=C1C2=C(O[C@@H](C1)C3=CC=CC=C3)C(=C(O)C=C2O)C/C=C(/CCC=C(C)C)\\\\C', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('O1C2=C(C(CC1(C3=CC=C(C=C3)O)O)=O)C(=CC(=C2)O)O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('OC[C@H]1O[C@H]([C@H](O)[C@@H](O)[C@@H]1O)c1c(O)cc(O)c2C(=O)C[C@H](Oc12)c1ccc(O)cc1', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1[C@]2(O)[C@@]([C@H](C3=C1C(=C(O)C4=C3O[C@@H](CC4=O)C5=CC=CC=C5)C)C6=CC=CC=C6)(C(=O)C(C(=O)C2(C)C)(C)C)[H]', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('Cc1c(O)c2C(=O)C[C@H](Oc2c(C)c1O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)c1cc(O)ccc1O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1[C@@H](CC(=O)C2=C1C(OC)=C(OC)C(=C2O)CC3=C(O)C=CC(OC)=C3)C4=CC=CC=C4', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('S(OC1=C(OC)C=C(C2OC=3C(C(=O)C2O)=C(O)C=C(O)C3)C=C1)(O)(=O)=O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(C2=CC(=C(O)C(=C2)CC=C(C)C)CC=C(C)C)CC(=O)C3=C1C=C(O)C=C3', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('COc1cc(ccc1O)[C@@H]1CC(=O)c2c(O)cc(O)cc2O1', 'Anthoxanthin "
               "with multiple hydroxyl groups'), "
               "('O1C(OC2C(OC=3C(C2=O)=C(O)C=C(O)C3)C4=CC(OC5OC(C(O)C(O)C5O)C(O)=O)=CC=C4)C(O)C(O)C1CO', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(OC2=C(C3C(OC=4C(C3=O)=C(O)C=C(O)C4)C5=CC=C(O)C=C5)C=6OC(CC(=O)C6C(O)=C2)C7=CC(O)=C(O)C=C7)C(O)C(O)C(O)C1CO', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(CC(=O)C=2C1=C(CC=C(C)C)C(O)=CC2OC)C3=CC=C(O)C=C3', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('O1C([C@H](O)[C@H](O)C(O)[C@@H]1OC=2C=C3OC(CC(=O)C3=C(O)C2)C4=CC=CC=C4)C', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O(C1C(O)C(O)C(OC1OC2=CC=C(C3OC4=C(C(=O)C3)C=CC(OC5OC(C(O)C(O)C5O)C(O)=O)=C4)C=C2)CO)C6OCC(O)(C6O)COC(=O)C=7C=8C(NC7)=CC=CC8', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(C(O)C(O)C(O)C1OC=2C3=C(OC(CC3=O)C4=CC(O)=C(OC)C=C4)C=C(OC)C2)CO', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('CC1=C[C@H]([C@@H]([C@H](C1)c1ccc(O)cc1O)C(=O)c1ccc(O)cc1O)c1c(O)ccc([C@H]2Oc3cc(O)ccc3C(=O)[C@@H]2O)c1O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('CC(C)=CCc1c(O)c(CC=C(C)C)c2O[C@@H](CC(=O)c2c1O)c1cc(O)cc(O)c1', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(OC=2C=C3OC(CC(=O)C3=C(O)C2)C4=CC=C(OC)C=C4)C(O)C(O)C(O)C1', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('COc1cc(OC)c2C(=O)C[C@H](Oc2c1C=O)c1ccccc1', 'Anthoxanthin "
               "with mixed hydroxyl/methoxy substitution'), "
               "('COc1cc(O)c2C(=O)C[C@H](Oc2c1CC=C(C)C)c1cc2C=CC(C)(C)Oc2cc1O', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('COc1cc(O)c(C)c2O[C@@H](CC(=O)c12)c1ccccc1', 'Anthoxanthin "
               "with mixed hydroxyl/methoxy substitution'), "
               "('O1C(C(OC)C(=O)C2=C1C=C(O)C(OC)=C2O)C3=CC(O)=C(OC)C=C3', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('[H][C@@]1(CC(=O)c2c(O)cc3O[C@]4(C[C@]([H])(c5c(O)cc(O[C@@H]6O[C@H](CO)[C@@H](O)[C@H](O)[C@H]6O)cc5O4)c3c2O1)c1ccc(O)c(O)c1)c1ccc(O)c(O)c1', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('Oc1cc(O)c2C(=O)C[C@H](Oc2c1)c1cc(O)c(O)c(O)c1', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(CCC=C(C)C)(C=CC=2C1=CC=3OC(CC(=O)C3C2O)C4=C(O)C=C(O)C=C4)C', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(OC2=C(C3OC4=C(C(=O)C3)C=CC(O)=C4)C(O)=C(C(OC)=C2)CC=C(C)C)C(O)C(O)C(O)C1C(O)=O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('COc1c(O)cc2OC(CC(=O)c2c1O)c1ccccc1', 'Anthoxanthin with "
               "mixed hydroxyl/methoxy substitution'), "
               "('O1[C@@H](CC(=O)C2=C1C(O)=C(O)C=C2O)C3=CC=C(OC)C=C3', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C([C@@H](OC(=O)C2=CC(O)=C(O)C(O)=C2)[C@H](O)C(O)[C@@H]1OC3=C(C=4O[C@@H](CC(=O)C4C(O)=C3C)C5=CC=C(OC)C=C5)C)COC(=O)C6=CC(O)=C(O)C(O)=C6', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(CC(=O)C2=C1C=C(O)C=C2)C3=CC(O)=C(O)C=C3', 'Anthoxanthin "
               "with multiple hydroxyl groups'), "
               "('O1C(OC2=C(O)C=C(C3OC4=C(C5C(OC=6C(C5=O)=C(O)C=C(O)C6)C7=CC=C(O)C=C7)C(O)=CC(O)=C4C(=O)C3)C=C2)C(O)C(O)C(O)C1C(O)=O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O[C@@H]1[C@H](Oc2cc([O-])cc(O)c2C1=O)c1ccc(O)cc1', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('Oc1ccccc1Cc1c(O)cc2O[C@@H](CC(=O)c2c1O)c1ccccc1', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(C=CC=2C=3OC(CC(=O)C3C(O)=C(C12)CC=C(C)C)C4=CC=C(O)C=C4)(C)C', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('C1=2C(C([C@@]3([C@](O1)(C=4C(O3)=CC(=CC4)O)CC=C(C)C)O)=O)=C(C5=C(C2)OC(C=C5)(C)C)O', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('CC(C)=CCc1c(O)cc(O)c2C(=O)C[C@H](Oc12)c1cc(ccc1O)C(C)(C)C=C', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(CC(=O)C2=C1C3=C(OC(C=C3)(C)C)C=C2)C4=CC=C(OC)C=C4', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('O1[C@@](CC(=O)C2=C1C=C(O)C(=C2O)CC=C(C)C)(C=3C(O)=CC(O)=C(OC)C3)[H]', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(C(C=2C=3OC=CC(=O)C3C(O)=CC2O)C(=O)C=4C1=CC(O)=CC4O)C5=CC=C(O)C=C5', "
               "'Anthoxanthin with multiple hydroxyl groups'), "
               "('O1C(CC(=O)C2=C1C(=C(O)C(=C2O)CC=C(C)C)C)C3=CC(=C(OC)C=C3)CC=C(C)C', "
               "'Anthoxanthin with mixed hydroxyl/methoxy substitution'), "
               "('O1C(CCC=C(C)C)(C=CC=2C1=CC(O)=C(C3OC=4C(C(=O)C3)=C(O)C=C(O)C4)C2)CO', "
               "'Anthoxanthin with multiple hydroxyl groups')]\n"
               'False negatives: '
               "[('O1C(=C(CC=C(C)C)C(=O)C=2C1=CC(O)=CC2O)C3=C(O)C=C(O)C=C3', "
               "'Not a flavonoid structure'), "
               "('O1C=2C(C3C(C(CC(=C3)C)C4=C(O)C=C(O)C=C4)C(=O)C5=C(O)C=C(O)C=C5)=C(O)C=C(O)C2C(=O)C(=C1C6=C(O)C=C(O)C=C6)CC=C(C)C', "
               "'Not a flavonoid structure'), "
               "('O1C(C2=CC(CCC(CO)C)=C(O)C=C2)=C(OC)C(=O)C3=C1C=C(O)C(OC)=C3O', "
               "'Not a flavonoid structure'), "
               "('COc1cc2oc(cc(=O)c2c(O)c1C)-c1ccc(OC)c(c1)-c1c(O)cc(O)c2c1oc(cc2=O)-c1ccc(O)cc1', "
               "'Not a flavonoid structure'), "
               "('COc1cc(O)c2c(oc(cc2=O)-c2ccc(O)cc2)c1C', 'Not a flavonoid "
               "structure'), "
               "('[H][C@]12SC(C)(C)C(N1C(=O)[C@H]2NC(=O)C1=CC(=CC=C1)C1=CC(=O)C2=CC=CC=C2O1)C(O)=O', "
               "'Not a flavonoid structure'), "
               "('COc1cc(O)c2c(c1)oc(-c1cc(O)c(OC)c(OC)c1)c(OC)c2=O', 'Not a "
               "flavonoid structure'), "
               "('OC[C@H]1O[C@H]([C@H](O)[C@@H](O)[C@@H]1O)c1c(O)c([C@@H]2OC[C@H](O)[C@H](O)[C@H]2O)c(O)c2c1oc(cc2=O)-c1ccc(O)c(O)c1', "
               "'Not a flavonoid structure'), "
               "('OC[C@@]1(O)CO[C@@H](OC[C@H]2O[C@H]([C@H](O)[C@@H](O)[C@@H]2O)c2c(O)ccc3c2occ(-c2ccc(O)cc2)c3=O)[C@@H]1O', "
               "'Not a flavonoid structure'), "
               "('COc1cc(ccc1O)-c1oc2cc(O[C@H]3O[C@@H](CO)[C@H](O)[C@@H](O)[C@@H]3O)cc(O)c2c(=O)c1O', "
               "'Not a flavonoid structure'), "
               "('[H][C@]1(OC[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1[C@@H](O)[C@H](C)O[C@@H](OC[C@H]2O[C@@H](Oc3c(oc4cc(O)cc(O)c4c3=O)-c3ccc(O)c(O)c3)[C@H](O)[C@@H](O)[C@@H]2O)[C@@H]1O', "
               "'Not a flavonoid structure'), "
               "('CC(=O)O[C@@H]1[C@@H](O)[C@H](O)[C@@H](CO)O[C@H]1Oc1c(oc2cc(O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)cc(O)c2c1=O)-c1ccc(O)cc1', "
               "'Not a flavonoid structure'), "
               "('O1C(C2=CC(CC=C(C)C)=C(O)C=C2)=CC(=O)C3=C1C=C(O)C=C3', 'Not a "
               "flavonoid structure'), "
               "('C[C@@H]1O[C@H](Oc2c(oc3cc(O)cc(O)c3c2=O)-c2ccc(O)c(O)c2)[C@@H](O)[C@H](O)[C@@H]1O', "
               "'Not a flavonoid structure'), "
               "('CC(C)=CCC\\\\C(C)=C\\\\Cc1c(O)cc(O)c2c1oc(cc2=O)-c1ccccc1', "
               "'Not a flavonoid structure'), "
               "('C[C@@H]1O[C@@H](Oc2cc(O)c3c(c2)oc(-c2ccc(O)cc2)c(O)c3=O)[C@H](OC(=O)\\\\C=C\\\\c2ccc(O)cc2)[C@H](OC(=O)\\\\C=C\\\\c2ccc(O)cc2)[C@H]1O', "
               "'Not a flavonoid structure'), "
               "('OC[C@H]1O[C@@H](Oc2cc3oc(-c4ccc(O)c(O)c4)c(O)c(=O)c3c(O)c2Cc2ccc(O)cc2)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Not a flavonoid structure'), "
               "('O1C(C=CC=2C1=C(C=3OC=4C(C(=O)C3CC=C(C)C)=C(O)C=C(O)C4)C=CC2O)(C)C', "
               "'Not a flavonoid structure'), "
               "('C1(OC2OC(C(C(C2O)O)OC(/C=C/C=3C=C(C(=CC3)O)OC)=O)CO)=CC(=C4C(OC(=CC4=O)C5=CC=C(O)C(=C5)C6OC(O)C(C6CO)O)=C1)O', "
               "'Not a flavonoid structure'), ('O=c1cc(oc2ccccc12)-c1ccccc1', "
               "'Not a flavonoid structure'), "
               "('CC(=C)C1Cc2c(O1)cc1oc(-c3ccc(O)c(O)c3)c(O)c(=O)c1c2O', 'Not "
               "a flavonoid structure'), "
               "('OC[C@@H]1O[C@H](Oc2c(oc3cc(O)cc(O)c3c2=O)-c2cc(O)c(O)c(O)c2)[C@@H](O)[C@H](O)[C@@H]1O', "
               "'Not a flavonoid structure'), "
               "('O1C(C2=CC(CC=C(C)C)=C(OC)C=C2)=C(OC)C(=O)C3=C1C=C(O)C(OC)=C3O', "
               "'Not a flavonoid structure'), "
               "('CC(C)=CCc1c(O)c(CC=C(C)C)c2oc(cc(=O)c2c1O)-c1ccccc1', 'Not a "
               "flavonoid structure'), "
               "('OC[C@H]1O[C@@H](Oc2cc3oc(cc(=O)c3c(O)c2[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)-c2ccc(O)cc2)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Not a flavonoid structure'), "
               "('C1(=O)C=C(C2=CC=C(C=C2)O)OC3=C1C(O)=C(C(=C3)OC)O', 'Not a "
               "flavonoid structure'), "
               "('COc1cc(cc(OC)c1OC)-c1cc(=O)c2c(OC)c(OC)c(OC)c(OC)c2o1', 'Not "
               "a flavonoid structure'), "
               "('COc1ccc(OC)c(c1)-c1cc(=O)c2c(OC)c(OC)c(OC)c(OC)c2o1', 'Not a "
               "flavonoid structure'), "
               "('O1C=2C(C(=O)C=C1C3=CC=CC=C3)=C(O)C=CC2', 'Not a flavonoid "
               "structure'), "
               "('COc1cc(\\\\C=C\\\\C(=O)OC[C@H]2OC(Oc3cc(O)c4c(c3)oc(cc4=O)-c3cc(OC)c(O)c(OC)c3)[C@H](O)[C@@H](O)[C@@H]2O)cc(OC)c1O', "
               "'Not a flavonoid structure'), "
               "('COc1cc(ccc1O)-c1cc(=O)c2c(O)cc(O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O[C@@H]3O[C@@H](C)[C@H](O)[C@@H](O)[C@H]3O)cc2o1', "
               "'Not a flavonoid structure'), "
               "('Oc1ccc(c(O)c1)-c1oc2cc(O)cc(O)c2c(=O)c1O', 'Not a flavonoid "
               "structure'), ('COc1cc(OC)c2c(c1)oc(-c1ccccc1)c(OC)c2=O', 'Not "
               "a flavonoid structure'), "
               "('COc1ccc(cc1O)-c1cc(=O)c2c(O)cc(O[C@@H]3O[C@H](CO[C@@H]4O[C@@H](C)[C@H](O)[C@@H](O)[C@H]4O)[C@@H](O)[C@H](O)[C@H]3O)cc2o1', "
               "'Not a flavonoid structure'), "
               "('S(OC=1C=C(C=2OC3=C(C(=O)C2)C=CC(O)=C3)C=CC1)(O)(=O)=O', 'Not "
               "a flavonoid structure'), "
               "('CN1CCCCC1c1c(O)cc(O)c2c1oc(cc2=O)-c1ccccc1', 'Not a "
               "flavonoid structure'), "
               "('COc1cc(O)cc2oc(-c3cc(O)c(O)c(O)c3)c(O[C@@H]3O[C@@H](C)[C@H](O)[C@@H](O)[C@H]3O)c(=O)c12', "
               "'Not a flavonoid structure'), "
               "('Oc1ccc2c(c1)oc(-c1ccc(O)c(O)c1)c(O)c2=O', 'Not a flavonoid "
               "structure'), "
               "('COc1cc(ccc1O)-c1cc(=O)c2c(O)c([C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)c(O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O[C@@H]3O[C@@H](C)[C@H](O)[C@@H](O)[C@H]3O)cc2o1', "
               "'Not a flavonoid structure'), "
               "('CC(C)=CCc1ccc(cc1O)-c1oc2c(CC=C(C)C)c(O)c(CC=C(C)C)c(O)c2c(=O)c1O', "
               "'Not a flavonoid structure'), "
               "('[H][C@]1(O[C@H](COC(=O)\\\\C=C\\\\c2ccc(O)cc2)[C@@H](O)[C@H](O)[C@H]1O)O[C@H]1[C@@H](O[C@@H](C)[C@H](O)[C@H]1O)Oc1c(oc2cc(O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3O)cc(O)c2c1=O)-c1ccc(O)c(O)c1', "
               "'Not a flavonoid structure'), "
               "('O1C2=C(C(O)=C(CC=C(CO)C)C(O)=C2)C(=O)C=C1C3=C(O)C=C(O)C=C3', "
               "'Not a flavonoid structure'), "
               "('Oc1cc(O)c2c(c1)oc(-c1ccc(O)c(OS(O)(=O)=O)c1)c(OS(O)(=O)=O)c2=O', "
               "'Not a flavonoid structure'), "
               "('Oc1cc(O)c2c(c1)oc(cc2=O)-c1cc(O)c(O)cc1O', 'Not a flavonoid "
               "structure'), "
               "('O=C1C(O)=C(OC2=C1C(O)=CC(=C2CC=C(C)C)O)C3=CC=C(OC)C=C3', "
               "'Not a flavonoid structure'), "
               "('C1=2C(C=C(OC1=CC(=CC2O)O)C=3C=C(OC)C(=C(C3)OC)O[C@H]([C@@H](C4=CC(OC)=C(C=C4)O)O)CO[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O)O)O)=O', "
               "'Not a flavonoid structure'), "
               "('O1C(C(O)CC2=C1C=C3OC(=CC(=O)C3=C2O)C4=CC=C(O)C=C4)(C)C', "
               "'Not a flavonoid structure'), "
               "('C[C@@H]1O[C@@H](OC[C@H]2O[C@@H](Oc3c(oc4cc(O)c(O)c(O)c4c3=O)-c3ccc(O)cc3)[C@H](O)[C@@H](O)[C@@H]2O)[C@H](O)[C@H](O)[C@H]1O', "
               "'Not a flavonoid structure'), "
               "('[C@H]1(O[C@H]([C@@H]([C@H]([C@H]1O)O)O)C)O[C@H]2[C@@H](O[C@@H]([C@H]([C@@H]2O)O)CO)OC3=CC4=C(C(C=C(O4)C5=CC(=C(C(=C5)OC)O)OC)=O)C(=C3)O', "
               "'Not a flavonoid structure'), "
               "('O1C(=C(CC=C(C)C)C(=O)C=2C1=CC(O)=CC2O)C=3C(OC)=CC(OC)=C(O)C3', "
               "'Not a flavonoid structure'), "
               "('C1(=C(C(=C(C2=C1OC(=C(C2=O)*)C3=C(C(=C(C(=C3*)*)*)[H])*)*)*)*)*', "
               "'Not a flavonoid structure'), "
               "('COc1cc2oc(-c3ccc(O)cc3O)c(CC=C(C)C)c(=O)c2c(O)c1\\\\C=C\\\\C(C)C', "
               "'Not a flavonoid structure'), "
               "('O1C([C@@H](O)[C@@H](O)[C@H](O)C1O)COC2=C(OC=3C(C2=O)=C(O)C=C(O)C3)C4=CC(O)=C(O)C=C4', "
               "'Not a flavonoid structure'), "
               "('C1=2C(OC(=CC1=O)C3=CC(=C(C=C3)O)O)=CC(=C(C2O)[C@H]4[C@@H]([C@H]([C@H](CO4)O)O)O[C@H]5[C@@H]([C@H]([C@@H]([C@@H](CO)O5)O)O)O)O', "
               "'Not a flavonoid structure'), "
               "('COc1cc(OC)c(cc1OC)-c1cc(=O)c2c(OC)c(OC)c(OC)c(OC)c2o1', 'Not "
               "a flavonoid structure'), "
               "('CN1CCCC1c1c(O)cc2oc(cc(=O)c2c1O)-c1ccccc1', 'Not a flavonoid "
               "structure'), "
               "('[H][C@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)c1c(O)c(O)c2oc(cc(=O)c2c1O)-c1ccc(O)cc1', "
               "'Not a flavonoid structure'), "
               "('Cc1c(oc2cc(O)cc(O)c2c1=O)-c1ccc(O)c(O)c1', 'Not a flavonoid "
               "structure'), "
               "('COc1cc(O)c2c(c1)oc(-c1cc(OC)c(OC)c(OC)c1)c(OC)c2=O', 'Not a "
               "flavonoid structure'), "
               "('O([C@H]1[C@@H]([C@H]([C@@H]([C@@H](COC(=O)/C=C/C2=CC(=C(C=C2)O)OC)O1)O)O)O)[C@@H]3[C@H]([C@@H]([C@H](O[C@H]3C4=C(C=C5C(=C4O)C(C=C(O5)C6=CC=C(C(=C6)OC)O)=O)O)CO)O)O', "
               "'Not a flavonoid structure'), "
               "('S(OCC1(OC2=C(C(O)=C3C(OC(=C(C3=O)C/C=C(\\\\CCC=C(C)C)/C)C4=C(O)C=C(O)C=C4)=C2)C=C1)C)(O)(=O)=O', "
               "'Not a flavonoid structure'), "
               "('OC[C@H]1O[C@@H](Oc2c(oc3cc(O)cc(O)c3c2=O)-c2ccc(O)cc2)[C@H](O)[C@H](O)[C@@H]1O', "
               "'Not a flavonoid structure'), "
               "('O[C@H]1[C@H](Oc2c(oc3cc(O)cc(O)c3c2=O)-c2cc(O)c(O)c(O)c2)O[C@@H]([C@@H](O)[C@@H]1O)C(O)=O', "
               "'Not a flavonoid structure'), "
               "('O[C@@H]1[C@@H](COC(=O)\\\\C=C\\\\c2ccc(O)cc2)O[C@@H](Oc2c(oc3cc(O)cc(O)c3c2=O)-c2ccc(O)cc2)[C@H](O)[C@H]1O', "
               "'Not a flavonoid structure'), "
               "('COc1c(oc2cc(O[C@@H]3O[C@H](CO[C@@H]4O[C@@H](CO)[C@H](O)[C@H]4O)[C@@H](O)[C@H](O)[C@H]3O)cc(O)c2c1=O)-c1ccc(O)cc1', "
               "'Not a flavonoid structure'), "
               "('COc1ccc(cc1)-c1cc(=O)c2c(O)c(OC)c(O)c(OC)c2o1', 'Not a "
               "flavonoid structure')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 66,
    'num_false_positives': 100,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.39759036144578314,
    'recall': 1.0,
    'f1': 0.5689655172413793,
    'accuracy': 0.39759036144578314}