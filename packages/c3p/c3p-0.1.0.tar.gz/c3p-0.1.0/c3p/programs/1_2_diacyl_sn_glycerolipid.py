"""
Classifies: CHEBI:144368 1,2-diacyl-sn-glycerolipid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_1_2_diacyl_sn_glycerolipid(smiles: str):
    """
    Determines if a molecule is a 1,2-diacyl-sn-glycerolipid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 1,2-diacyl-sn-glycerolipid, False otherwise
        str: Reason for classification
    """
    # Check for valid SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Look for glycerol backbone pattern with correct stereochemistry
    glycerol_pattern = Chem.MolFromSmarts("[OX2][CH2X4][C@@H]([OX2])[CH2X4][OX2]")
    if not mol.HasSubstructMatch(glycerol_pattern):
        glycerol_pattern_alt = Chem.MolFromSmarts("[OX2][CH2X4][C@H]([OX2])[CH2X4][OX2]")
        if not mol.HasSubstructMatch(glycerol_pattern_alt):
            return False, "Missing glycerol backbone with correct stereochemistry"

    # Look for acyl groups at positions 1,2
    acyl_pattern = Chem.MolFromSmarts("[CX3](=O)[OX2]")
    acyl_matches = mol.GetSubstructMatches(acyl_pattern)
    if len(acyl_matches) < 1:
        return False, "Missing required acyl group(s)"

    # Check R3 position for allowed groups
    # Updated patterns to be more specific
    r3_h_pattern = Chem.MolFromSmarts("[CH2X4][OH]")
    r3_phosphate_pattern = Chem.MolFromSmarts("[CH2X4]OP(=O)([O-])[O-]")
    r3_phospholipid_pattern = Chem.MolFromSmarts("[CH2X4]OP(=O)([O-])O[CH2,CH3]")

    if mol.HasSubstructMatch(r3_phosphate_pattern):
        return True, "Valid 1,2-diacyl-sn-glycerolipid with R3=phosphate"
    elif mol.HasSubstructMatch(r3_phospholipid_pattern):
        return True, "Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid"
    elif mol.HasSubstructMatch(r3_h_pattern):
        return True, "Valid 1,2-diacyl-sn-glycerolipid with R3=H"
    else:
        # Check for wildcard patterns that might indicate R3 groups
        r3_wildcard_pattern = Chem.MolFromSmarts("[CH2X4][OX2][*]")
        if mol.HasSubstructMatch(r3_wildcard_pattern):
            return True, "Valid 1,2-diacyl-sn-glycerolipid with R3=H"

    return False, "R3 position does not match allowed groups (H, phosphate, or phospholipid)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:144368',
                          'name': '1,2-diacyl-sn-glycerolipid',
                          'definition': 'A diradylglycerolipid where R1 and R2 '
                                        'are acyl chains and R3 can be an H, a '
                                        'phosphate or a phospholipid group.',
                          'parents': ['CHEBI:35741', 'CHEBI:50860']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.019417475728155338 is too low.\n'
               "True positives: [('OC[C@@H](CO\\\\C=C/[*])OC([*])=O', 'Valid "
               "1,2-diacyl-sn-glycerolipid with R3=H')]\n"
               'False positives: '
               "[('C(C(COC(CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)O/C=C\\\\CCCCCCCC/C=C\\\\CCCCCC)OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('[C@](COC(CCCCCCCCCCCCC)=O)(OC(=O)CCCCCCCCCCCCC)([H])COP(OCCC[S+](C)C)([O-])=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)C(C(C(C(C(C(C(C(C(C(C(C(C([2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])COC(=O)C(C(C(C(C(C(C(C(C(C(C(C(C([2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([2H])[2H])([O-])=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('O1[C@@H]([C@H](O)C(O)C(O)[C@@H]1OC[C@H](OC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO[C@H]2O[C@@H]([C@H](O)C(O)C2O)CO', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCCC)([O-])=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('S([C@@H]([C@@H](O)CCCC(O)=O)/C=C/C=C/C=C\\\\C/C=C\\\\CCCCC)C[C@H](N)C(O[C@H](COC(=O)CCCCCCCCC)CO)=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('CCCCCCCCCCCCCCCCCC(=O)O[C@H](COC(=O)CCCCCCC\\\\C=C/CCCCCCCC)COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\CCCC)=O)(OC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('P(OC[C@H](OC(=O)CCC(O)/C=C/C(O)=O)COC(=O)CCCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('N[C@@H](COP(O)(=O)OC[C@H](O)CO)C(O)=O', 'Valid "
               "1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCC)([O-])=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('CCCCCCCCCCCC(=O)OC[C@H](COP([O-])([O-])=O)OC(=O)CCCCCCCCCCC', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phosphate'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCC([O-])=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)C=C)COCCCCCCCCCCCCCCCC)([O-])=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('O=C(CCC/C=C\\\\C\\\\C=C/C=C/C(C/C=C\\\\CCCCC)OO)OC(CO)CO', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('[C@](CO/C=C\\\\CCCCCCCCCCCCCC)(OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)([H])COP(OCC[N+](C)(C)C)([O-])=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('O(C[C@](CO)(OC(CCCCCCCCC/C=C\\\\CCCCCC)=O)[H])C(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('C(C(COC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)O/C=C\\\\CCCCCCCCCCCCCC)OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('CCCCCCCCCCCCCCCCCCOC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCCCCCCC\\\\C=C/C\\\\C=C/CCCCC', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('O(C(=O)CCCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)CO', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('[C@H]1(O)[C@@H](OC[C@H]2O[C@H]([C@@H]([C@H]([C@H]2O)O)O)OC[C@@H](COC(=O)*)OC(*)=O)O[C@H](CO)[C@@H]([C@@H]1O)O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('CCCCCCCCCCCCCCCCC(=O)OC[C@@H](O)COP([O-])([O-])=O', 'Valid "
               "1,2-diacyl-sn-glycerolipid with R3=phosphate'), "
               "('O[C@H]1[C@@H]([C@H](C(=O)C1)C/C=C\\\\CCCC(OC[C@@H](OC(=O)CCCCCCCCCCCCCCCC)CO)=O)/C=C/[C@@H](O)CCCCC', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OCC(O)CO)OC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C([C@@](COC(CCCCCCCCCCCCC)=O)(OC(CCCCCCC/C=C\\\\CCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C([C@H](NC(*)=O)C([O-])=O)OP(=O)([O-])OC[C@H](O)COC(=O)*', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('CCCCCCCCCCCCCC(=O)OCC(O)CO', 'Valid "
               "1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)[H])O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)(OC(CCCCCCC/C=C\\\\CCCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OC[C@H](CO)OC([*])=O', 'Valid "
               "1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('C([C@@](COC(CCCCCCCCCCC/C=C\\\\CCCCCCCC)=O)(OC(CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)[H])O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('[H][C@@](COC(=O)CCCCCCC\\\\C=C/CCCCCCCC)(COP([O-])([O-])=O)OC(=O)CCCCCCC\\\\C=C/CCCCCC', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phosphate'), "
               "('C([C@@](COC(CCCCCCCCCCCCC/C=C\\\\CCCCCCCC)=O)(OC(CCCCCCC/C=C\\\\CCCC)=O)[H])O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('C(\\\\OC[C@H](COP([O-])(=O)OCC[NH3+])OC(=O)*)=C\\\\CCCCCCCCCCCCCCCC', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C(OC[C@H](COP(OCC[N+](C)(C)C)(=O)[O-])O)(*)=O', 'Valid "
               "1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C([C@@](COC(CCCCCCCCCCC/C=C\\\\CCCCCCCC)=O)(OC(CCCCCCCCC/C=C\\\\CCCCCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('P([O-])(=O)(OC[C@@H](C(=O)[O-])[NH3+])OC[C@@H](COC(=O)*)OC(=O)*', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OCC(CO[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)OC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('C([C@@](CO/C=C\\\\CCCCCCCCCCCCCC)(OC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)(OC(CCCCCCCCCCCCCCCCC)=O)[H])OP(=O)(O)OC[C@@](CO)([H])O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)C)COCCCCCCCCCC/C=C\\\\CCCC)([O-])=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C([C@@](COC(CCCCCCCCCCCCC)=O)(OC(CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('C([C@@](COC(CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCCC/C=C\\\\CCCCCCCC)=O)[H])O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('CCCCCCCCCCCCCCCC(=O)OCC(O)COP([O-])([O-])=O', 'Valid "
               "1,2-diacyl-sn-glycerolipid with R3=phosphate'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCC)([O-])=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C([C@@](COC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCC/C=C\\\\CCCC)=O)[H])O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('[NH3+]CCOP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O', 'Valid "
               "1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C(C(COC(CCCCCCCCCCCCCCC)=O)O/C=C\\\\CCCCCCCC/C=C\\\\CCCCCC)OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('O(C(=O)CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)[C@H](COC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)([O-])=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C([C@@](COC(CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](O)COC(=O)CC)([O-])=O', 'Valid "
               "1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('O(C[C@](COP([O-])(=O)OCC[N+](C)(C)C)(OC(CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)[H])CCCCCCCCCCCC/C=C\\\\CCCCCCCC', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C(C[NH3+])OP(=O)([O-])OC[C@H](OC(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C=C\\\\C(CCCCC)O)=O)COC(=O)CCCCCCCCCCCCCCCCC', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('CCCCCCCCCCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OCC(O)COP([O-])(=O)OC[C@H](O)COC([*])=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('[H][C@@](COC(=O)CCCCCCCCCCCCCCC)(COP([O-])([O-])=O)OC(=O)CCCCCCC\\\\C=C/CCCCCC', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phosphate'), "
               "('P(OC[C@@H](CO)OC(=O)CCCCCC)(=O)(OCC[N+](C)(C)C)[O-]', 'Valid "
               "1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C(CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(=O)OCC(COP(=O)(OCC(CO)O)O)OC(CCCCCCCCCCCCCCC)=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('C([C@@](COC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)(OC(CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)[H])O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('O(C(=O)CCCCCCCCCCC)C[C@@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('CCCCCCCCCCCCCCCCCCCC(=O)O[C@H](COC(=O)CCCCCCC\\\\C=C/CCCCCCCC)COP([O-])([O-])=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phosphate'), "
               "('C(\\\\CCCCCCCCOC[C@H](COP([O-])(=O)OCC[NH3+])OC(=O)*)=C\\\\CCCCCCCC', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('O(C[C@](CO)(OC(CCCCCCCCC/C=C\\\\CCCCCC)=O)[H])C(CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('C(C[N+](C)(C)C)OP(=O)([O-])OC[C@H](OC(=O)C)COCCCCCCCCCCCCCCC', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C(C(COC(CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)O/C=C\\\\CCCCCCCCCCCCCC)OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('OC[C@](COC(CCCCCCCC1CC2C3C4C5CCC5C4C3C21)=O)([H])OCCCCCCCCC6CCC7C(C6)C8C7C9C8CC9', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCC)([O-])=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CC', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](OP([O-])([O-])=O)[C@H]1O)OC(=O)CCCCCCC\\\\C=C/C\\\\C=C/CCCCC', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\CCCC)=O)(OC(CCCCCCC/C=C\\\\CCCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C([C@@](COC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('O([C@H](COC(=O)CCCCCCCCCCCCCCC)COP(OCC[N+](C)(C)C)(=O)[O-])C(=O)CCCCCCCCO', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCC)([O-])=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('O=P([O-])(O[C@@H]1[C@@H]([C@@H]([C@H]([C@@H]([C@H]1O[C@H]2O[C@@H]([C@H]([C@@H]([C@H]2NC(C)=O)O)O)CO)O)O)O)O)OCC(COC(CCCCCCCCCCCCCCCCC)=O)OC(=O)CCCCCCC/C=C\\\\CCCCCCCC', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OCCNC(=O)CCCCCCCCC)OC(=O)CCCCCCC\\\\C=C/C\\\\C=C/CCCCC', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('O1C(C(O)C(O)C(O)C1OCC(OC(=O)CCCCCCCCCCCCCCC)COCCCCCCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('C(C[N+](C)(C)C)OP(=O)([O-])OC[C@H](OC(*)=O)COC(=O)*', 'Valid "
               "1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C([C@@](COC(CCCCCCCCCCCCC)=O)(OC(CCCCCCCCCCCCCCCCCCCCC)=O)[H])O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('P(O[C@H]1[C@H](O[C@H]2OC([C@@H](O)C(O)[C@H]2O)CO)C(O)[C@H](O)C(O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(O)=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('O=C(O[C@H](CO[C@H]1O[C@@H]([C@@H](O)C([C@H]1O)O)CO)COCCCCCCCCCCCCCCC)CCCCCCCCCCCCCC', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('C(C[N+](C)(C)C)OP(=O)([O-])OCC(OC(*)=O)COC(=O)*OO', 'Valid "
               "1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('O(C(=O)CCCCCCCCC/C=C\\\\CCCCCCCC)[C@H](COC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('CC(C)[C@H](N)C(=O)OCC(CO)OCn1cnc2c1[nH]c(N)nc2=O', 'Valid "
               "1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('[C@@H](COC(CCCCCCCCCCCCCCC)=O)(COP(OCC[N+](C)(C)C)(=O)[O-])OC(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCC)=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C([C@@](COC(CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCCCCCCC)=O)[H])OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C=1(/C=C(/C=C/C=C(/C=C/C2=C(CCCC2(C)C)C)\\\\C)\\\\C)C=C(C=C[N+]1CCOP(OC[C@@H](COC(*)=O)OC(*)=O)(=O)[O-])/C=C/C=C(/C=C/C3=C(CCCC3(C)C)C)\\\\C', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('OC[C@@H](COP([O-])(=O)OC[C@H](CO)OC([*])=O)OC([*])=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('O[C@@H]1[C@@H]([C@H]([C@H](O)C1)/C=C/[C@@H](O)CCCCC)CC(=O)CCCCC(OC(CO)CO)=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('C[N+](C)(C)CCOP([O-])(=O)OC[C@H](O)COC([*])=O', 'Valid "
               "1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('O(C(=O)CCCCCCC/C=C\\\\CCCC)[C@H](COC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)([O-])=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('C([C@](COC(CCCCCCCCCCC/C=C\\\\CCCCCCCC)=O)([H])O)OP([O-])(=O)OCC[N+](C)(C)C', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=phospholipid'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'Valid 1,2-diacyl-sn-glycerolipid with R3=H')]\n"
               "False negatives: [('O(*)C[C@@H](CO*)OC(*)=O', 'R3 position "
               'does not match allowed groups (H, phosphate, or '
               "phospholipid)')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 2107,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9547306473517428}