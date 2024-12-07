"""
Classifies: CHEBI:15693 aldose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_aldose(smiles: str):
    """
    Determines if a molecule is an aldose (aldehydic parent sugar or its intramolecular hemiacetal).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an aldose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for required elements (C, H, O only)
    allowed_atoms = {'C', 'H', 'O'} 
    mol_atoms = {atom.GetSymbol() for atom in mol.GetAtoms()}
    if not mol_atoms.issubset(allowed_atoms):
        return False, f"Contains disallowed elements: {mol_atoms - allowed_atoms}"

    # Count hydroxy groups
    num_oh = len(mol.GetSubstructMatches(Chem.MolFromSmarts('[OH]')))
    if num_oh < 2:
        return False, "Must have at least 2 hydroxy groups"

    # Check for either aldehyde or hemiacetal
    has_aldehyde = len(mol.GetSubstructMatches(Chem.MolFromSmarts('[CH]=O'))) > 0
    
    # More specific hemiacetal patterns for sugars
    pyranose_pattern = Chem.MolFromSmarts('[C]1[O][C@H]([OH])[C@H]([OH])[C@H]([OH])[C@H]1[OH,CH3,CH2OH]')
    furanose_pattern = Chem.MolFromSmarts('[C]1[O][C@H]([OH])[C@H]([OH])[C@H]1[OH,CH3,CH2OH]')
    
    has_hemiacetal = mol.HasSubstructMatch(pyranose_pattern) or mol.HasSubstructMatch(furanose_pattern)

    # Check carbon chain length (at least 3 carbons)
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 3:
        return False, "Must have at least 3 carbons"

    if has_aldehyde:
        # For open-chain form, check for polyhydroxy aldehyde pattern
        aldehyde_pattern = Chem.MolFromSmarts('[CH](=O)[CH]([OH])[CH]([OH])')
        if mol.HasSubstructMatch(aldehyde_pattern):
            return True, "Open-chain aldose"
    
    if has_hemiacetal:
        # For cyclic forms, check specific sugar patterns
        if mol.HasSubstructMatch(pyranose_pattern):
            return True, "Pyranose form (hemiacetal)"
        elif mol.HasSubstructMatch(furanose_pattern):
            return True, "Furanose form (hemiacetal)"

    # Additional check for deoxy sugars and other variations
    deoxy_pyranose = Chem.MolFromSmarts('[C]1[O][C@H]([OH])[C@H]([OH])[C@H]([H])[C@H]1[OH,CH3,CH2OH]')
    deoxy_furanose = Chem.MolFromSmarts('[C]1[O][C@H]([OH])[C@H]([H])[C@H]1[OH,CH3,CH2OH]')
    
    if mol.HasSubstructMatch(deoxy_pyranose) or mol.HasSubstructMatch(deoxy_furanose):
        return True, "Deoxy sugar form (hemiacetal)"
        
    return False, "Does not match aldose structure requirements"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15693',
                          'name': 'aldose',
                          'definition': 'Aldehydic parent sugars (polyhydroxy '
                                        'aldehydes H[CH(OH)]nC(=O)H, n >= 2) '
                                        'and their intramolecular hemiacetals.',
                          'parents': ['CHEBI:35381']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.047619047619047616 is too low.\n'
               "True positives: [('C([C@H]([C@@H](C(=O)[H])O)O)O', 'Open-chain "
               "aldose'), "
               "('[H][C@](C)(O)[C@@]([H])(O)[C@]([H])(O)[C@@]([H])(O)C=O', "
               "'Open-chain aldose'), "
               "('O[C@@H]([C@H](O)[C@@H](O)C=O)[C@@H](O)CO', 'Open-chain "
               "aldose')]\n"
               'False positives: '
               "[('O=C1OC[C@]23[C@H]1[C@@](O[C@H]2[C@H](O)CO3)(O)CCCCC', "
               "'Pyranose form (6-membered ring)'), "
               "('[H][C@]12C(C)(C)CCC[C@@]11C(=O)O[C@]2(O)C(=O)C2=C[C@](C)(C[C@@H](O)[C@]12O)C=C', "
               "'Pyranose form (6-membered ring)'), "
               "('OC[C@H]1O[C@H](O[C@@H]2[C@@H](CO)O[C@H](O[C@@H]3[C@@H](CO)OC(O)(CO)[C@H]3O)[C@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C1O[C@@](O)(CCCCCC)C=2C1=C(O)C=CC2', 'Pyranose form "
               "(6-membered ring)'), "
               "('O=C1C2=C(OC3=C1[C@H]4C=5OC6=C(C(O)=CC(=C6)C)C(C5[C@@]7([C@H]4[C@H](C3)C(O)(C(=O)OCC)O7)C(=O)OC)=O)C=C(C)C=C2O', "
               "'Pyranose form (6-membered ring)'), "
               "('C[C@@]12C[C@@]3(O)O[C@@H](O1)[C@]1(COC(=O)c4ccccc4)[C@H]3C[C@]21O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C1O[C@@H]([C@@H]([C@H](O)[C@@H](CC(=C[C@@H]([C@@H](O)[C@@H]([C@@H](O)CC)C)C)C)C)C)CC=C(C)CC2(OC(C1)(O)[C@@H](C2=O)CC)C', "
               "'Pyranose form (6-membered ring)'), "
               "('[H]C(=O)[C@H](O)[C@@H](O)CC(=O)C(O)=O', 'Open-chain "
               "aldose'), "
               "('O1[C@@]2(O)[C@](O)([C@H]3C=C(CC[C@@H]3[C@H](C2)C)C)C(C1)=C', "
               "'Pyranose form (6-membered ring)'), "
               "('[H]C(=O)[C@@H](O)[C@@H](O)[C@H](O)[C@@H](O)C(O)=O', "
               "'Open-chain aldose'), "
               "('O1C2(O)[C@@]3(O)C(CCC[C@]3(C1)[C@@]4(O)[C@H](O)C[C@@](C=C4C2O)(C=C)C)(C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('CC(C)C1=CC(=O)[C@]2(C)C[C@]3(O)O[C@@]4([C@H](O)[C@@H](C)CC[C@]24O)C(=O)[C@]13C', "
               "'Pyranose form (6-membered ring)'), "
               "('O1[C@@]2(O)[C@](O)(C3=C(CC(C3)(C)C)[C@H]([C@@H]2O)C)C(C1)=C', "
               "'Pyranose form (6-membered ring)'), "
               "('O([C@]([C@](O[H])([C@](O[H])(C(=O)[H])[H])[H])([C@@](O[H])(C([H])([H])[H])[H])[H])[H]', "
               "'Open-chain aldose'), "
               "('[H][C@@]12CC[C@]3(O)OC[C@@]1(CC[C@@]1([H])[C@@]2(C)CC[C@@]2(C)[C@]4([H])C[C@@](C)(CC[C@]4(C)CC[C@]12C)C(O)=O)[C@H]3C', "
               "'Pyranose form (6-membered ring)'), "
               "('O[C@H](CC(O)=O)[C@H](O)[C@@H](O)C=O', 'Open-chain aldose'), "
               "('OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](OC[C@H]3O[C@@H](OC[C@H]4O[C@@H](OC[C@H]5O[C@@H](OC[C@@H](O)[C@H](O)[C@H](O)[C@@H](O)C=O)[C@H](O[C@@H]6O[C@@H](CO)[C@H](O)[C@H]6O)[C@@H](O)[C@H]5O)[C@H](O)[C@@H](O)[C@H]4O)[C@H](O)[C@@H](O)[C@H]3O)[C@H](O[C@@H]3O[C@@H](CO[C@@H]4O[C@@H](CO)[C@H](O)[C@H]4O)[C@H](O)[C@H]3O)[C@@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@H]1O', "
               "'Open-chain aldose'), "
               "('O=C(O[C@@H]1C(=CC[C@H]2[C@H]1[C@]3(O)C(=C)CO[C@]3(O)C[C@@H]2C)C)CCCCCCC', "
               "'Pyranose form (6-membered ring)'), "
               "('OC[C@@H]1O[C@](O)(CO)[C@H](O)[C@H]1O', 'Pyranose form "
               "(6-membered ring)'), "
               "('O=C1O[C@H]2C=C[C@H]([C@@]13[C@@H](O)[C@](O)(C)O[C@H]32)/C=C/C=C/C', "
               "'Pyranose form (6-membered ring)'), "
               "('OC[C@@]1(O)O[C@@H]([C@@H](O)[C@@H]1O)C(O)=O', 'Pyranose form "
               "(6-membered ring)'), "
               "('O1C2C(C3(C(C4C(CC3)C5(C(=CC4)CC(OC6OC(C(O)C(OC7OC(C(O)C(O)C7O)CO)C6O)CO)CC5)C)C2)C)C(C1(O)CCC(COC8OC(C(O)C(O)C8O)CO)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('OC[C@H]1O[C@@](CO)(OC[C@H]2O[C@](O)(CO)[C@@H](O)[C@@H]2O)[C@@H](O)[C@@H]1O', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C1C(=C(O)C(=C(O)C=CC=CCO)[C@H]2[C@@]1(O[C@@]3(O)[C@@](O)(CC(C([C@@]23C)=O)C(=O)CCC=CC)C)C)C', "
               "'Pyranose form (6-membered ring)'), ('O1[C@](O)(CCC1)CO', "
               "'Pyranose form (6-membered ring)'), "
               "('CCC(C)C(=O)O[C@@H]1[C@H]2[C@@H](C)[C@@H](O)[C@]3(O)OC[C@@]22[C@H]3[C@@]3(C)[C@H](O)C(=O)C=C(C)[C@@H]3C[C@H]2OC1=O', "
               "'Pyranose form (6-membered ring)'), "
               "('O1C(=O)C=2[C@]3([C@@H]([C@H](C=C4C3(OC([C@@]4(CC2C1=O)CC(=O)[O-])=O)O)CCCCC/C=C/C)C[C@@H](C(CC/C=C/C)=O)O)[H]', "
               "'Pyranose form (6-membered ring)'), "
               "('OC[C@H]1OC(O)(CO)[C@H](O)[C@H]1O', 'Pyranose form "
               "(6-membered ring)'), "
               "('[C@]12([C@@]([C@](OC1)(C3=CC(=C(C=C3)O)OC)O)(CO[C@@H]2C4=CC(=C(C=C4)O)OC)[H])[H]', "
               "'Pyranose form (6-membered ring)'), "
               "('OC[C@H]1O[C@](O)(COC[C@H]2O[C@](O)(CO)[C@@H](O)[C@@H]2O)[C@@H](O)[C@@H]1O', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C(O[C@H]1[C@@]23O[C@@H]2[C@@]4(OC[C@H]([C@@H]4C[C@@]3([C@@H](C)CC1)C)C)O)[C@@H]([C@H](O)/C(=C/C(CO)CCCCCC)/C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('CO[C@@H]1C[C@@]2(O)[C@@H](O1)O[C@H]1C[C@@H]2[C@]2(C)O[C@]12[C@@]1(C)[C@@H]2[C@](O)(OC[C@]22[C@H]3[C@@H](OC[C@@]3([C@@H](C[C@@H]2OC(=O)C(\\\\C)=C\\\\C)OC(C)=O)C(=O)OC)[C@H]1O)C(=O)OC', "
               "'Pyranose form (6-membered ring)'), "
               "('O1C(O)(C(O)C(O)C1CO)COC2OC(C(O)C(O)C2O)C(O)=O', 'Pyranose "
               "form (6-membered ring)'), "
               "('O=C1C=C2C(=COC(=C2)/C=C/[C@H]([C@H](O)C)C)[C@H]3[C@@]1(O[C@]4(O)[C@@H]([C@@H](C)OC([C@H]34)=O)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O1[C@@]2(O)[C@]3([C@@](O)(C4=C([C@H](OC)C[C@]4(C)CC3)C(C)C)C[C@@H]1[C@@H](CO)[C@H]2O)C', "
               "'Pyranose form (6-membered ring)'), "
               "('[H][C@]12C[C@@]3([H])[C@]4([H])C[C@H](O[C@@H]5O[C@H](C)[C@@H](O)[C@H](O[C@@H]6O[C@@H](C)[C@H](O)[C@@H](O)[C@H]6O)[C@H]5O)[C@@]5([H])CC(=O)CC[C@]5(C)[C@@]4([H])CC[C@]3(C)[C@@]1([H])[C@H](C)[C@@](O)(CC[C@H](C)CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O2', "
               "'Pyranose form (6-membered ring)'), "
               "('OC[C@H]1O[C@H](OC[C@H]2O[C@@](O)(CO)[C@@H](O)[C@@H]2O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C1C(=C(O)C(=C(O)C=CC=CCO)[C@H]2[C@@]1(O[C@@]3(O)[C@@](O)(CC(C([C@@]23C)=O)=C(O)C=CC=CCO)C)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O1[C@]2(O)[C@@H](CCC=3C(OC(=O)C3CO)=C[C@]1(CC2)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O1[C@@](O)([C@@]2([C@@]3([C@]1(C(OC[C@H]3C)=O)[H])[H])[C@H](O)C(=O)C(=CC2)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O1C(O)(C2(OC(C(C2)C)C(C(=O)C(C(O)C(C3OC(O)(C(CC3C)C)CC)C)C)CC)C)C(CC1(C(O)C)CC)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O1[C@@]2([C@@]([C@@]3([C@]([C@]4([C@@]([C@@]5([C@](CC4)(C[C@@H](O)CC5)[H])C)(CC3)[H])[H])(C2)[H])C)([C@@H]([C@@]1(O)CC[C@@H](CO[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)CO)C)C)[H])[H]', "
               "'Pyranose form (6-membered ring)'), "
               "('O1[C@@]2(O)[C@](O)(C3=C(C[C@](C3)(CO)C)[C@H]([C@@H]2O)C)C(C1)=C', "
               "'Pyranose form (6-membered ring)'), "
               "('O1[C@@]2([C@@]([C@@]3([C@]([C@]4([C@@]([C@@]5([C@@](CC4)(C[C@@H](O)CC5)[H])C)(CC3)[H])[H])(C2)[H])C)([C@@H]([C@@]1(O)CC[C@H](CO[C@@H]6O[C@@H]([C@@H](O)C(O)C6O)CO)C)C)[H])[H]', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C1C2=C[C@@](C=C)(C[C@H](C2(O)[C@]34CCCC([C@@]4([C@]1(OC3)O)O)(C)C)O)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O1C2(O)[C@]3([C@@H](C4=C(C(C)C)C[C@H]([C@]4(C)CC3)O)C[C@@H]1[C@]5(CO)[C@H]2O5)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C1C2=C([C@]34CCCC([C@@]4([C@@]1(OC3)O)O)(C)C)[C@H](O)C[C@@]([C@@H]2O)(C=C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('OC[C@@H](O)[C@@H](O[C@H]1O[C@H](CO)[C@@H](O[C@H]2O[C@H](CO)[C@@H](O[C@H]3O[C@H](CO)[C@@H](O[C@H]4O[C@H](CO)[C@@H](O[C@H]5O[C@H](CO)[C@@H](O[C@H]6O[C@H](CO)[C@@H](O)[C@H](O)[C@H]6O)[C@H](O)[C@H]5O)[C@H](O)[C@H]4O)[C@H](O)[C@H]3O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)[C@@H](O)C=O', "
               "'Open-chain aldose'), "
               "('O=C1[C@@H](O)[C@]2([C@@H](CC(=C)[C@@]3([C@H]2C(=O)OC3(O)[C@](O)(C(=O)OC)C)C)[C@]4([C@H]1C(C(=O)CC4)(C)C)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('[H]C(=O)[C@@H](O)[C@@H](O)CC(=O)C([O-])=O', 'Open-chain "
               "aldose'), "
               "('O=C1C(=C2[C@@H]3[C@@]([C@@]4(O[C@H](C3)[C@@H](CO)[C@H]4O)O)(C)CC[C@]2(C1)C)C(CO)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C1/C(=C/[C@H](O)C)/C[C@H](O)[C@@]23[C@@]1(OC(C)(C)[C@@H]2C3)O', "
               "'Pyranose form (6-membered ring)'), "
               "('[H][C@@](O)(CO[C@H]1O[C@H](CO[C@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2O)[C@H](O)[C@H](O)[C@H]1O)[C@@]([H])(O)[C@]([H])(O)[C@@]([H])(O)C=O', "
               "'Open-chain aldose'), "
               "('O1[C@@]2([C@@]3(O[C@@]4([C@@]1(O)C5(C2C(C(=O)[C@@]3(C4C(C5=O)=C(O)/C=C/C=C/C)C)=C(O)/C=C/C=C/C)C)C)O)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C1OC(O)(CCC(=O)OC)C=2C1=C3C(O[C@]4(CCC5[C@](C4C3)(CCC6[C@@]5(CCC7[C@]6(CCC8[C@@]7([C@@H](CC9[C@]8(CCC%10[C@@]9([C@@H](CC([C@@]%10(C(=O)O)C)OC%11O[C@H](C(=O)O)[C@@H](O)[C@@H]([C@H]%11OC)O)C)C)C)C)C)C)CO)C)CO)=CC2', "
               "'Pyranose form (6-membered ring)'), ('O1C(O)(C(O)C(O)C1CO)CO', "
               "'Pyranose form (6-membered ring)'), "
               "('O1C2(O)C3C(C(C(CC3C4OC=5C(C(=O)C4O)=C(O)C=C(O)C5)C2=O)C6=CC(OC)=C(O)C=C6)C1', "
               "'Pyranose form (6-membered ring)'), "
               "('O1C2(O)C3C4(C(C(C2O)C)C(OC5OC(C(O)C(O)C5O)CO)C(OC4CC6C3(C(O)C(=O)C=C6C)C)=O)C1', "
               "'Pyranose form (6-membered ring)'), "
               "('O1C2(O)C3(C4C5(C(OC(=O)C=C5C(=C(O)C14)C)CC3C(CC2=O)C)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C1C(=C(O)/C=C/C=C/C)[C@H]2[C@@](O)(C)C([C@@]1([C@@H](/C=C/C(O)=C3C(=O)[C@@]4([C@]5(O[C@@]6([C@@H]4C(=C(O)/C=C/C=C/C)C([C@]7([C@@H]3[C@@]5(O[C@@]76O)C)C)=O)C)O)C)[C@@H]2C)C)=O', "
               "'Pyranose form (6-membered ring)'), "
               "('C[C@H](CC[C@@]1(O)O[C@H]2C[C@H]3[C@@H]4CC=C5C[C@H](CC[C@]5(C)[C@H]4CC[C@]3(C)[C@H]2[C@@H]1C)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O)[C@H]2O)[C@H]1O[C@@H]1O[C@@H](C)[C@H](O)[C@@H](O)[C@H]1O)CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C1C2=C([C@]34CCCC([C@@]4([C@@]1(OC3)O)O)(C)C)[C@H](O)C[C@@]([C@@H]2OC)(C=C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C1[C@]23[C@](O[C@@H]([C@H]2C(=C4CC[C@]([C@H]4C3)(O)C)C)C=C(C)C)(O)[C@@H]5C[C@@]1(O)CO5', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C1/C(=C(\\\\O)/C=C/C=C/C)/C2[C@@]3(O[C@@]4([C@H]2C(=O)\\\\C(\\\\C5[C@]1([C@]3(O[C@@]54C)O)C)=C(/O)\\\\C=C\\\\C=C\\\\C)O)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C([C@@H]([C@H]1O[C@@]([C@@]2(O[C@]([C@H](O)C)(CC)C[C@H]2C)O)(C)C[C@@H]1C)CC)[C@H]([C@@H](O)[C@@H]([C@H]3O[C@](O)([C@H](C)C[C@@H]3C)CC)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O1C2C3(O)C4(C1(O)CC(C3CC4C(COC5OC(C(O)C(O)C5O)CO)C)(C6C2C(O)(CC6)C)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('CCC(O)CC1CCCC2(CC3OC(=O)\\\\C=C\\\\C(C)(O)C(O)C(C)C(O)C(O)C(O)C(C)(O)CCCCC\\\\C=C\\\\C4CC(C)(C)OC4(O)CC(O2)C3C)O1', "
               "'Pyranose form (6-membered ring)'), "
               "('O1[C@@]23[C@@]4(O)[C@]5([C@]1(O)C[C@]([C@]4(O)C[C@]5(O)C(C)C)([C@@]2(O)CC[C@@H]([C@H]3O)C)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O1[C@]2(O)[C@H](O)C(C)=C3[C@@H]2[C@@H](C1)CCC4=C([C@H](CO)C)CC[C@@]4(C3)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O1[C@@]2(O)[C@]3([C@@H](C4=C([C@@H](OC)C[C@]4(C)CC3)C(C)C)C[C@@H]1[C@H](CO)[C@H]2O)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C(O)[C@H]([C@H](OC)[C@@H]([C@H]1O[C@]2(O[C@H]([C@@H]3O[C@@]([C@@H]4O[C@@H]([C@]5(O[C@@]([C@H](O)CC)(C)C[C@@H]5C)O)C[C@@H]4C)(C)C[C@H]3O[C@@H]6O[C@@H]([C@@H](OC)CC6)C)CC2)[C@H](C)[C@@H]([C@H]1C)OC)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O1C2C(C3(C(C4C(C5(C(CC4)CC(OC6OC(C(O)C(O)C6OC7OC(C(O)C(O)C7O)CO)CO)CC5)C)CC3)C2)C)C(C1(O)CCC(COC8OC(C(O)C(O)C8O)CO)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O1C2C(C3(C(C4C(C5(C(CC4)CC(OC6OC(C(OC7OC(C(O)C(O)C7O)C)C(O)C6OC8OC(C(O)C(O)C8O)C)CO)C(O)C5)C)CC3)C2)C)C(C1(O)CCC(COC9OC(C(O)C(O)C9O)CO)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O1[C@@]2(O)[C@]3([C@@H](C4=C([C@H](O)[C@@H]([C@]4(C)CC3)O)C(C)C)C[C@@H]1[C@H](CO)[C@H]2O)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O[C@H](CC([O-])=O)[C@H](O)[C@@H](O)C=O', 'Open-chain "
               "aldose'), "
               "('O=C1O[C@@]2([C@H](CC=C([C@H]3O[C@](O)(C)[C@@H]4[C@H]3C(=C(CC2)C)OC4=O)C)[C@@](C1=O)(O)C(C)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C1C2=C[C@H]3[C@@]4(/C=C/C(O)(C)C)[C@](O)([C@@H]5[C@H]([C@@H]([C@H]4[C@@H]2[C@@H](O)[C@H]6[C@@H]1O6)O)O5)OC3(C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C1C(=C(O)C(=C(O)C=CC=CCO)[C@H]2[C@@]1(O[C@@]3(O)[C@@](O)(CC(C([C@@]23C)=O)=C(O)C=CC=CC)C)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('CC1=CC(=O)[C@@H](O)[C@]2(C)[C@H]3[C@@]4(O)OC[C@@]33[C@@H](C[C@@H]12)OC(=O)C[C@H]3C(=C)[C@H]4O', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C1/C(=C/[C@@H](O)C)/C[C@H](O)[C@@]23[C@@]1(OC(C)(C)[C@@H]2C3)O', "
               "'Pyranose form (6-membered ring)'), "
               "('O1C2(O)C3C4(C(C(C2O)C)C(OC5OC(C(O)C(O)C5O)CO)C(OC4CC6C3(C(O)C(O)C=C6C)C)=O)C1', "
               "'Pyranose form (6-membered ring)'), "
               "('O1C2C(C3(C(C4C(CC3)C5(C(=CC4)CC(O)CC5)C)C2)C)C(C1(O)CCC(COC6OC(C(O)C(O)C6O)CO)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O1[C@]2(O)[C@@]3(O)C(CCC[C@]3(C1)C=4CC[C@@]([C@@H](C4[C@@H]2O)O)(C=C)C)(C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O([C@]([C@@](O[H])([C@](O[H])(C(=O)[H])[H])[H])([C@@](O[H])(C([H])([H])[H])[H])[H])[H]', "
               "'Open-chain aldose'), "
               "('O1C2C(C3(C(C4C(C5(C(CC4)CC(OC6OC(C(OC7OCC(O)C(O)C7O)C(O)C6OC8OC(C(O)C(O)C8O)CO)CO)CC5)C)CC3)C2)C)C(C1(O)CCC(COC9OC(C(O)C(O)C9O)CO)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C1O[C@@]2(C(CC=C([C@@H]3O[C@](O)(C)[C@@H]4[C@H]3C(=C(CC2)C)OC4=O)C)=C([C@H]1O)C(C)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('O1[C@@H]([C@@H](O)[C@H](O)[C@@H](O)[C@@H]1OC[C@@H](O)[C@@H](O)[C@H](O)[C@@H](O)C=O)COC2O[C@@H]([C@@H](O)[C@H](O)[C@H]2O)CO', "
               "'Open-chain aldose'), "
               "('C[C@H]1[C@@H](O)[C@]2(O)OC[C@]34[C@H]2[C@@]2(C)[C@H](O)[C@@H](O)C=C(C)[C@@H]2C[C@H]3OC(=O)C[C@@H]14', "
               "'Pyranose form (6-membered ring)'), "
               "('[H]C(=O)[C@H](O)[C@@H](O)[C@@H](O)[C@H](O)C([O-])=O', "
               "'Open-chain aldose'), "
               "('O1C2(O)C(C3C(C4(C(C5(C(CC4)C(C(OC6OC(C(O)C(O)C6O)COC7OC(C(O)C(O)C7O)C)CC5)(C)C)C)CC3)C)(C2O)C)C(O)(C1CC=C(C)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('OC[C@@H]1OC(O)(CO)[C@@H](O)[C@@H]1O', 'Pyranose form "
               "(6-membered ring)'), "
               "('O=C1C2=C(OC3=C1C4C=5OC6=C(C(O)=CC(=C6)C)C(C5C7(C4C(C3)C(O)(C(=O)OC)O7)C(=O)OC)=O)C=C(C)C=C2O', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C1C=CC2=C[C@@]3(OC[C@@H]([C@@]3(C[C@@]2([C@H]1C)C)O)C)O', "
               "'Pyranose form (6-membered ring)'), "
               "('C\\\\C=C\\\\C=C\\\\C(=O)C1=C(O)[C@@]2(C)[C@H]3C(C(=O)\\\\C=C\\\\C=C\\\\C)=C(O)[C@@]4(C)[C@@H]1[C@@]1(C)O[C@]4(O)[C@]3(C)O[C@@]21O', "
               "'Pyranose form (6-membered ring)'), "
               "('O=C1C(C(=O)[C@]2([C@H]3C(C(O)=C(C([C@]3(O[C@]2([C@]1(O)C)O)C)=O)C)=C(O)/C=C/[C@H]4[C@@]5(C(=O)C(=C(O)/C=C/C=C/C)[C@H]([C@@H]4C)[C@@](C5=O)(O)C)C)C)=C(O)/C=C/C=C/C', "
               "'Pyranose form (6-membered ring)'), "
               "('O1C(O)([C@@H](O)[C@H](O)C1)CO', 'Pyranose form (6-membered "
               "ring)'), "
               "('O=C1C(=C(O)C(=C(O)C=CC=CCO)[C@H]2[C@@]1(O[C@@]3(O)[C@@](O)(CC(C([C@@]23C)=O)C(=O)CCC=CCO)C)C)C', "
               "'Pyranose form (6-membered ring)'), "
               "('OC[C@@H]1O[C@](O)(CO)[C@@H](O)[C@@H]1O', 'Pyranose form "
               "(6-membered ring)'), "
               "('O[C@@H]([C@H](O)[C@H](O)CO)[C@@H](O)[C@@H](O)C=O', "
               "'Open-chain aldose'), "
               "('O1[C@]2([C@@H](O)C[C@]1(O)C(C[C@]3(OC(=O)C([C@]3([C@H](OC(=O)/C(/C)=C\\\\C)C2)[H])=C)[H])CO)C', "
               "'Pyranose form (6-membered ring)')]\n"
               "False negatives: [('C[C@@H]1OC(O)[C@H](O)[C@H](O)[C@H]1O', "
               "'Must have either aldehyde group or hemiacetal ring'), "
               "('OC[C@@H]1OC(O)[C@@H](O)[C@H](O)[C@@H]1O', 'Must have either "
               "aldehyde group or hemiacetal ring'), "
               "('OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O', 'Must have "
               "either aldehyde group or hemiacetal ring'), "
               "('C[C@H]1O[C@H](O)[C@@H](O)[C@@H](O)[C@@H]1O', 'Must have "
               "either aldehyde group or hemiacetal ring'), "
               "('C[C@@H]1O[C@@H](O)[C@@H](O)[C@H](O)[C@@H]1O', 'Must have "
               "either aldehyde group or hemiacetal ring'), "
               "('[C@H]1([C@@H]([C@@H](CC(O1)O)O)O)CO', 'Must have either "
               "aldehyde group or hemiacetal ring'), "
               "('C[C@@H]1O[C@@H](O)[C@H](O)C[C@H]1O', 'Must have either "
               "aldehyde group or hemiacetal ring'), "
               "('OC[C@H]1O[C@@H](O)[C@H](O)[C@H](O)[C@@H]1O', 'Must have "
               "either aldehyde group or hemiacetal ring'), "
               "('[C@@H]1(O)[C@H](O)[C@@H](O)[C@H](O)[C@@H](O1)CO', 'Must have "
               "either aldehyde group or hemiacetal ring'), "
               "('[H][C@]1(O[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)CO', 'Must have "
               "either aldehyde group or hemiacetal ring'), "
               "('O1[C@H]([C@H](O)[C@H](O)[C@H]1O)[C@H](O)CO', 'Must have "
               "either aldehyde group or hemiacetal ring'), "
               "('OC[C@@H]1O[C@@H](O)[C@@H](O)[C@H]1O', 'Must have either "
               "aldehyde group or hemiacetal ring'), "
               "('C1([C@H]([C@@H]([C@H]([C@H](O1)CO)O)O)O)O', 'Must have "
               "either aldehyde group or hemiacetal ring'), "
               "('O1[C@H]([C@H](O)[C@@H](O)[C@H]1O)[C@H](O)C', 'Must have "
               "either aldehyde group or hemiacetal ring'), "
               "('OC[C@@H]1O[C@H](O)[C@H](O)[C@H]1O', 'Must have either "
               "aldehyde group or hemiacetal ring'), "
               "('[H][C@]1(O[C@H](O)[C@@H](O)[C@H]1O)[C@@H](O)CO', 'Must have "
               "either aldehyde group or hemiacetal ring'), "
               "('O1[C@H]([C@@H](O)[C@@H](O)[C@@H](O)[C@H]1O)C', 'Must have "
               "either aldehyde group or hemiacetal ring'), "
               "('[C@@H]1(O)[C@H](O)[C@@H](O)[C@](OC1O)([C@H](O)CO)[H]', 'Must "
               "have either aldehyde group or hemiacetal ring'), "
               "('O1[C@@H]([C@H]([C@@H]([C@@H]1O)O)O)CO', 'Must have either "
               "aldehyde group or hemiacetal ring'), "
               "('O1[C@@H]([C@@H](O)[C@H](O)C1O)[C@H](O)CO', 'Must have either "
               "aldehyde group or hemiacetal ring')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 21,
    'num_false_positives': 100,
    'num_true_negatives': 43510,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.17355371900826447,
    'recall': 0.9130434782608695,
    'f1': 0.2916666666666667,
    'accuracy': 0.9976623198038183}