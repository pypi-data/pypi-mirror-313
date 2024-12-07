"""
Classifies: CHEBI:17761 ceramide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_ceramide(smiles: str):
    """
    Determines if a molecule is a ceramide based on its structure.
    
    Ceramides are N-acyl-sphingoid bases with:
    - Long chain base (sphingoid base) with 2-amino-1,3-diol group
    - N-acyl group (fatty acid) linked via amide bond
    - Usually 14-26 carbon fatty acid chain
    - May have hydroxyl group on C2 of fatty acid
    
    Args:
        smiles (str): SMILES string of molecule
        
    Returns:
        bool: True if molecule is a ceramide, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for required substructures
    # 1. Amide group
    amide_pattern = Chem.MolFromSmarts('[NX3][CX3](=[OX1])')
    if not mol.HasSubstructMatch(amide_pattern):
        return False, "No amide group found"
        
    # 2. Sphingoid base patterns
    sphingoid_patterns = [
        # Basic sphingoid base pattern with more flexibility
        '[OX2][CX4][CX4]([NX3])[CX4][OX2]',
        # Pattern with double bond
        '[OX2][CX4][CX4]([NX3])[CX3]=[CX3]',
        # Pattern for phytosphingosine
        '[OX2][CX4][CX4]([NX3])[CX4][CX4][OX2]',
        # Pattern allowing for phosphate/other modifications
        '[OX2,PX4][CX4][CX4]([NX3])[CX4][OX2]'
    ]
    
    found_sphingoid = False
    for pattern in sphingoid_patterns:
        if mol.HasSubstructMatch(Chem.MolFromSmarts(pattern)):
            found_sphingoid = True
            break
            
    if not found_sphingoid:
        return False, "No sphingoid base pattern found"
        
    # 3. Check for minimum carbon chain length
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 12:  # Adjusted threshold for minimum ceramide size
        return False, "Carbon chain too short for ceramide"
        
    # Check for glycosylation
    glycosyl_patterns = [
        # Pyranose ring pattern
        '[OX2][CH1]1[OH1,OX2][CH1][CH1][CH1][CH1]1',
        # More general glycosidic linkage pattern
        '[OX2]([CH1]1[OH1,OX2][CH1][CH1][CH1][CH1]1)[CH1]'
    ]
    
    is_glycosylated = any(mol.HasSubstructMatch(Chem.MolFromSmarts(pattern)) 
                         for pattern in glycosyl_patterns)
    
    # Check for 2-hydroxy fatty acid
    fatty_acid_c2_oh = Chem.MolFromSmarts('[CX4]-[CX3](=O)-[NX3]-[CX4]-[CX4]-[OX2]')
    has_c2_oh = mol.HasSubstructMatch(fatty_acid_c2_oh)
    
    # Check for phosphate group
    phosphate_pattern = Chem.MolFromSmarts('[PX4](=[OX1])([OX2])[OX2]')
    has_phosphate = mol.HasSubstructMatch(phosphate_pattern)
    
    # Classify based on modifications
    if is_glycosylated:
        return True, "Glycosylated ceramide"
    elif has_phosphate:
        return True, "Ceramide phosphate"
    elif has_c2_oh:
        return True, "Ceramide with 2-hydroxy fatty acid"
    else:
        return True, "Non-glycosylated ceramide"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17761',
                          'name': 'ceramide',
                          'definition': 'Ceramides (N-acyl-sphingoid bases) '
                                        'are a major subclass of sphingoid '
                                        'base derivatives with an amide-linked '
                                        'fatty acid. The fatty acids are '
                                        'typically saturated or '
                                        'monounsaturated with chain lengths '
                                        'from 14 to 26 carbon atoms; the '
                                        'presence of a hydroxyl group on '
                                        'carbon 2 is fairly common. Ceramides '
                                        'are generally precursors of more '
                                        'complex sphingolipids. In the '
                                        'illustrated generalised structure, '
                                        'R(1) = OH, OX (where X = acyl, '
                                        'glycosyl, phosphate, phosphonate, '
                                        'etc.), or H.',
                          'parents': ['CHEBI:26739', 'CHEBI:37622']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.7469879518072288 is too low.\n'
               'True positives: '
               "[('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O)O[C@@H]4O[C@H]([C@H]([C@H]([C@@H]4O)O)O)C)O)NC(C)=O)O)O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)O)NC(C)=O)O)O[C@H]8[C@@H]([C@H]([C@@H](O[C@@H]8CO)O[C@@H]9[C@H]([C@@H](O[C@@H]([C@@H]9O)CO)O[C@H]%10[C@@H]([C@H]([C@@H](O[C@@H]%10CO)OC[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(C)=O)O', "
               "'Glycosylated ceramide'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)NC(=O)C)O[C@@H]2[C@H]([C@@H](O[C@@H]([C@@H]2O)CO)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO)O[C@H]5[C@@H]([C@H]([C@@H](O[C@@H]5CO)OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)O)O)O)NC(=O)C)O)O[C@H]6[C@H]([C@@H]([C@@H]([C@@H](O6)C)O)O)O', "
               "'Glycosylated ceramide'), "
               "('C(O[C@]1(O[C@@]([C@@H]([C@H](C1)O)NC(C)=O)([H])[C@@H]([C@@H](CO)O)O)C(=O)[O-])[C@H]2O[C@H]([C@@H]([C@H]([C@H]2O)O)O)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O)O)O)NC(C)=O)O[C@H]7[C@@H]([C@H]([C@@H](O[C@@H]7CO)OC[C@@H]([C@@H](*)O)NC(=O)*)O)O)O)NC(C)=O)O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP(O)(O)=O)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'Non-glycosylated ceramide'), "
               "('O([C@@H]1[C@H](O[C@@H](OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)[C@@H]([C@H]1O)O)CO)[C@@H]2O[C@@H]([C@@H]([C@@H]([C@H]2O)O[C@H]3O[C@@H]([C@@H]([C@@H]([C@H]3O)O[C@H]4[C@@H]([C@H]([C@H]([C@@H](CO)O4)O)O)NC(C)=O)O)CO)O)CO', "
               "'Glycosylated ceramide'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)O)O[C@H]5[C@H]([C@@H]([C@@H]([C@@H](O5)C)O)O)O)O)NC(C)=O)O)O[C@H]6[C@@H]([C@H]([C@@H]([C@H](O6)CO)O[C@H]7[C@@H]([C@H]([C@H]([C@H](O7)CO)O)O[C@]8(O[C@]([C@@H]([C@H](C8)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)O)NC(C)=O)O)O[C@H]9[C@@H]([C@H]([C@@H](O[C@@H]9CO)O[C@@H]%10[C@H]([C@@H](O[C@@H]([C@@H]%10O)CO)O[C@H]%11[C@@H]([C@H]([C@@H](O[C@@H]%11CO)OC[C@@H]([C@@H](*)O)NC(=O)*)O)O)O)NC(C)=O)O', "
               "'Glycosylated ceramide'), "
               "('C(CCCCCCCCCC)CC\\\\C=C\\\\[C@@H](O)[C@@H](NC(=O)*CO)CO', "
               "'Non-glycosylated ceramide'), "
               "('[H][C@]1(O[C@@](C[C@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2NC(C)=O)[C@H]1NC(C)=O)(O[C@H]1[C@@H](O)[C@@H](CO)O[C@@H](O[C@H]2[C@H](O)[C@@H](O)[C@H](OC[C@H](NC([*])=O)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC)O[C@@H]2CO)[C@@H]1O)C(O)=O)[C@H](O)[C@H](O)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@H](O[C@@H](OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(*)=O)[C@@H]([C@H]1O)O)CO)[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O[C@H]5[C@@H]([C@H]([C@H]([C@H](O5)CO)O)O[C@@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O)O)O[C@@H]7O[C@H]([C@H]([C@H]([C@@H]7O)O)O)C)NC(=O)C)O)O', "
               "'Glycosylated ceramide'), "
               "('[C@]1(C[C@@H]([C@H](C(O1)[C@@H]([C@@H](CO)O)O)NC(=O)C)O)(C(=O)O)O[C@@H]([C@@H](O)C2O[C@@](C[C@@H]([C@H]2NC(=O)C)O)(O[C@@H]3[C@H]([C@@H](O[C@@H]([C@@H]3O)CO)O[C@H]4[C@@H]([C@H]([C@@H](O[C@@H]4CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)CCCCCCCCCCCCCCC)O)O)O)C(=O)O)CO', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)C(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)\\\\C=C\\\\CC\\\\C=C(/C)CCCCC', "
               "'Glycosylated ceramide'), "
               "('[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)CCCCCCCCCCCCCCCCC)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O[C@H]5[C@@H]([C@@H](O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@H](O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)O)CO)O)[H])C(O)=O)[C@H]([C@H](O5)CO)O)O)NC(C)=O)(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O[C@]8(O[C@]([C@@H]([C@H](C8)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(O)=O)CO)O)[H])C(O)=O', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1[C@H]([C@H](O[C@H]([C@@H]1O)O[C@@H]2[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]2O)O)CO)CO)O)[C@@H]3[C@@H]([C@H]([C@H](O)[C@H](O3)CO)O[C@@H]4O[C@@H]([C@@H]([C@@H]([C@H]4O)O[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(O)=O)O[C@H]6[C@@H]([C@H]([C@@H](O)[C@H](O6)CO)O)NC(=O)C)CO)NC(C)=O', "
               "'Glycosylated ceramide'), "
               "('CC(C)CCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Glycosylated ceramide'), "
               "('CC(C)CCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O[C@H]3O[C@H](CO)[C@H](O)[C@H](O[C@@H]4O[C@H](CO)[C@@H](O)[C@H](O[C@@H]5O[C@H](CO)[C@H](O)[C@H](O)[C@H]5O[C@@H]5O[C@@H](C)[C@@H](O)[C@@H](O)[C@@H]5O)[C@H]4NC(C)=O)[C@H]3O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@@H]([C@H]([C@H]([C@H](O1)CO)OCCCC=2C=CC(=CC2)C)O)O)C[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(CCCCCCCCCCCCCCCCCCCCCCCCC)=O', "
               "'Glycosylated ceramide'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)O[C@@H]2O[C@H]([C@H]([C@H]([C@@H]2O)O)O)C)O[C@H]3[C@@H]([C@@H](NC(C)=O)[C@H](OC[C@H]4O[C@H]([C@@H]([C@@H](O[C@@H]5O[C@H](CO)[C@H]([C@@H]([C@H]5NC(C)=O)O)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O)O[C@@H]7O[C@H]([C@H]([C@H]([C@@H]7O)O)O)C)[C@H]4O)O)O[C@H]8[C@@H]([C@@H](NC(C)=O)[C@H](O[C@@H]9[C@H]([C@H](O[C@H]%10[C@@H]([C@H]([C@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(*)=O)O[C@@H]%10CO)O)O)O[C@@H]([C@@H]9O)CO)O)O[C@@H]8CO)O)O[C@@H]3CO)O', "
               "'Glycosylated ceramide'), "
               "('CC(C)CCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Glycosylated ceramide'), "
               "('[C@H]1(O[C@@H]([C@H](O)[C@@H]([C@H]1O)O[C@@H]2O[C@H](CO)[C@H]([C@@H]([C@H]2NC(=O)C)O)O[C@@H]3O[C@@H]([C@H](O)[C@@H]([C@H]3O[C@@H]4O[C@H]([C@H]([C@H]([C@@H]4O)O)O)C)O)CO)CO)O[C@H]5[C@@H]([C@@H](NC(=O)C)[C@H](O[C@@H]6[C@H]([C@H](O[C@H]7[C@@H]([C@H]([C@H](OC[C@@H]([C@@H](*)O)NC(*)=O)O[C@@H]7CO)O)O)O[C@@H]([C@@H]6O)CO)O)O[C@@H]5CO)O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(C)=O)[C@@H]([C@H]1O)O)CO)[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)O)NC(C)=O)O[C@@]5(C[C@@H]([C@H]([C@@](O5)([C@@H]([C@@H](CO)O)O)[H])NC(C)=O)O)C(=O)O)O', "
               "'Glycosylated ceramide'), "
               "('O1[C@@H]([C@@H](O)C(O)C(O)[C@@H]1OC[C@H](NC(=O)[C@H](O)CCCCCCCCCCCCCCC)[C@H](O)/C=C/CC/C=C\\\\CCCCCCCCC)CO', "
               "'Glycosylated ceramide'), "
               "('CC(C)CCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Glycosylated ceramide'), "
               "('CC(C)CCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@H]([C@@H](O[C@@H]([C@@H]1O)CO)O[C@H]2[C@@H]([C@H]([C@@H](O[C@@H]2CO)O[C@@H]3[C@H]([C@@H](O[C@@H]([C@@H]3O)CO)O[C@H]4[C@@H]([C@H]([C@@H](O[C@@H]4CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(=O)C)O[C@H]5[C@H]([C@@H]([C@@H]([C@@H](O5)C)O)O)O)O[C@H]6[C@H]([C@@H]([C@@H]([C@@H](O6)C)O)O)O)[C@@H]7[C@@H]([C@H]([C@H]([C@H](O7)CO)O)O)O', "
               "'Glycosylated ceramide'), "
               "('[C@]([C@@](/C=C/CCCCCCCCCCCCC)(O)[H])(NC(=O)CCCCCCCCCCCCCCCCCC)([H])CO', "
               "'Ceramide with 2-hydroxy fatty acid'), "
               "('O=C(N[C@H]([C@H](O)/C=C/CCC(O)C(CCCCCCCCC)C)CO[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)[C@H](O)CCCCCCCCCCCCCC', "
               "'Glycosylated ceramide'), "
               "('[H][C@@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1[C@@H](O)[C@@H](O)[C@@H](CO)O[C@H]1OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](OC[C@H](NC(=O)[C@H](O)CCCCCCCCCCCCCCCCCCCCCC)[C@H](O)[C@H](O)CCCCCCCCCCCCCC)[C@H](O)[C@@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@H]1O', "
               "'Glycosylated ceramide'), "
               "('[H][C@]1(O[C@@](C[C@H](O)[C@H]1NC(C)=O)(O[C@H]1[C@@H](O)[C@@H](CO)O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(C)=O)[C@@H](O[C@@H]2CO)O[C@H]2[C@@H](O)[C@@H](CO[C@@H]3O[C@H](CO)[C@@H](O[C@@H]4O[C@H](CO)[C@H](O)[C@H](O)[C@H]4O)[C@H](O)[C@H]3NC(C)=O)O[C@@H](O[C@H]3[C@H](O)[C@@H](NC(C)=O)[C@@H](O[C@@H]3CO)O[C@H]3[C@@H](O)[C@@H](CO)O[C@@H](O[C@H]4[C@H](O)[C@@H](O)[C@H](OC[C@H](NC([*])=O)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC)O[C@@H]4CO)[C@@H]3O)[C@@H]2O)[C@@H]1O)C(O)=O)[C@H](O)[C@H](O)CO', "
               "'Glycosylated ceramide'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)NC(C)=O)O[C@H]5[C@H]([C@@H]([C@@H]([C@@H](O5)C)O)O)O)O)NC(C)=O)O)O[C@H]6[C@@H]([C@H]([C@@H]([C@H](O6)CO)O[C@H]7[C@@H]([C@H]([C@H]([C@H](O7)CO)O)O[C@]8(O[C@]([C@@H]([C@H](C8)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)O)NC(C)=O)O)O[C@H]9[C@@H]([C@H]([C@@H](O[C@@H]9CO)O[C@@H]%10[C@H]([C@@H](O[C@@H]([C@@H]%10O)CO)O[C@H]%11[C@@H]([C@H]([C@@H](O[C@@H]%11CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(C)=O)O', "
               "'Glycosylated ceramide'), "
               "('[H][C@]1(O[C@@](C[C@H](O)[C@H]1NC(C)=O)(O[C@H]1[C@@H](O)[C@@H](CO)O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(C)=O)[C@@H](O[C@@H]2CO)O[C@H]2[C@@H](O)[C@@H](CO)O[C@@H](O[C@H]3[C@H](O)[C@@H](O)[C@H](OC[C@H](NC([*])=O)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC)O[C@@H]3CO)[C@@H]2O)[C@@H]1O)C(O)=O)[C@H](O)[C@H](O)CO', "
               "'Glycosylated ceramide'), "
               "('O[C@@H]1[C@H]([C@@H](O[C@@H]([C@H]1O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)O)NC(=O)C)O)O[C@H]8[C@H]([C@@H]([C@@H]([C@@H](O8)C)O)O)O)NC(=O)C)O)CO)O[C@@H]9[C@H]([C@@H](O[C@@H]([C@@H]9O)CO)O[C@H]%10[C@@H]([C@H]([C@@H](O[C@@H]%10CO)O[C@@H]%11[C@H]([C@@H](O[C@@H]([C@@H]%11O)CO)O[C@H]%12[C@@H]([C@H]([C@@H](O[C@@H]%12CO)OC[C@@H]([C@@H](*)O)NC(=O)*)O)O)O)NC(=O)C)O)O)NC(=O)C', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCCCCCCCCCC[C@@H](O)[C@H](O)C(=O)N[C@@H](CO)[C@H](O)[C@H](O)CCCCCCCCCCCCCC', "
               "'Non-glycosylated ceramide'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O[C@@H]3O[C@H](CO)[C@@H](O[C@@H]4O[C@H](CO[C@@H]5O[C@H](CO)[C@@H](O[C@@H]6O[C@H](CO)[C@H](O)[C@H](O[C@H]7O[C@H](CO)[C@H](O)[C@H](O)[C@H]7NC(C)=O)[C@H]6O[C@@H]6O[C@@H](C)[C@@H](O)[C@@H](O)[C@@H]6O)[C@H](O)[C@H]5NC(C)=O)[C@H](O)[C@H](O[C@@H]5O[C@H](CO)[C@@H](O[C@@H]6O[C@H](CO)[C@H](O)[C@H](O[C@H]7O[C@H](CO)[C@H](O)[C@H](O)[C@H]7NC(C)=O)[C@H]6O[C@@H]6O[C@@H](C)[C@@H](O)[C@@H](O)[C@@H]6O)[C@H](O)[C@H]5NC(C)=O)[C@H]4O)[C@H](O)[C@H]3NC(C)=O)[C@H]2O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Glycosylated ceramide'), "
               "('O[C@@H]1[C@H]([C@@H](O[C@@H]([C@H]1O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O[C@@H]4O[C@@H]([C@@H]([C@@H]([C@H]4O)O[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)O)NC(=O)C)O)CO)O[C@@H]6[C@H]([C@@H](O[C@@H]([C@@H]6O)CO)O[C@H]7[C@@H]([C@H]([C@@H](O[C@@H]7CO)O[C@@H]8[C@H]([C@@H](O[C@@H]([C@@H]8O)CO)O[C@H]9[C@@H]([C@H]([C@@H](O[C@@H]9CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(=O)C)O)O)NC(=O)C', "
               "'Glycosylated ceramide'), "
               "('O[C@H]1[C@H]([C@H](O[C@H]([C@@H]1O)O[C@@H]2[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]2O)O)CO)CO)O[C@H]3[C@@H]([C@H]([C@@H](O)[C@H](O3)CO)O[C@H]4[C@@H]([C@@H](O[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@H](O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)O)CO)O)[H])C(O)=O)[C@H]([C@H](O4)CO)O)O)NC(C)=O', "
               "'Glycosylated ceramide'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)NC(=O)C)O[C@@H]2[C@H]([C@@H](O[C@@H]([C@@H]2O)CO)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO)O[C@H]5[C@@H]([C@H]([C@@H](O[C@@H]5CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(=O)C)O)O', "
               "'Glycosylated ceramide'), "
               "('[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O[C@@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O)O)O)O)O)O)OC[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)NC(=O)*', "
               "'Glycosylated ceramide'), "
               "('[C@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O)NC(=O)C)O[C@@H]2[C@@H]([C@H]([C@@H](O[C@@H]2CO)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3COP(=O)(OCCN)O)O[C@@H]4[C@@H]([C@@H](O[C@@H]([C@H]4O)CO)O[C@H]5[C@@H]([C@H]([C@@H](O[C@@H]5CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(=O)C)O)NC(=O)C)O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO)NC([*])=O', "
               "'Non-glycosylated ceramide'), "
               "('O[C@H]1[C@H](O[C@@H](OC[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)NC(=O)CCCCCCCCCCCCCCCCC)[C@@H]([C@H]1O)O)CO', "
               "'Glycosylated ceramide'), "
               "('C(O[C@]1(O[C@@]([C@@H]([C@H](C1)O)NC(C)=O)([H])[C@@H]([C@@H](CO)O)O)C(=O)[O-])[C@H]2O[C@H]([C@@H]([C@H]([C@H]2O)O)O)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O)O)O)NC(C)=O)O[C@H]7[C@@H]([C@H]([C@@H](O[C@@H]7CO)O[C@@H]8[C@H]([C@@H](O[C@@H]([C@@H]8O)CO)O[C@H]9[C@@H]([C@H]([C@@H](O[C@@H]9CO)OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)O)O)O)NC(C)=O)O)O)NC(C)=O)O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O)[C@H]3NC(C)=O)[C@H]2O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](COC1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Glycosylated ceramide'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O[C@H]5[C@@H]([C@H]([C@H]([C@H](O5)CO)O)O[C@@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O)NC(C)=O)O[C@H]7[C@H]([C@@H]([C@@H]([C@@H](O7)C)O)O)O)O[C@H]8[C@H]([C@@H]([C@@H]([C@@H](O8)C)O)O)O)NC(C)=O)O)O)NC(C)=O)O)O[C@H]9[C@@H]([C@H]([C@@H]([C@H](O9)CO)O[C@H]%10[C@@H]([C@H]([C@H]([C@H](O%10)CO)O)O[C@]%11(O[C@]([C@@H]([C@H](C%11)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)O)NC(C)=O)O)O[C@H]%12[C@@H]([C@H]([C@@H](O[C@@H]%12CO)O[C@@H]%13[C@H]([C@@H](O[C@@H]([C@@H]%13O)CO)O[C@H]%14[C@@H]([C@H]([C@@H](O[C@@H]%14CO)OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)O)O)O)NC(C)=O)O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O[C@@H]4O[C@H](CO)[C@H](O)[C@H](O[C@H]5O[C@H](CO)[C@H](O)[C@H](O)[C@H]5O)[C@H]4O[C@@H]4O[C@@H](C)[C@@H](O)[C@@H](O)[C@@H]4O)[C@H]3NC(C)=O)[C@H]2O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Glycosylated ceramide'), "
               "('CC(C)CCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Glycosylated ceramide'), "
               "('[C@]1(O[C@]([C@@H]([C@H](C1)O)NC(C)=O)([C@@H]([C@H](O)CO)O)[H])(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H]([C@H](O[C@@H]4[C@H](O[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@H](O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@@H](CO)O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)O)O)[H])C(=O)O)CO)O)[H])C(O)=O)[C@H]([C@H](O[C@@H]8[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]8O)O)CO)O[C@@H]4CO)O)O[C@H](CO[C@]9(O[C@]([C@@H]([C@H](C9)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)O)[C@@H]3O)NC(C)=O)CO)O)C(O)=O', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@H]([C@@H](O[C@@H]([C@@H]1O)CO)O[C@H]2[C@@H]([C@H]([C@@H](O[C@@H]2CO)O[C@@H]3[C@H]([C@@H](O[C@@H]([C@@H]3O)CO)O[C@H]4[C@@H]([C@H]([C@@H](O[C@@H]4CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(C)=O)O)O)[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O[C@@H]7[C@@H]([C@H]([C@H]([C@H](O7)CO)O)O)O)O[C@@H]8O[C@H]([C@H]([C@H]([C@@H]8O)O)O)C)O)NC(C)=O', "
               "'Glycosylated ceramide'), "
               "('O=C(N[C@H]([C@H](O)/C=C/CC/C=C\\\\CCCCCCCCC)CO[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)[C@H](O)/C=C/CCCCCCCCCCCCCC', "
               "'Glycosylated ceramide'), "
               "('O=C(N[C@H]([C@H](O)/C=C/CC/C=C(/CCCCCCCCC)\\\\C)CO)CCCCCCCCCCCCCCC', "
               "'Ceramide with 2-hydroxy fatty acid'), "
               "('[C@@]1(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O)CO)O)[H])(C(O)=O)O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)CCCCCCCC=CCCCCCCCC)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O)NC(C)=O', "
               "'Glycosylated ceramide'), "
               "('C(CCCCCC(CC)C)CCCC[C@@H](O)[C@@H](NC(CCCCCCCCCCCCCCCCCCCCCCCCC)=O)CO', "
               "'Ceramide with 2-hydroxy fatty acid'), "
               "('CCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O)[C@H]3NC(C)=O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@@H](CO)O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C(O)=O)C(O)=O)[C@H]2O)[C@H](O)[C@H]1O)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'Glycosylated ceramide'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O[C@H]5[C@@H]([C@H]([C@H]([C@H](O5)CO)O)O[C@@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O)O)O[C@H]7[C@H]([C@@H]([C@@H]([C@@H](O7)C)O)O)O)O)NC(=O)C)O)O[C@H]8[C@@H]([C@H]([C@@H]([C@H](O8)CO)O[C@H]9[C@@H]([C@H]([C@H]([C@H](O9)CO)O)O[C@H]%10[C@@H]([C@H]([C@@H]([C@H](O%10)CO)O[C@H]%11[C@@H]([C@H]([C@H]([C@H](O%11)CO)O)O[C@@H]%12[C@@H]([C@H]([C@H]([C@H](O%12)CO)O)O)O)O[C@H]%13[C@H]([C@@H]([C@@H]([C@@H](O%13)C)O)O)O)O)NC(=O)C)O)O)NC(=O)C)O)O)NC(=O)C)O)O[C@H]%14[C@@H]([C@H]([C@@H](O[C@@H]%14CO)OC[C@@H]([C@@H](*)O)NC(=O)*)O)O', "
               "'Glycosylated ceramide'), "
               "('[C@H]1(O[C@@H]([C@H](O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O)NC(C)=O)[C@@H]([C@H]1O)O[C@]3(O[C@]([C@@H]([C@H](C3)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)CO)O[C@@H]4[C@H]([C@H](O[C@@H]5[C@H]([C@H](O[C@@H]6[C@H](O[C@@H](OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)[C@@H]([C@H]6O)O)CO)O[C@@H]([C@@H]5O)CO)O)O[C@H](CO)[C@H]4O)NC(C)=O', "
               "'Glycosylated ceramide'), "
               "('[C@@H]1([C@H](O[C@@H](O[C@@H]2[C@H]([C@@H](O[C@H]3[C@H](O[C@@H](O[C@@H]4[C@H](O[C@@H](OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)[C@@H]([C@H]4O)O)CO)[C@@H]([C@H]3O)O)CO)O[C@@H]([C@@H]2O[C@@H]5O[C@@H]([C@H](O)[C@@H]([C@H]5NC(C)=O)O[C@H]6[C@@H]([C@H]([C@@H](O)[C@H](O6)CO)O)O)CO)CO)O)[C@@H]([C@H]1O[C@@H]7[C@@H]([C@H]([C@@H](O)[C@H](O7)CO)O)NC(C)=O)NC(C)=O)CO)O', "
               "'Glycosylated ceramide'), "
               "('[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O[C@@H]6O[C@@H]([C@@H]([C@@H]([C@H]6O)O)O)CO)NC(C)=O)(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)CO)O)[H])C([O-])=O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCC\\\\C(C)=C\\\\CC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Glycosylated ceramide'), "
               "('[C@@]1(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O)CO)O)[H])(C(OC)=O)O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)CCCCCCCCCCCCCCCCC)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O)NC(C)=O', "
               "'Glycosylated ceramide'), "
               "('C([C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(*)=O)O[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)O)NC(C)=O)O[C@@]5(C[C@@H]([C@H]([C@@](O5)([C@@H]([C@@H](CO)O)O)[H])NC(CO)=O)O)C([O-])=O)O)O)O', "
               "'Glycosylated ceramide'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)O)O)O)NC(C)=O)O)O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(CO)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)O)NC(C)=O)O)O[C@H]8[C@@H]([C@H]([C@@H](O[C@@H]8CO)O[C@@H]9[C@H]([C@@H](O[C@@H]([C@@H]9O)CO)O[C@H]%10[C@@H]([C@H]([C@@H](O[C@@H]%10CO)OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)O)O)O)NC(C)=O)O', "
               "'Glycosylated ceramide'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)O)O)O)NC(C)=O)O)O[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(CO)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)O)NC(C)=O)O)O[C@H]8[C@@H]([C@H]([C@@H](O[C@@H]8CO)O[C@@H]9[C@H]([C@@H](O[C@@H]([C@@H]9O)CO)O[C@H]%10[C@@H]([C@H]([C@@H](O[C@@H]%10CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(C)=O)O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCC', "
               "'Ceramide with 2-hydroxy fatty acid'), "
               "('[C@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)(NC(=O)*)CO[C@@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@H](O[C@@H]3[C@@H]([C@@H](O[C@H]4[C@@H]([C@H]([C@@H](O[C@@H]5[C@@H]([C@@H](O[C@H]6[C@@H]([C@H]([C@@H](O)[C@H](O6)CO)O)NC(C)=O)[C@H]([C@@H](CO)O5)O)O)[C@H](O4)CO)O)NC(C)=O)[C@H]([C@@H](CO)O3)O)O)[C@@H]([C@H]2O)O)CO)[C@@H]([C@H]1O)O)CO', "
               "'Glycosylated ceramide'), "
               "('[C@H]1(O[C@@H]([C@@H]([C@@H]([C@H]1O)O[C@]2(O[C@]([C@@H]([C@H](C2)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO)O[C@H]5[C@@H]([C@H]([C@@H](O[C@@H]5CO)O[C@@H]6[C@H]([C@@H](O[C@@H]([C@@H]6O)CO)O[C@H]7[C@@H]([C@H]([C@@H](O[C@@H]7CO)OC[C@@H]([C@@H](*)O)NC(=O)*)O)O)O)NC(C)=O)O)O)NC(=O)C)O', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@H](O)[C@@H](O)[C@@H](O[C@@H]1CO)OCC(NC(=O)CCCCCCCCCCCCCCC)C(O)/C=C\\\\CCCCCCCCCCCCC)[C@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@H]([C@H](O[C@@H]2[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]2O)O)CO)O[C@@H]([C@@H]1O)CO)O)[C@]3(O[C@]([C@@H]([C@H](C3)O)NC(C)=O)([C@@H]([C@H](O[C@]4(O[C@]([C@@H]([C@H](C4)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)O)CO)O)[H])C(O)=O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C', "
               "'Non-glycosylated ceramide'), "
               "('O[C@H]1[C@H]([C@H](O[C@H]([C@@H]1O)O[C@@H]2[C@H](O[C@@H](OC[C@@H]([C@@H](*)O)NC(=O)*)[C@@H]([C@H]2O)O)CO)CO)O[C@H]3[C@@H]([C@H]([C@@H](O)[C@H](O3)CO)O[C@@H]4O[C@@H]([C@@H]([C@@H]([C@H]4O)O[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O[C@H]6[C@@H]([C@H]([C@@H](O)[C@H](O6)CO)O)NC(C)=O)CO)NC(C)=O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](COP(O)(O)=O)NC(=O)CCCCC', "
               "'Non-glycosylated ceramide'), "
               "('[C@H]1(O[C@@H]([C@@H]([C@@H]([C@H]1O)O)O)CO)O[C@H]2[C@@H]([C@H]([C@@H](O[C@@H]2CO)O[C@@H]3[C@H]([C@@H](O[C@@H]([C@@H]3O)CO)O[C@H]4[C@@H]([C@H]([C@@H](O[C@@H]4CO)O[C@@H]5[C@H]([C@@H](O[C@@H]([C@@H]5O)CO)O[C@H]6[C@@H]([C@H]([C@@H](O[C@@H]6CO)OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)O)O)O)NC(C)=O)O)O)NC(=O)C)O', "
               "'Glycosylated ceramide'), "
               "('O[C@H](CCCCCCCCCCCCCCC)[C@@H](NC(=O)CCCCCCCCCCCCCCCCCCCCCCCC)CO', "
               "'Ceramide with 2-hydroxy fatty acid'), "
               "('O=C(N[C@H]([C@H](O)[C@H](O)CCCCCCCCCCCCCCCC)CO)[C@@H](O)CCCCCCCCCCCCCCCCCCCC', "
               "'Non-glycosylated ceramide'), "
               "('O([C@@H]1[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]1O)O)CO)[C@@H]2O[C@@H]([C@@H]([C@@H]([C@H]2O)O[C@H]3O[C@@H]([C@@H]([C@@H]([C@H]3O)O[C@H]4[C@@H]([C@H]([C@H]([C@@H](CO)O4)O)O[C@@H]5O[C@@H]([C@@H]([C@@H]([C@H]5O)O)O)CO)NC(C)=O)O)CO)O)CO', "
               "'Glycosylated ceramide'), "
               "('C(=C/*)\\\\[C@@H](O)[C@@H](NC(CCCCCCCCCCCCCCCCCCCCCC)=O)CO', "
               "'Ceramide with 2-hydroxy fatty acid'), "
               "('O([C@@H]1[C@@H]([C@H]([C@H]([C@H](O1)CO)OCCC)O)O)C[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(CCCCCCCCCCCCCCCCCCCCCCCCC)=O', "
               "'Glycosylated ceramide'), "
               "('O[C@@H]1[C@H]([C@@H](O[C@@H]([C@H]1O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)O)O[C@H]5[C@H]([C@@H]([C@@H]([C@@H](O5)C)O)O)O)NC(=O)C)O)CO)O[C@@H]6[C@H]([C@@H](O[C@@H]([C@@H]6O)CO)O[C@H]7[C@@H]([C@H]([C@@H](O[C@@H]7CO)O[C@@H]8[C@H]([C@@H](O[C@@H]([C@@H]8O)CO)O[C@H]9[C@@H]([C@H]([C@@H](O[C@@H]9CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(=O)C)O)O)NC(=O)C', "
               "'Glycosylated ceramide'), "
               "('O1[C@@H]([C@@H](O)C(O)C(O)[C@@H]1OC[C@H](NC(=O)[C@H](O)CCCCCCCCCCCCCCCCCCCCCCC)[C@H](O)/C=C/CC/C=C\\\\CCCCCCCCC)CO', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'Ceramide with 2-hydroxy fatty acid'), "
               "('O([C@@H]1[C@@H]([C@H]([C@H]([C@H](O1)CO)OCC=2C=CC(=CC2)C)O)O)C[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(CCCCCCCCCCCCCCCCCCCCCCCCC)=O', "
               "'Glycosylated ceramide'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)C([O-])=O)O)OS(=O)(=O)[O-])O)O)O)NC(C)=O)O)O[C@@H]5[C@H](O[C@H]([C@@H]([C@H]5O)NC(C)=O)O[C@H]6[C@H]([C@H](O[C@@H](O[C@@H]7[C@H](O[C@@H](OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(*)=O)[C@@H]([C@H]7O)O)CO)[C@@H]6O)CO)O)CO', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCCC[C@@H](O)[C@@H](O)[C@H](CO)NC(=O)CCCCCCC', "
               "'Ceramide with 2-hydroxy fatty acid'), "
               "('OC(C(NC(=O)CCCCCCCCCCCCCCC)CO)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'Ceramide with 2-hydroxy fatty acid'), "
               "('CCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)\\\\C=C\\\\CCCCCCCCCC(C)C', "
               "'Non-glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)\\\\C=C\\\\CCCCCCCCCC(C)C', "
               "'Glycosylated ceramide'), "
               "('[C@H]1(O[C@@H]([C@@H]([C@@H]([C@H]1O)O[C@]2(O[C@]([C@@H]([C@H](C2)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@@H]6O[C@@H]([C@@H]([C@@H]([C@H]6O)O)O)CO)O)NC(=O)C)O[C@H]7[C@@H]([C@H]([C@@H](O[C@@H]7CO)O[C@@H]8[C@H]([C@@H](O[C@@H]([C@@H]8O)CO)O[C@H]9[C@@H]([C@H]([C@@H](O[C@@H]9CO)OC[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(C)=O)O)O)NC(=O)C)O', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@H]([C@H](O[C@@H]2[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]2O)O)CO)O[C@@H]([C@@H]1O)CO)O)[C@]3(O[C@]([C@@H]([C@H](C3)O)NC(C)=O)([C@@H]([C@H](O[C@]4(O[C@]([C@@H]([C@H](C4)O)NC(C)=O)([C@@H]([C@@H](COC(=O)C)O)O)[H])C(=O)O)CO)O)[H])C(O)=O', "
               "'Glycosylated ceramide'), "
               "('O[C@@H]([C@@H](NC(=O)CCCCCCC[2H])CO)\\\\C=C\\\\CCCCCCCCCCCCC', "
               "'Ceramide with 2-hydroxy fatty acid'), "
               "('C(O[C@]1(O[C@@]([C@@H]([C@H](C1)O)NC(C)=O)([H])[C@@H]([C@@H](CO)O)O)C(=O)[O-])[C@H]2O[C@H]([C@@H]([C@H]([C@H]2O)O)O)O[C@H]3[C@@H]([C@H]([C@@H](O[C@@H]3CO)O[C@@H]4[C@H]([C@@H](O[C@@H]([C@@H]4O)CO[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O)O)O)NC(C)=O)O[C@H]7[C@@H]([C@H]([C@@H](O[C@@H]7CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(C)=O)O', "
               "'Glycosylated ceramide'), "
               "('O(C[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)NC(=O)*)[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O[C@@H]7[C@@H]([C@H]([C@H]([C@H](O7)CO)O)O)O)O[C@H]8[C@H]([C@@H]([C@@H]([C@@H](O8)C)O)O)O)O)NC(=O)C)O)O[C@H]9[C@@H]([C@H]([C@@H]([C@H](O9)CO)O[C@H]%10[C@@H]([C@H]([C@H]([C@H](O%10)CO)O)O[C@H]%11[C@@H]([C@H]([C@@H]([C@H](O%11)CO)O[C@H]%12[C@@H]([C@H]([C@H]([C@H](O%12)CO)O)O[C@@H]%13[C@@H]([C@H]([C@H]([C@H](O%13)CO)O)O)O)O[C@H]%14[C@H]([C@@H]([C@@H]([C@@H](O%14)C)O)O)O)O)NC(=O)C)O)O)NC(=O)C)O)O)NC(=O)C)O)O)O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCC\\\\C=C\\\\CCC[C@@H](O)[C@@H](O)[C@H](CO)NC([*])=O', "
               "'Non-glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C', "
               "'Ceramide with 2-hydroxy fatty acid'), "
               "('O([C@@H]1[C@H]([C@@H](O[C@@H]([C@H]1O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)O)O[C@H]5[C@H]([C@@H]([C@@H]([C@@H](O5)C)O)O)O)NC(=O)C)O)CO)O[C@@H]6[C@H]([C@@H](O[C@@H]([C@@H]6O)CO)O[C@H]7[C@@H]([C@H]([C@@H](O[C@@H]7CO)O[C@@H]8[C@H]([C@@H](O[C@@H]([C@@H]8O)CO)O[C@H]9[C@@H]([C@H]([C@@H](O[C@@H]9CO)OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)O)O)O)NC(=O)C)O)O)NC(=O)C)[C@H]%10[C@H]([C@@H]([C@@H]([C@@H](O%10)C)O)O)O', "
               "'Glycosylated ceramide'), "
               "('O1C(OC2C(O)C(O)C(OC2CO)OCC(NC(=O)CCCCCCC/C=C/CCCCCCCC)C(O)/C=C/CCCCCCCCCCCCC)C(O)C(O)C(OC3OC(C(O)C(O)C3O)CO)C1CO', "
               "'Glycosylated ceramide'), "
               "('O(C[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO[C@H]5[C@@H]([C@H]([C@@H]([C@H](O5)CO)O[C@H]6[C@@H]([C@H]([C@H]([C@H](O6)CO)O)O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)O)NC(=O)C)O)O[C@H]8[C@@H]([C@H]([C@@H]([C@H](O8)CO)O[C@H]9[C@@H]([C@H]([C@H]([C@H](O9)CO[C@H]%10[C@@H]([C@H]([C@@H]([C@H](O%10)CO)O[C@H]%11[C@@H]([C@H]([C@H]([C@H](O%11)CO)O)O[C@]%12(O[C@]([C@@H]([C@H](C%12)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)O)NC(=O)C)O)O[C@H]%13[C@@H]([C@H]([C@@H]([C@H](O%13)CO)O[C@H]%14[C@@H]([C@H]([C@H]([C@H](O%14)CO)O)O[C@]%15(O[C@]([C@@H]([C@H](C%15)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)O)NC(=O)C)O)O)NC(=O)C)O)O)NC(=O)C)O)O)O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](CO)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C', "
               "'Non-glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C', "
               "'Ceramide with 2-hydroxy fatty acid'), "
               "('CCCCCCCCCCCCCC[C@@H](O)[C@@H](O)[C@H](CO[C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)NC(=O)CCCCCCCCCCCCC', "
               "'Glycosylated ceramide')]\n"
               'False positives: '
               "[('O([C@H]1[C@H](O)[C@@H](NC(=O)C)C(O[C@@H]1CO)OC[C@@H](O)[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)CO)[C@@H](NC(=O)C)CO)[C@@H]4O[C@@H]([C@H](O)[C@H](O[C@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5NC(=O)C)CO)[C@H]4O)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)OC[C@@H](O)[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)[C@@H](NC(=O)C)CO)[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H]3O)CO', "
               "'Glycosylated ceramide'), "
               "('[H][C@]1(O[C@@H]2O[C@@H](C)[C@@H](NO[C@H]3C[C@H](O)[C@H](SC(=O)c4c(C)c(I)c(O[C@@H]5O[C@@H](C)[C@H](O)[C@@H](OC)[C@H]5O)c(OC)c4OC)[C@@H](C)O3)[C@H](O)[C@H]2O[C@H]2C[C@H](OC)[C@H](CO2)NCC)C#C\\\\C=C/C#C[C@]2(O)CC(=O)C(NC(=O)OC)=C1/C2=C\\\\CSSSC', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)[C@H](O[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@H]1NC(=O)C)CO)[C@H]4[C@@H](O)[C@H](O[C@@H](O[C@@H]([C@@H](O)[C@H](O)CO[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)[C@@H](NC(=O)C)CO)[C@@H]4O)CO[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O)CO)[C@H](O[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)[C@H]7NC(=O)C)CO', "
               "'Glycosylated ceramide'), "
               "('O1[C@@H]([C@@H](O)C(O)C(O)[C@@H]1OC[C@H](NC(=O)CCCCCCCCCCCCCCCCCCC)[C@H](O)/C=C/CCCCCCCCCC)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1[C@H](O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)OC[C@@H](O)[C@H](O)[C@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@@H](NC(=O)C)CO)[C@@H]4O[C@@H]([C@H](O)[C@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5NC(=O)C)CO)[C@H]4O)CO', "
               "'Glycosylated ceramide'), "
               "('O1[C@@H]([C@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)[C@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@@H](O)[C@@H]1O[C@@H]([C@@H](O)[C@H](O)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)[C@@H](NC(=O)C)CO)CO', "
               "'Glycosylated ceramide'), "
               "('[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O)NC(C)=O)(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@@H](CO)O)OC(=O)C)[H])C([O-])=O)CO)O)[H])C([O-])=O', "
               "'Glycosylated ceramide'), "
               "('[H][C@]1(O[C@@](C[C@H](O)[C@H]1NC(C)=O)(O[C@@H]1[C@@H](O)[C@@H](O[C@H](CO)[C@@H]1O[C@@H]1O[C@H](CO)[C@H](O)[C@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2O)[C@H]1NC(C)=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](OC[C@H](NC(=O)CCCCCCCCCCCCCCCCC)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC)O[C@@H]1CO)C([O-])=O)[C@H](O)[C@H](O)CO', "
               "'Glycosylated ceramide'), "
               "('[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O[C@@H]5O[C@@H]([C@@H]([C@@H]([C@H]5O)O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O[C@H]7[C@@H]([C@H]([C@@H](O)[C@H](O7)CO)O)NC(C)=O)CO)NC(C)=O)(O[C@]([C@H](NC(=O)CO)[C@H](C1)O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O', "
               "'Glycosylated ceramide'), "
               "('O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O)[C@@H]3O)CO)[C@H](O)[C@@H]1O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)CO[C@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7NC(=O)C)CO)[C@H](O)[C@@H]6O[C@@H]8O[C@@H]([C@@H](O)[C@H](O)[C@H]8NC(=O)C)CO)CO[C@@H]9O[C@@H]([C@@H](O)[C@H](O)[C@H]9NC(=O)C)CO', "
               "'Glycosylated ceramide'), "
               "('O=C(N[C@H]([C@H](O)[C@H](O)CCCCCCCCCCCCCC)CO[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)[C@H](O)CCCCCCCCCCCCCC/C=C\\\\CCCCCC', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@@H](O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)[C@@H](O[C@@H]([C@@H]1O)CO)O[C@@H]([C@@H](O)[C@H](O)CO[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)[C@@H](NC(=O)C)CO)[C@H]4O[C@@H]([C@H](O)[C@H](O[C@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H]4NC(=O)C)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1O[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O)[C@@H]1O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)CO)[C@H]4[C@H](O)[C@H](O[C@@H](O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@H]4O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6NC(=O)C)CO)CO[C@@H]7O[C@@H]([C@@H](O)[C@H](O)[C@H]7NC(=O)C)CO', "
               "'Glycosylated ceramide'), "
               "('S(OC[C@H]1O[C@@H](O[C@@H]2[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]2O)CO)OC[C@@H](O)[C@H](O)[C@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO)[C@@H](NC(=O)C)CO)[C@H](O)[C@@H](O)[C@H]1O)(O)(=O)=O', "
               "'Glycosylated ceramide'), "
               "('O1[C@H]([C@H]([C@H]([C@@H]([C@@H]1O[C@H]2[C@@H](O[C@@H]([C@@H]([C@@H]2O)O)CO)O[C@@H]3[C@H]([C@@H](O[C@@H]([C@@H]3O)CO)O[C@@H]4[C@@H]([C@H]([C@@H](O[C@@H]4CO)O[C@@H]5[C@H](O[C@@H](OC[C@@H]([C@@H](*)O)NC(*)=O)[C@@H]([C@H]5O)O)CO)O)O[C@@]6(C[C@@H]([C@H]([C@@](O6)([C@@H]([C@@H](CO)O)O)[H])NC(C)=O)O)C(=O)[O-])NC(C)=O)O)O)O)C', "
               "'Glycosylated ceramide'), "
               "('O=C(N[C@H]([C@H](O)/C=C/CC/C=C(/CCCCCCCC)\\\\C)CO[C@@H]1O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)[C@H](O)/C=C/CCCCCCCCCCCCCC', "
               "'Glycosylated ceramide'), "
               "('O1[C@@H]([C@@H](O)[C@H](O[C@H]2O[C@@H]([C@@H](O)[C@H](O)[C@@H]2O)CO)[C@H](O)[C@@H]1O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO)CO)[C@@H]4O)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O)CO)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]5NC(=O)C)CO)CO[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O[C@]%10(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%10)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)[C@H]%11O[C@@H]([C@@H](O)[C@H](O)[C@@H]%11O[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%12NC(=O)C)CO)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@H]1O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O[C@@H]%10O[C@H]([C@@H](O)[C@@H](O)[C@@H]%10O)C)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO', "
               "'Glycosylated ceramide'), "
               "('O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)[C@H](O)[C@@H](NC(=O)C)[C@@H]1O[C@@H]([C@@H](O)[C@H](O)CO[C@]3(O[C@H]([C@H](NC(=O)CO)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)CO', "
               "'Glycosylated ceramide'), "
               "('*[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O)NC(*)=O', "
               "'Glycosylated ceramide'), "
               "('[C@H]1([C@H]([C@H]([C@@H]([C@H](O1)CO*)O*)O*)O*)O[C@@H]2[C@@H]([C@@H](O[C@@H]([C@H]2O)CO[C@@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO*)O*)O*)O*)O[C@H]4[C@@H]([C@H]([C@@H](O[C@@H]4CO)O[C@H]5[C@@H]([C@H](CO[C@@H]5CO)NC(C)=O)O)NC(C)=O)O)O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@H](O[C@@H]3O[C@H](CO)[C@H](O)[C@H](O)[C@H]3NC(C)=O)[C@H](O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@@H](CO)O[C@@]3(C[C@H](O)[C@@H](NC(C)=O)[C@@H](O3)[C@H](O)[C@H](O)CO)C([O-])=O)C([O-])=O)[C@H]2O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@H]([C@@H](O[C@@H]([C@H]1O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O[C@@H]4O[C@@H]([C@@H]([C@@H]([C@H]4O)O[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)O)NC(=O)C)O)CO)O[C@@H]6[C@H]([C@@H](O[C@@H]([C@@H]6O)CO)O[C@H]7[C@@H]([C@H]([C@@H](O[C@@H]7CO)O[C@@H]8[C@H]([C@@H](O[C@@H]([C@@H]8O)CO)O[C@H]9[C@@H]([C@H]([C@@H](O[C@@H]9CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(=O)C)O)O)NC(=O)C)[C@@H]%10O[C@H]([C@H]([C@H]([C@@H]%10O)O)O)C', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)\\\\C=C\\\\CCCCCCCCCC(C)C', "
               "'Non-glycosylated ceramide'), "
               "('O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O)CO)[C@H](O)[C@@H]1O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)CO[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O)CO', "
               "'Glycosylated ceramide'), "
               "('O1[C@H](O[C@H]2[C@H](O)[C@H](O[C@@H](O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@H]2O)CO[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)CO[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)[C@@H](O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)[C@@H](O)[C@H](O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O)CO)[C@H](O)[C@H]%10NC(=O)C)CO)[C@H]1CO', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@H]1O)CO[C@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)[C@H](O)[C@@H]4O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%13O[C@@H]([C@@H](O[C@@H]%14O[C@@H]([C@H](O)[C@H](O)[C@H]%14O)CO)[C@H](O)[C@H]%13NC(=O)C)CO', "
               "'Glycosylated ceramide'), "
               "('O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)[C@H](O[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@@H](NC(=O)C)[C@@H]1OC[C@@H](O)[C@H](O)[C@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)CO)[C@@H](NC(=O)C)CO)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@H](O)[C@@H](O)[C@@H](O[C@@H]1CO)O[C@@H]([C@@H](O)[C@H](O)CO[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@@H](NC(=O)C)CO)[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO', "
               "'Glycosylated ceramide'), "
               "('O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4NC(=O)C)CO)CO)[C@H](O)[C@@H]1O[C@H]5[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]5CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO[C@@H]6O[C@H]([C@@H](O)[C@@H](O)[C@@H]6O)C)CO[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1[C@@H](O)[C@H](O)[C@H](O[C@@H]1OC[C@H]2O[C@@H](O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@@H](O)[C@@H](O)[C@@H]2O)CO)[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@H](O)[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)OC[C@@H](O)[C@H](O)[C@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)CO)[C@@H](NC(=O)C)CO)O[C@@H]1CO)[C@H]5O[C@@H]([C@H](O)[C@H](O[C@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O[C@@H]7O[C@H]([C@@H](O)[C@@H](O)[C@@H]7O)C)CO)[C@H]5O)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@@H](O[C@H]2[C@H](O)[C@H](O[C@@H](O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)[C@H]2O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)CO)O[C@@H]([C@@H](O)[C@@H]1O)CO)[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O[C@]%10(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%10)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCC[C@@H](O)C(=O)N[C@@H](CO)[C@H](O)/C=C/CCCCCCCCCC(C)C', "
               "'Non-glycosylated ceramide'), "
               "('[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](*)O)NC(=O)*)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O[C@@H]5O[C@@H]([C@@H]([C@@H]([C@H]5O)O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@@H](CO)OC(C)=O)O)[H])C([O-])=O)O)CO)NC(C)=O)(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O', "
               "'Glycosylated ceramide'), "
               "('[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](CCCCCCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O)O[C@@H]6O[C@@H]([C@@H]([C@@H]([C@H]6O)O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)NC(C)=O)(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O[C@]8(O[C@]([C@@H]([C@H](C8)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)CO)O)[H])C([O-])=O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C', "
               "'Non-glycosylated ceramide'), "
               "('O([C@@H]1[C@@H](O[C@H]2[C@H](O)[C@H](O[C@@H](O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)C)[C@H]2O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)CO)O[C@@H]([C@@H](O)[C@@H]1O)CO)[C@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O[C@]9(O[C@H]([C@H](NC(=O)C)[C@@H](O)C9)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]8O)CO)[C@H](O)[C@H]7NC(=O)C)CO', "
               "'Glycosylated ceramide'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](NC(=O)CCCCCCCCCCCCCCCCCCCCCCCCC)[C@H](O)CCCCCCCCCCCCCCCCC)(O)=O', "
               "'Non-glycosylated ceramide'), "
               "('O([C@@H]1[C@@H](NC(=O)C)[C@H](O[C@H]2[C@@H](O)[C@H](O[C@@H](O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@@H]([C@@H](O)[C@H](O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)[C@@H]2O)CO[C@@H]5O[C@@H]([C@@H](O)[C@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7NC(=O)C)CO)[C@H]6O)CO[C@]8(O[C@H]([C@H](NC(=O)C)[C@@H](O)C8)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]5NC(=O)C)CO)O[C@@H]([C@H]1O)CO)[C@@H]9O[C@@H]([C@H](O)[C@H](O[C@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10NC(=O)C)CO)[C@H]9O[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)CO', "
               "'Glycosylated ceramide'), "
               "('O1[C@@H](O[C@@H]2[C@@H](OC[C@H]3O[C@@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)[C@@H](O)[C@@H](O[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@@H]7O[C@@H]([C@@H](O)[C@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O)CO)[C@H]7NC(=O)C)CO)CO)[C@@H]3O)O[C@@H]([C@@H](O)[C@@H]2O)CO)[C@H](NC(=O)C)[C@@H](O[C@@H]9O[C@H]([C@@H](O)[C@@H](O)[C@@H]9O)C)[C@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H]1CO', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C', "
               "'Non-glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)CCCCCCCCCCCCCCC', "
               "'Non-glycosylated ceramide'), "
               "('S(OC[C@H]1O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@H](O[C@@H]3[C@@H](O)[C@H](O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)OC[C@@H](O)[C@H](O)[C@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@@H](NC(=O)C)CO)O[C@@H]([C@@H]3O)CO)O[C@@H]2CO)[C@H](O)[C@@H](O)[C@H]1O)(O)(=O)=O', "
               "'Glycosylated ceramide'), "
               "('S(OC[C@H]1O[C@@H](OC[C@@H](O)[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)[C@@H](NC(=O)C)CO)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O)(O)(=O)=O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO[C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCC(=O)NC1=CC=C(CCCCC)C=C1', "
               "'Glycosylated ceramide'), "
               "('O[C@@H]1[C@H]([C@@H](O[C@@H]([C@@H]1O)CO)O[C@@H]2[C@H]([C@H](O[C@@H]([C@@H]2O)CO)O[C@@H]3[C@H]([C@@H](O[C@@H]([C@@H]3O)CO)O[C@H]4[C@@H]([C@H]([C@@H](O[C@@H]4CO)O[C@@H]5[C@H]([C@@H](O[C@@H]([C@@H]5O)CO)O[C@H]6[C@@H]([C@H]([C@@H](O[C@@H]6CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(=O)C)O)O[C@H]7[C@H]([C@@H]([C@@H]([C@@H](O7)C)O)O)O)NC(=O)C)O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCCCCCCCC(O)C(=O)NC(CO[C@@H]1O[C@H](COP(O)(=O)OCCN)[C@@H](O)[C@H](O)[C@H]1O)C(O)C(O)CCCCCCCCCCC(C)C', "
               "'Glycosylated ceramide'), "
               "('O[C@@H]1[C@H]([C@@H](O[C@@H]([C@@H]1O)CO)O[C@H]2[C@@H]([C@H]([C@@H](O[C@@H]2CO)O[C@@H]3[C@H]([C@@H](O[C@@H]([C@@H]3O)CO)O[C@H]4[C@@H]([C@H]([C@@H](O[C@@H]4CO)OC[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(=O)C)O[C@H]5[C@H]([C@@H]([C@@H]([C@@H](O5)C)O)O)O)O[C@H]6[C@H]([C@@H]([C@@H]([C@@H](O6)C)O)O)O', "
               "'Glycosylated ceramide'), "
               "('O(P(=O)(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)OC2[C@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O)[O-])C[C@@H]([C@H](O)C*)NC(=O)*', "
               "'Glycosylated ceramide'), "
               "('[C@]1(O[C@]([C@@H]([C@H](C1)O)NC(C)=O)([C@@H]([C@H](O)CO)O)[H])(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H]([C@H](O[C@@H]4[C@H](O[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@H](O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@@H](CO)O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)[O-])O)[H])C(=O)[O-])CO)O)[H])C([O-])=O)[C@H]([C@H](O[C@@H]8[C@H](O[C@@H](OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)[C@@H]([C@H]8O)O)CO)O[C@@H]4CO)O)O[C@H](CO[C@]9(O[C@]([C@@H]([C@H](C9)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)[O-])[C@@H]3O)NC(C)=O)CO)O)C([O-])=O', "
               "'Glycosylated ceramide'), "
               "('O[C@@H]([C@@H](NC(=O)CCCCCCCCCCCCCCCCCCC)CO)/C=C/CCCCCCCCC', "
               "'Ceramide with 2-hydroxy fatty acid'), "
               "('O([C@@H]1[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCC)O)NC(*)=O)[C@@H]([C@H]1O)O)CO)[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O)O[C@@H]4O[C@H]([C@H]([C@H]([C@@H]4O)O)O)C)O', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1OC[C@H]5O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O[C@]%10(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%10)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12O)CO[C@]%13(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%13)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%11NC(=O)C)CO)[C@@H]5O)CO)[C@@H]%14O[C@@H]([C@@H](O[C@@H]%15O[C@@H]([C@H](O)[C@H](O[C@]%16(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%16)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%15O)CO)[C@H](O)[C@H]%14NC(=O)C)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@H]1O)CO[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H]4NC(=O)C)CO)CO)[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@@H]7O[C@@H]([C@@H](O)[C@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O)CO)[C@H]7NC(=O)C)CO)CO', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](CO[C@@H]1O[C@H](CO)[C@@H](O[C@@H]2O[C@H](CO)[C@@H](O)[C@H](O[C@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@@H]3O[C@@H]3O[C@H](CO)[C@@H](O)[C@H](O)[C@H]3NC(C)=O)[C@@H]2O[C@@H]2OC[C@@H](O)[C@H](O)[C@H]2O)[C@H](O)[C@H]1O)NC([*])=O', "
               "'Glycosylated ceramide'), "
               "('[C@@H]1([C@@H]([C@H]([C@H]([C@H](O1)CO)O)O[C@]2(O[C@]([C@@H]([C@H](C2)O)NC(CO)=O)([C@@H]([C@@H](CO)O[C@]3(O[C@]([C@@H]([C@H](C3)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)[H])C([O-])=O)O)O[C@H]4[C@@H]([C@H]([C@@H](O[C@@H]4CO)O[C@@H]5[C@H]([C@@H](O[C@@H]([C@@H]5O)CO)O[C@H]6[C@@H]([C@H]([C@@H](O[C@@H]6CO)OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(=O)*)O)O)O)NC(C)=O)O', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@H](O[C@@H](OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)[C@@H]([C@H]1O)O)CO)[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O[C@@H]4O[C@H]([C@H]([C@H]([C@@H]4O)O)O)C)O[C@H]5[C@@H]([C@H]([C@H]([C@H](O5)CO)O)O)O[C@@H]6O[C@H]([C@H]([C@H]([C@@H]6O)O)O)C)NC(=O)C)O', "
               "'Glycosylated ceramide'), "
               "('[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H](CCCCCCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO)O[C@@H]5O[C@@H]([C@@H]([C@@H]([C@H]5O)O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(CO)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)NC(C)=O)(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O', "
               "'Glycosylated ceramide'), "
               "('[C@@]1(O[C@H]2[C@H]([C@H](O[C@H]([C@@H]2O)O[C@@H]3[C@H](O[C@@H](OC[C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(=O)*)[C@@H]([C@H]3O)O)CO)CO)O[C@H]4[C@@H]([C@H]([C@@H](O)[C@H](O4)CO[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O)O[C@@H]6O[C@@H]([C@@H]([C@@H]([C@H]6O)O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)NC(C)=O)(O[C@]([C@H](NC(=O)C)[C@H](C1)O)([C@@H]([C@H](O)CO)O)[H])C([O-])=O', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1CO)OC[C@H]5O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O[C@]%10(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%10)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@@H]5O)[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O[C@]%13(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%13)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@H]([C@@H](NC(=O)C)CO)[C@@H](O)[C@H](O)CO)O[C@@H]([C@@H]1O)CO)[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)OC[C@@H](O)[C@H](O)[C@H](O)[C@@H](NC(=O)C)CO)[C@@H]2O[C@@H]([C@H](O)[C@H](O[C@@H]3O[C@@H]([C@@H](O)[C@H](O)[C@H]3NC(=O)C)CO)[C@H]2O)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1O[C@H]5[C@H](O)[C@H](O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO[C@@H]7O[C@H]([C@@H](O)[C@@H](O)[C@@H]7O)C)[C@H]5O)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]9NC(=O)C)CO)CO)CO)[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1[C@@H](O)[C@H](O)[C@H](O[C@@H]1OC[C@H]2O[C@@H](O[C@H]3[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]3CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO[C@@H]4O[C@H]([C@@H](O)[C@@H](O)[C@@H]4O)C)[C@@H](O)[C@@H](O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@@H]2O)CO[C@@H]6O[C@@H]([C@@H](O[C@@H]7O[C@@H]([C@H](O)[C@H](O)[C@H]7O)CO)[C@H](O)[C@H]6NC(=O)C)CO)[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO)[C@H](O)[C@H]8NC(=O)C)CO', "
               "'Glycosylated ceramide'), "
               "('[C@]1(O[C@]([C@@H]([C@H](C1)O)NC(C)=O)([C@@H]([C@H](O[C@]2(O[C@]([C@@H]([C@H](C2)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)[O-])CO)O)[H])(O[C@H]3[C@H]([C@H](O[C@H]([C@@H]3O)O[C@@H]4[C@H]([C@H](O[C@@H]5[C@H](O[C@]6(O[C@]([C@@H]([C@H](C6)O)NC(C)=O)([C@@H]([C@H](O[C@]7(O[C@]([C@@H]([C@H](C7)O)NC(C)=O)([C@@H]([C@@H](CO)O[C@]8(O[C@]([C@@H]([C@H](C8)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)[O-])O)[H])C(=O)[O-])CO)O)[H])C([O-])=O)[C@H]([C@H](O[C@@H]9[C@H](O[C@@H](OC[C@@H]([C@@H](CCCCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]9O)O)CO)O[C@@H]5CO)O)O[C@H](CO)[C@@H]4O)NC(C)=O)CO)O)C([O-])=O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](COP([O-])([O-])=O)NC(C)=O', "
               "'Non-glycosylated ceramide'), "
               "('O([C@H]1[C@H](O[C@@H]2O[C@H]([C@@H](O)[C@@H](O)[C@@H]2O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]1CO)OC[C@@H](O)[C@H](O)[C@H](O[C@@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO)[C@H](O[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)[C@H]3NC(=O)C)CO)[C@@H](NC(=O)C)CO)[C@@H]6O[C@@H]([C@H](O)[C@H](O[C@]7(O[C@H]([C@H](NC(=O)C)[C@@H](O)C7)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]6O)CO', "
               "'Glycosylated ceramide'), "
               "('O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO)[C@H](O)[C@H]4NC(=O)C)CO)CO)[C@H](O)[C@@H]1O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO[C@@H]7O[C@H]([C@@H](O)[C@@H](O)[C@@H]7O)C)CO[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O)[C@H]%10O)CO)[C@H](O[C@@H]%11O[C@H]([C@@H](O)[C@@H](O)[C@@H]%11O)C)[C@H]9NC(=O)C)CO)CO', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](COP([O-])([O-])=O)NC(=O)CCCCC', "
               "'Non-glycosylated ceramide'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O)CO)[C@@H]2O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)CO)[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@H]([C@H](O[C@@H]2[C@H](O[C@@H](OC[C@@H]([C@@H](CCCCCCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]2O)O)CO)O[C@@H]([C@@H]1O)CO)O)[C@]3(O[C@]([C@@H]([C@H](C3)O)NC(C)=O)([C@@H]([C@H](O[C@]4(O[C@]([C@@H]([C@H](C4)O)NC(C)=O)([C@@H]([C@@H](CO)O[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@@H](COC(C)=O)O)O)[H])C(=O)[O-])O)[H])C(=O)[O-])CO)O)[H])C([O-])=O', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@H]1O)CO[C@H]3O[C@@H]([C@@H](O[C@@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO[C@]6(O[C@H]([C@H](NC(=O)C)[C@@H](O)C6)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]4NC(=O)C)CO)[C@H](O)[C@@H]3O[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O[C@]9(O[C@H]([C@H](NC(=O)C)[C@@H](O)C9)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]8O)CO)[C@H](O)[C@H]7NC(=O)C)CO)CO)[C@H]%10O[C@@H]([C@@H](O)[C@H](O)[C@@H]%10O[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O[C@]%13(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%13)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%12O)CO)[C@H](O)[C@H]%11NC(=O)C)CO)CO[C@@H]%14O[C@@H]([C@@H](O[C@@H]%15O[C@@H]([C@H](O)[C@H](O)[C@H]%15O)CO[C@]%16(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%16)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%14NC(=O)C)CO', "
               "'Glycosylated ceramide'), "
               "('N([C@H]([C@@H](C*)O)COP([O-])(=O)O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)OC2[C@H]([C@H]([C@@H]([C@H](O2)COP([O-])(=O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H]([C@H]3O)O)O)O)O)O)O)O)C(=O)*', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O)CO)OC[C@@H](O)[C@H](O)[C@H](O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)CO)[C@@H](NC(=O)C)CO)[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O[C@@H]5O[C@H]([C@@H](O)[C@@H](O)[C@@H]5O)C)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@H]1O)CO[C@H]2O[C@@H]([C@@H](O)[C@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O)CO)[C@@H]2O)CO[C@H]4O[C@@H]([C@@H](O)[C@H](O)[C@@H]4O)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO)[C@H]6O[C@@H]([C@@H](O)[C@H](O)[C@@H]6O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O)CO)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1O[C@@H]([C@@H]([C@@H]([C@H]1O)O[C@]2(O[C@]([C@@H]([C@H](C2)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)C[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(=O)*', "
               "'Glycosylated ceramide'), "
               "('C([C@@H]([C@@H]([C@@H](CCCCCCCCCCCCCC)O)O)NC(*)=O)O[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)CO)O[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O[C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)COS([O-])(=O)=O)O)O)NC(C)=O)O)O)O', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1OC[C@H]5O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)[C@@H](O)[C@@H](O[C@H]7O[C@@H]([C@@H](O)[C@H](O)[C@@H]7O[C@@H]8O[C@@H]([C@@H](O[C@@H]9O[C@@H]([C@H](O)[C@H](O)[C@H]9O)CO[C@]%10(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%10)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]8NC(=O)C)CO)CO)[C@@H]5O)CO)[C@@H]%11O[C@@H]([C@@H](O[C@@H]%12O[C@@H]([C@H](O)[C@H](O)[C@H]%12O)CO[C@]%13(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%13)[C@H](O)[C@H](O)CO)C(O)=O)[C@H](O)[C@H]%11NC(=O)C)CO', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP([O-])(=O)OCC[N+](C)(C)C)[C@H](O)[C@H](O)CCCCCCCCCCC(C)C', "
               "'Non-glycosylated ceramide'), "
               "('O([C@H]1[C@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@H]1O)CO[C@H]4O[C@@H]([C@@H](O[C@@H]5O[C@@H]([C@@H](O[C@@H]6O[C@@H]([C@H](O)[C@H](O)[C@H]6O)CO)[C@H](O)[C@H]5NC(=O)C)CO)[C@H](O)[C@@H]4O[C@@H]7O[C@@H]([C@@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O)CO)[C@H](O)[C@H]7NC(=O)C)CO)CO)[C@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O)CO)[C@H](O)[C@H]%10NC(=O)C)CO)[C@H](O)[C@@H]9O[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1[C@@H](O)[C@H](O[C@@H](O[C@H]2[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)O[C@@H]([C@@H](O)[C@H](O)CO[C@]3(O[C@H]([C@H](NC(=O)C)[C@@H](O)C3)[C@H](O)[C@H](O)CO)C(O)=O)[C@@H](NC(=O)C)CO)[C@@H]1O)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O[C@@H]5O[C@@H]([C@H](O)[C@H](O)[C@H]5O)CO[C@]6(O[C@H]([C@H](NC(=O)C)[C@@H](O)C6)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]4NC(=O)C)CO)[C@@H]7O[C@@H]([C@@H](O)[C@H](O[C@@H]8O[C@@H]([C@H](O)[C@H](O)[C@H]8O)CO[C@]9(O[C@H]([C@H](NC(=O)C)[C@@H](O)C9)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]7NC(=O)C)CO', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCC[C@@H](O)[C@H](COP([O-])(=O)OCC[NH3+])NC([*])=O', "
               "'Non-glycosylated ceramide'), "
               "('O1[C@@H]([C@@H](O[C@@H]2O[C@@H]([C@@H](O)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@H]3O[C@@H]([C@@H](O)[C@H](O)[C@@H]3O)CO)[C@H](O)[C@@H]1O[C@H]4[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]4CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO)CO[C@H]5O[C@@H]([C@@H](O)[C@H](O)[C@@H]5O)CO', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP(O)(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)[C@H](O)CCCCCCCCCCCCCCC', "
               "'Non-glycosylated ceramide'), "
               "('S(O[C@@H]1[C@@H](O)[C@H](O[C@H]2[C@H](O[C@@H]3O[C@H]([C@@H](O)[C@@H](O)[C@@H]3O)C)[C@@H](NC(=O)C)[C@@H](O[C@@H]2CO)OC[C@@H](O)[C@H](O)[C@H](O[C@@H]4O[C@@H]([C@H](O)[C@H](O[C@]5(O[C@H]([C@H](NC(=O)C)[C@@H](O)C5)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]4O)CO)[C@@H](NC(=O)C)CO)O[C@@H]([C@@H]1O)CO)(O)(=O)=O', "
               "'Glycosylated ceramide'), "
               "('[C@@H]1([C@@H]([C@H]([C@@H](O)[C@H](O1)CO)O)NC(C)=O)O[C@@H]2[C@H](O[C@]3(O[C@]([C@@H]([C@H](C3)O)NC(C)=O)([C@@H]([C@H](O[C@]4(O[C@]([C@@H]([C@H](C4)O)NC(C)=O)([C@@H]([C@@H](CO)O[C@]5(O[C@]([C@@H]([C@H](C5)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C(=O)[O-])O)[H])C(=O)[O-])CO)O)[H])C(=O)[O-])[C@H]([C@H](O[C@@H]6[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(=O)*)[C@@H]([C@H]6O)O)CO)O[C@@H]2CO)O', "
               "'Glycosylated ceramide'), "
               "('CCCCCCCCCCCCC\\\\C=C\\\\[C@@H](O)[C@H](COC1O[C@H](CO)[C@H](O)[C@H](OS([O-])(=O)=O)[C@H]1O)NC(=O)C(O)[*]', "
               "'Glycosylated ceramide'), "
               "('C(CCCCCC[C@H]([C@H](COP(=O)(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O[C@@H]2[C@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O)[O-])NC(=O)*)O)CCCCCCCCCC', "
               "'Glycosylated ceramide'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](NC(=O)CCCC(O)C(O)C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)[C@H](O)\\\\C=C\\\\CCCCCCCCCCCCC)([O-])=O', "
               "'Non-glycosylated ceramide'), "
               "('O[C@@H]1[C@H](O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O[C@@H]3O[C@@H]([C@@H]([C@@H]([C@H]3O)O[C@]4(O[C@]([C@@H]([C@H](C4)O)NC(C)=O)([C@@H]([C@@H](CO)O)O)[H])C([O-])=O)O)CO)O[C@@H]5O[C@H]([C@H]([C@H]([C@@H]5O)O)O)C)NC(=O)C)[C@H]([C@H](O[C@@H]6[C@H](O[C@@H](OC[C@@H]([C@@H](*)O)NC(=O)*)[C@@H]([C@H]6O)O)CO)O[C@@H]1CO)O', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@H](O[C@@H](OC[C@@H]([C@@H](*)O)NC(=O)*)[C@@H]([C@H]1O)O)CO)[C@@H]2O[C@@H]([C@@H]([C@@H]([C@H]2O)O[C@H]3O[C@@H]([C@@H]([C@@H]([C@H]3O)O[C@H]4[C@@H]([C@H]([C@H]([C@@H](CO)O4)O)O[C@H]5[C@@H]([C@H]([C@H]([C@@H](CO)O5)O)OS(=O)(=O)[O-])O)NC(C)=O)O)CO)O)CO', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@H](O[C@@H](OC[C@@H]([C@@H](/C=C/CCCCCCCCCCCCCCC)O)NC(*)=O)[C@@H]([C@H]1O)O)CO)[C@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O[C@H]3[C@@H]([C@H]([C@H]([C@H](O3)CO)O)O[C@H]4[C@@H]([C@H]([C@H]([C@H](O4)CO)O)O)O[C@@H]5O[C@H]([C@H]([C@H]([C@@H]5O)O)O)C)NC(C)=O)O[C@@]6(C[C@@H]([C@H]([C@@](O6)([C@@H]([C@@H](CO)O)O)[H])NC(CO)=O)O)C(=O)[O-])O', "
               "'Glycosylated ceramide'), "
               "('C(CCCCCCCCCC)CC\\\\C=C\\\\[C@@H](O)[C@@H](NC(=O)CCCCCCCCCCCCCCCCCCCCC)COP(=O)([O-])OCC[N+](C)(C)C', "
               "'Non-glycosylated ceramide'), "
               "('S(OC[C@H]1O[C@@H](O[C@H]([C@@H](NC(=O)C)CO)[C@@H](O)[C@H](O)CO)[C@H](NC(=O)C)[C@@H](O)[C@@H]1O[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO)(O)(=O)=O', "
               "'Glycosylated ceramide'), "
               "('O([C@@H]1[C@@H](NC(=O)C)[C@@H](O[C@@H]([C@H]1O)CO)OC[C@@H](O)[C@H](O)[C@H](O)[C@@H](NC(=O)C)CO)[C@@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO', "
               "'Glycosylated ceramide'), "
               "('S(SC/C=C/1\\\\C2=C(NC(=O)OC)C(=O)C([C@@]1(O)C#CC=CC#C[C@@H]2OC3OC(C(NOC4OC(C(SC)C(C4)O)C)C(C3OC5OCC(NCC)C(C5)OC)O)C)OC6OC(C(OC(=O)C7=C(NC(=O)C(OC)=C)C=C(OC)C(=C7)OC)C(C6)O)C)SC', "
               "'Glycosylated ceramide'), "
               "('O([C@H]1[C@@H](O)[C@H](O[C@@H]2O[C@@H]([C@@H](O[C@@H]3O[C@@H]([C@H](O)[C@H](O[C@]4(O[C@H]([C@H](NC(=O)C)[C@@H](O)C4)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]3O)CO)[C@H](O)[C@H]2NC(=O)C)CO)[C@H](O[C@@H]1OC[C@H]5O[C@@H](O[C@H]6[C@H](O)[C@@H](NC(=O)C)[C@@H](O[C@@H]6CO)O[C@@H]([C@H](O)[C@@H](NC(=O)C)CO)[C@H](O)CO[C@@H]7O[C@H]([C@@H](O)[C@@H](O)[C@@H]7O)C)[C@@H](O)[C@@H](O[C@H]8O[C@@H]([C@@H](O)[C@H](O)[C@@H]8O[C@@H]9O[C@@H]([C@@H](O[C@@H]%10O[C@@H]([C@H](O)[C@H](O[C@]%11(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%11)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%10O)CO)[C@H](O)[C@H]9NC(=O)C)CO)CO[C@@H]%12O[C@@H]([C@@H](O[C@@H]%13O[C@@H]([C@H](O)[C@H](O[C@]%14(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%14)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%13O)CO)[C@H](O)[C@H]%12NC(=O)C)CO)[C@@H]5O)CO)[C@@H]%15O[C@@H]([C@@H](O[C@@H]%16O[C@@H]([C@H](O)[C@H](O[C@]%17(O[C@H]([C@H](NC(=O)C)[C@@H](O)C%17)[C@H](O)[C@H](O)CO)C(O)=O)[C@H]%16O)CO)[C@H](O)[C@H]%15NC(=O)C)CO', "
               "'Glycosylated ceramide')]\n"
               'False negatives: '
               "[('CCCCCCCCCCCCCCCCCCCCCCCCCC(=O)N[C@@H](CN[C@H]1C[C@H](O)[C@@H](O)[C@H](O)[C@H]1O)[C@H](O)[C@H](O)CCCCCCCCCCCCCC', "
               "'No sphingoid base pattern found'), "
               "('[C@@H]([C@H](C*)NC(=O)*)(O)*', 'No sphingoid base pattern "
               "found'), ('OC[C@@H]([C@@H](*)O)NC(=O)*', 'Carbon chain too "
               "short for ceramide'), "
               "('C1(C(OC(OC[C@@H]([C@@H](*)O)NC(=O)*)C(C1O)O)CO)O', 'Carbon "
               "chain too short for ceramide'), "
               "('[C@@H]([C@H](C*)NC(=O)*)(O)*', 'No sphingoid base pattern "
               "found')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 156,
    'num_false_positives': 100,
    'num_true_negatives': 1210,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.609375,
    'recall': 0.975,
    'f1': 0.7499999999999999,
    'accuracy': 0.9292517006802721}