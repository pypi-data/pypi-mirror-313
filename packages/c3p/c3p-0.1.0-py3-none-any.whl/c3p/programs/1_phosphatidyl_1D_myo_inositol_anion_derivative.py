"""
Classifies: CHEBI:147334 1-phosphatidyl-1D-myo-inositol anion derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_1_phosphatidyl_1D_myo_inositol_anion_derivative(smiles: str):
    """
    Determines if a molecule is a 1-phosphatidyl-1D-myo-inositol anion derivative.
    These are phosphatidylinositol anions where the inositol is either not phosphorylated 
    or phosphorylated at position 4 and/or position 5.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 1-phosphatidyl-1D-myo-inositol anion derivative
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for basic inositol ring with phosphatidyl linkage
    inositol_patterns = [
        Chem.MolFromSmarts("[C@H]1[C@H](O)[C@@H](O)[C@H](OP([O-])(=O)OCC)[C@@H](O)[C@H]1O"),
        Chem.MolFromSmarts("O[C@H]1[C@H](O)[C@@H](O)[C@H](OP([O-])(=O)OCC)[C@H](O)[C@@H]1O")
    ]
    
    has_inositol = False
    for pattern in inositol_patterns:
        if pattern is not None and mol.HasSubstructMatch(pattern):
            has_inositol = True
            break
            
    if not has_inositol:
        return False, "No myo-inositol ring with correct stereochemistry and phosphatidyl linkage found"

    # Check for glycerol backbone with ester linkages
    glycerol_pattern = Chem.MolFromSmarts("COP([O-])(=O)OC[C@@H](COC(=O)*)OC(=O)*")
    if not mol.HasSubstructMatch(glycerol_pattern):
        glycerol_pattern_alt = Chem.MolFromSmarts("COP([O-])(=O)OC[C@H](COC(=O)*)OC(=O)*")
        if not mol.HasSubstructMatch(glycerol_pattern_alt):
            return False, "No proper glycerol backbone with ester linkages found"

    # Check for phosphate groups at positions 4 and/or 5
    phosphate_pattern = Chem.MolFromSmarts("OP([O-])([O-])=O")
    matches = mol.GetSubstructMatches(phosphate_pattern)
    
    if len(matches) == 0:
        return True, "Unphosphorylated phosphatidylinositol"
    
    # Patterns for phosphates at positions 4 and 5
    correct_phosphate_patterns = [
        Chem.MolFromSmarts("[C@H]1[C@H](O)[C@H](O)[C@@H](OP([O-])([O-])=O)[C@H](OP([O-])([O-])=O)[C@H]1O"),
        Chem.MolFromSmarts("[C@H]1[C@H](O)[C@H](O)[C@@H](OP([O-])([O-])=O)[C@H](O)[C@H]1O"),
        Chem.MolFromSmarts("[C@H]1[C@H](O)[C@H](O)[C@H](O)[C@@H](OP([O-])([O-])=O)[C@H]1O")
    ]
    
    for pattern in correct_phosphate_patterns:
        if pattern is not None and mol.HasSubstructMatch(pattern):
            return True, "Phosphatidylinositol with phosphate groups at positions 4 and/or 5"
    
    return False, "Contains phosphate groups at positions other than 4 and 5"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:147334',
                          'name': '1-phosphatidyl-1D-myo-inositol anion '
                                  'derivative',
                          'definition': 'A phosphatidylinositol anion where '
                                        'the inositol is either not '
                                        'phosphorylated or phosphorylated at '
                                        'position 4 and/or position 5; major '
                                        'species at pH 7.3.',
                          'parents': ['CHEBI:62643']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.26923076923076916 is too low.\n'
               'True positives: '
               "[('CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('O[C@H]1[C@H](O)[C@@H](O)[C@H](OP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O)[C@H](O)[C@@H]1O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('CCCCCCCC(=O)OC[C@H](COP([O-])(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP([O-])([O-])=O)[C@H](OP([O-])([O-])=O)[C@H]1O)OC(=O)CCCCCCC', "
               "'Phosphatidylinositol with phosphate groups at positions 4 "
               "and/or 5'), "
               "('CCCCC\\\\C=C/C\\\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCCCCCC\\\\C=C/C\\\\C=C/CCCCC', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('O[C@H]1[C@H](O)[C@@H](O)[C@H](OP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O)[C@H](O)[C@@H]1O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('CCCCCC\\\\C=C/CCCCCCCCC(=O)OC[C@H](COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OC(=O)CCCCCCCCCCC', "
               "'Unphosphorylated phosphatidylinositol')]\n"
               'False positives: '
               "[('O=P([O-])(O[C@@H]1[C@@H]([C@@H]([C@H]([C@@H]([C@H]1O[C@H]2O[C@@H]([C@H]([C@@H]([C@H]2NC(C)=O)O)O)CO)O)O)O)O)OCC(COC(CCCCCCCCCCCCCCCCC)=O)OC(=O)CCCCCCC/C=C\\\\CCCCCCCC', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('CC(=O)N[C@@H]1[C@@H](O)[C@H](O)[C@@H](CO)O[C@@H]1O[C@@H]1[C@@H](O)[C@H](O)[C@@H](O)[C@@H](O)[C@H]1OP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('O(C(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)C[C@H](COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O)(=O)[O-])O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](OP([O-])([O-])=O)[C@@H](OP([O-])([O-])=O)[C@H]1O)OC(=O)CCCCCCCCCCCCCCC', "
               "'Phosphatidylinositol with phosphate groups at positions 4 "
               "and/or 5'), "
               "('CCCCCC\\\\C=C/CCCCCCCCC(=O)OC[C@@H](O)COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('[C@@H]1([C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O)O)O)O[C@@H]2[C@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O)OP(OC[C@@H](COC(=O)*)OC(=O)*)(=O)[O-])O[C@@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('OC1C(O)C(O)C(OP([O-])(=O)OCC(COC=C[*])OC([*])=O)C(O)C1O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('P(OC1[C@H](O)[C@H](O)C(O)[C@H](O)[C@H]1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)([O-])=O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('OC(COC([*])=O)COP([O-])(=O)OC1C(O)C(O)C(O)C(O)C1O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('O=P([O-])(O[C@@H]1[C@@H]([C@@H]([C@H]([C@@H]([C@H]1O[C@H]2O[C@@H]([C@H]([C@@H]([C@H]2[NH3+])O)O)CO)O)O)O)O)OCC(COC(CCCCCCCCCCCCCCCCC)=O)OC(=O)CCCCCCC/C=C\\\\CCCCCCCC', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OC[C@@H](O)COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('O=P([O-])(O[C@@H]1[C@@H]([C@@H]([C@H]([C@@H]([C@H]1O)O)O)O)O[C@@H]2[C@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O)OC[C@@H](COC(*)=O)OC(*)=O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('O[C@H](CO\\\\C=C/[*])COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('CCCCCCCCCCCCCCCCCC(=O)OC[C@@H](O)COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('CC(C)CCC[C@@H](C)CCC[C@@H](C)CCC[C@@H](C)CCOC[C@@H](COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O)OCC[C@H](C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('[H][C@@](COC([*])=O)(COP([O-])(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1O[C@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1[NH3+])OC([*])=O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('[C@@H]1([C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O*)O*)O)O)OP(OC[C@@H](COC(=O)*)OC(=O)*)(=O)[O-])O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('[C@@H]1([C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O)O)O)O[C@@H]2[C@H]([C@H]([C@@H]([C@H](O2)COC(=O)*)O)O)O)OP(OC[C@@H](COC(=O)*)OC(=O)*)(=O)[O-])O[C@@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('P(OC1[C@H](O)[C@@H](O)C(O)[C@@H](O)[C@H]1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCC/C=C\\\\CCCCCC)([O-])=O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('P(OC1[C@H](O)[C@@H](O)C(O)[C@@H](O)[C@H]1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)([O-])=O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('O[C@H]1[C@H](O)[C@@H](O)[C@H](OP([O-])(=O)OC[C@@H](COC([*])=O)O[*])[C@H](O)[C@@H]1O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('O([C@@H]1[C@@H]([C@@H]([C@H]([C@@H]([C@H]1O[C@@H]2[C@H]([C@H]([C@@H]([C@H](O2)COC(=O)CCCCCCCCCCCCCCC)O)O)O)OC(CCCCCCCCCCCCCCC)=O)O)O)O[C@@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)P(=O)([O-])OC[C@@H](COC(CCCCCCCC[C@H](CCCCCCCC)C)=O)OC(CCCCCCCCCCCCCCC)=O.[Na+]', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('[C@@H]1([C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O)O)O)O)OP(OC[C@@H](COC=C*)OC(*)=O)(=O)[O-])O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCC(O)C(=O)N[C@@H](COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O[C@@H]2O[C@H](COP([O-])(=O)O[C@H]3[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]3O)[C@@H](O)[C@H](O)[C@@H]2O)[C@H]1O)[C@H](O)[C@H](O)CCCCCCCCCCCCCC', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('P(OC1[C@H](O)[C@@H](O)C(O)[C@@H](O)[C@H]1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCCCCCCCCCC)([O-])=O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('[H][C@@](COC([*])=O)(COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](OP([O-])([O-])=O)[C@@H](OP([O-])([O-])=O)[C@H]1O)OC([*])=O', "
               "'Phosphatidylinositol with phosphate groups at positions 4 "
               "and/or 5'), "
               "('OC1C(O)C(O)C(OP([O-])(=O)OCC(COC([*])=O)OC([*])=O)C(O)C1O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('O([C@@H]1[C@@H]([C@@H]([C@H]([C@@H]([C@H]1O[C@@H]2[C@H]([C@H]([C@@H]([C@H](O2)COC(=O)CCCCCCCCCCCCCCC)O)O)O)OC(CCCCCCCCCCCCCCC)=O)O)O)O[C@@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)P(=O)([O-])OC[C@@H](COC(CCCCCCCC[C@H](CCCCCCCC)C)=O)OC(CCCCCCCCCCCCCCC)=O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('OC(COC=C[*])COP([O-])(=O)OC1C(O)C(O)C(O)C(O)C1O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('O[C@H]1[C@H](O)[C@@H](O)[C@H](OP([O-])(=O)OC[C@@H](CO\\\\C=C/[*])OC([*])=O)[C@H](O)[C@@H]1O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('C(C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CC(=O)OC[C@H](COP(O[C@H]1[C@@H]([C@H]([C@@H]([C@H]([C@H]1O)O)O)O)O)(=O)[O-])O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('O=P([O-])(O[C@@H]1[C@@H]([C@@H]([C@H]([C@@H]([C@H]1O)O)O)O)O[C@@H]2[C@H]([C@H]([C@@H]([C@H](O2)COC(*)=O)O)O)O)OC[C@@H](COC(*)=O)OC(*)=O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@@H](O)COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('CCCCCCCC(=O)OC[C@H](COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](OP([O-])([O-])=O)[C@@H](OP([O-])([O-])=O)[C@H]1O)OC(=O)CCCCCCC', "
               "'Phosphatidylinositol with phosphate groups at positions 4 "
               "and/or 5'), "
               "('O[C@H](COC([*])=O)COP([O-])(=O)O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCC)COC(=O)CCCCCCCCCCCCCCCC)([O-])=O.[NH4+]', "
               "'Unphosphorylated phosphatidylinositol'), "
               "('[C@@H]1([C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O)O)O)OC(=O)*)OP(OC[C@H](COC(=O)*)OC(=O)*)(=O)[O-])O[C@@H]2[C@H]([NH3+])[C@@H](O)[C@@H]([C@H](O2)CO)O', "
               "'Unphosphorylated phosphatidylinositol')]\n"
               'False negatives: '
               "[('CCCCCCCC(=O)OC[C@H](COP([O-])(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP([O-])([O-])=O)[C@H](O)[C@H]1O)OC(=O)CCCCCCC', "
               "'Contains phosphate groups at positions other than 4 and 5')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 8,
    'num_false_positives': 43,
    'num_true_negatives': 183848,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.1568627450980392,
    'recall': 1.0,
    'f1': 0.2711864406779661,
    'accuracy': 0.9997661759987819}