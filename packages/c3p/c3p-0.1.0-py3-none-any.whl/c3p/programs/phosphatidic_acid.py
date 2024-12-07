"""
Classifies: CHEBI:16337 phosphatidic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_phosphatidic_acid(smiles: str):
    """
    Determines if a molecule is a phosphatidic acid - a derivative of glycerol with one hydroxy group 
    esterified with phosphoric acid and the other two esterified with fatty acids.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a phosphatidic acid, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Look for phosphate group (-OP(=O)(O)O)
    phosphate_pattern = Chem.MolFromSmarts('[O,OH]-P(=O)([O,OH])[O,OH]')
    if not mol.HasSubstructMatch(phosphate_pattern):
        return False, "No phosphate group found"

    # Look for glycerol backbone with specific connectivity
    # Pattern matches glycerol backbone with phosphate and two ester groups
    glycerol_pattern = Chem.MolFromSmarts('[#6]C(=O)O[CH2][CH](O[#6])[CH2]OP(=O)([O,OH])[O,OH]')
    
    if not mol.HasSubstructMatch(glycerol_pattern):
        # Try alternative pattern for different representation
        glycerol_pattern2 = Chem.MolFromSmarts('[#6]C(=O)OC[CH]([CH2]OP(=O)([O,OH])[O,OH])OC(=O)[#6]')
        if not mol.HasSubstructMatch(glycerol_pattern2):
            # Try pattern for generic structures with wildcards
            if '*' in smiles:
                generic_pattern = Chem.MolFromSmarts('C(O[#6])(CO[#6])[CH2]OP(=O)([O,OH])[O,OH]')
                if mol.HasSubstructMatch(generic_pattern):
                    return True, "Generic phosphatidic acid structure found"
            return False, "No proper glycerol backbone found"

    # Look for two ester groups (-C(=O)O-) connected to glycerol
    ester_pattern = Chem.MolFromSmarts('C(=O)O[CH2,CH]')
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    if len(ester_matches) < 2:
        return False, "Less than 2 ester groups found"

    # Check for fatty acid chains (at least 4 carbons in length)
    fatty_acid_pattern = Chem.MolFromSmarts('C(=O)O[CH2,CH]-[CH2]-[CH2]-[CH2]')
    if not mol.HasSubstructMatch(fatty_acid_pattern):
        return False, "No proper fatty acid chains found"

    # All criteria met
    return True, "Valid phosphatidic acid structure found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16337',
                          'name': 'phosphatidic acid',
                          'definition': 'A derivative of glycerol in which one '
                                        'hydroxy group, commonly but not '
                                        'necessarily primary, is esterified '
                                        'with phosphoric acid and the other '
                                        'two are esterified with fatty acids.',
                          'parents': ['CHEBI:37739']},
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
               "[('C([C@H](NC(*)=O)C([O-])=O)OP(=O)([O-])OC[C@H](O)COC(=O)*', "
               "'Generic phosphatidic acid structure found'), "
               "('P([O-])(=O)(OC[C@@H](C(=O)[O-])[NH3+])OC[C@@H](COC(=O)*)OC(=O)*', "
               "'Generic phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OC[C@@H](CO[*])O[*])C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OCC(COC([*])=O)OC([*])=O)C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('[C@@H](COC(=O)*)(COP(OC[C@@H](C(=O)[O-])[NH3+])(=O)[O-])OC(=O)*', "
               "'Generic phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OCC(CO)OC([*])=O)C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OCC(CO[*])O[*])C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP(O)(=O)OC[C@H](COC([*])=O)OC([*])=O)C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('N[C@@H](COP(O)(=O)OC[C@@H](CO[*])O[*])C(O)=O', 'Generic "
               "phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OC[C@@H](CO)OC([*])=O)C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('C(=O)(N[C@H](C(=O)O)COP(OC[C@@H](COC(=O)*)OC(=O)*)(=O)O)*', "
               "'Generic phosphatidic acid structure found'), "
               "('P([O-])(=O)(OC[C@@H](C(=O)[O-])NC(C[NH3+])=O)OC[C@@H](COC(=O)*)OC(=O)*', "
               "'Generic phosphatidic acid structure found'), "
               "('[C@](CO/C=C\\\\*)(O)([H])COP(OC[C@@H](C(O)=O)N)(=O)O', "
               "'Generic phosphatidic acid structure found'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OCC(CO[*])OC([*])=O)C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('N[C@@H](COP(O)(=O)OC[C@@H](CO[*])OC([*])=O)C(O)=O', 'Generic "
               "phosphatidic acid structure found'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)O[C@H](COC=C[*])COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OC[C@@H](COC([*])=O)O[*])C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OC[C@@H](CO[*])OC([*])=O)C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OC[C@H](COC([*])=O)OC([*])=O)C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OCC(O)COC=C[*])C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('[C@](CO*)(O)([H])COP(OC[C@@H](C(O)=O)N)(=O)O', 'Generic "
               "phosphatidic acid structure found'), "
               "('[C@@H](COC(=O)*)(COP(OC[C@@H](C(=O)O)N)(=O)O)OC(=O)*', "
               "'Generic phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OCC(O)COC([*])=O)C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('C([C@H](NC(*)=O)C([O-])=O)OP(=O)([O-])OC[C@H](OC(*)=O)COC(=O)*', "
               "'Generic phosphatidic acid structure found'), "
               "('P(O)(=O)(OC[C@@H](C(=O)O)N)OC[C@@H](CO*)O*', 'Generic "
               "phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OC[C@H](O)COC=C[*])C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('C(OC[C@H](COP(OC[C@@H](C(O)=O)N)(=O)O)OC(*)=O)=C*', 'Generic "
               "phosphatidic acid structure found'), "
               "('CCCCCC\\\\C=C/CCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OC[C@H](O)CO\\\\C=C/[*])C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O)C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('P(O)(=O)(OC[C@@H](C(=O)O)N)OC[C@@H](COC(=O)*)OC(=O)*', "
               "'Generic phosphatidic acid structure found'), "
               "('N[C@@H](COP(O)(=O)OC[C@@H](CO)OC([*])=O)C(O)=O', 'Generic "
               "phosphatidic acid structure found'), "
               "('N[C@@H](COP(O)(=O)OC[C@@H](COC([*])=O)O[*])C(O)=O', 'Generic "
               "phosphatidic acid structure found'), "
               "('Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP([O-])(-*)=O)[C@@H](OC(=O)[C@@H]([NH3+])COP([O-])([O-])=O)[C@H]1O', "
               "'Generic phosphatidic acid structure found'), "
               "('CCCCC\\\\C=C/C\\\\C=C/CCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('O(P(OC[C@@H](C(=O)O)N)(=O)O)C[C@@H](CO*)O*', 'Generic "
               "phosphatidic acid structure found'), "
               "('O(C[C@@H](C(=O)[O-])[NH3+])P(=O)(OC[C@@H](COC(=O)*)O)[O-]', "
               "'Generic phosphatidic acid structure found'), "
               "('N[C@@H](COP(O)(=O)OC[C@H](O)COC([*])=O)C(O)=O', 'Generic "
               "phosphatidic acid structure found'), "
               "('O(P(=O)(OC[C@@H](C([O-])=O)NC(CNC(=O)[C@@H](N*)*)=O)[O-])C[C@H](OC(*)=O)COC(*)=O', "
               "'Generic phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OC[C@H](O)CO[*])C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OC[C@@H](CO\\\\C=C/[*])OC([*])=O)C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('P(=O)(OC[C@@H](C(=O)[O-])[NH3+])(OC[C@@H](COC(=O)*)OC(=O)*)[O-]', "
               "'Generic phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OCC(O)CO[*])C([O-])=O', 'Generic "
               "phosphatidic acid structure found'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)O[C@H](CO\\\\C=C/[*])COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('O(P(=O)(OC[C@@H](C([O-])=O)NC(CN*)=O)[O-])C[C@H](OC(*)=O)COC(*)=O', "
               "'Generic phosphatidic acid structure found'), "
               "('N[C@@H](COP(O)(=O)OC[C@@H](COC([*])=O)OC([*])=O)C(O)=O', "
               "'Generic phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OCC(COC=C[*])OC([*])=O)C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('C(C(COP(=O)(OC[C@@H](C(=O)O)N)O)OC(=O)*)OC(=O)*', 'Generic "
               "phosphatidic acid structure found'), "
               "('N[C@@H](COP(O)(=O)OC[C@H](COC([*])=O)OC([*])=O)C(O)=O', "
               "'Generic phosphatidic acid structure found'), "
               "('[NH3+][C@@H](COP([O-])(=O)OC[C@@H](COC=C[*])OC([*])=O)C([O-])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('CC(C)(COP(O)(=O)OC[C@H](N)C(O)=O)[C@@H](O)C(=O)NCCC(=O)NCCSC([*])=O', "
               "'Generic phosphatidic acid structure found'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O)OC([*])=O', "
               "'Generic phosphatidic acid structure found')]\n"
               'False negatives: '
               "[('P(OC[C@H](OC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('CCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(O)=O)OC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'No proper glycerol backbone found'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(O)=O)OC(=O)CCCCCCC\\\\C=C/C\\\\C=C/CCCCC', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCC)COC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(O)=O)OC(=O)CCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(O)=O)OC(=O)CCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCC(O)/C=C/C=O)COC(=O)CCCCCCCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('[C@@H](COC(=O)*)(COP(=O)(O)O)OC(*)=O', 'No proper glycerol "
               "backbone found'), "
               "('CCCCCCCCCC(=O)OC[C@H](COP(O)(O)=O)OC(=O)CCCCCCCCC', 'No "
               "proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCC(=O)/C=C/C(O)=O)COC(=O)CCCCCCCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('O(C(*)=O)C(COC(=O)*)COP(=O)(O)O', 'No proper glycerol "
               "backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCCC(C)C)COC(=O)CCCCCCCCCCCCCCCCCCCCC(C)C)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('CCCCCCCCCCCCCCCCCCCC(=O)O[C@H](COC(=O)CCCCCCC\\\\C=C/CCCCCCCC)COP(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('O(C(*)=O)C(COC(=O)*)COP(=O)(O)O', 'No proper glycerol "
               "backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCC/C=C\\\\CCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCC[C@H](O)[C@@H](O)C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCC/C=C\\\\CCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCCCCCCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('CCCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(O)=O)OC(=O)CCCCCCCCCCC', "
               "'No proper glycerol backbone found'), "
               "('O(C(*)=O)C(COC(=O)*)COP(=O)(O)O', 'No proper glycerol "
               "backbone found'), "
               "('C([C@@](COC(CCCCCCCCC/C=C\\\\CCCCCC)=O)(OC(CCCCCCC/C=C\\\\CCCCCCCC)=O)[H])OP(O)(=O)O', "
               "'No proper glycerol backbone found'), "
               "('O(C(*)=O)C(COC(=O)*)COP(=O)(O)O', 'No proper glycerol "
               "backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found'), "
               "('P(OC[C@H](OC(=O)CCCC(O)/C=C/C(O)=O)COC(=O)CCCCCCCCCCCCCCC)(O)(O)=O', "
               "'No proper glycerol backbone found')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 49316,
    'num_false_negatives': 44,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 0.10204081632653061,
    'f1': 0.06493506493506494,
    'accuracy': 0.997088850702517}