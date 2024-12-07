"""
Classifies: CHEBI:167497 1-O-(alk-1-enyl)-2-acyl-sn-glycerolipid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_1_O__alk_1_enyl__2_acyl_sn_glycerolipid(smiles: str):
    """
    Determines if a molecule is a 1-O-(alk-1-enyl)-2-acyl-sn-glycerolipid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 1-O-(alk-1-enyl)-2-acyl-sn-glycerolipid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define key structural patterns
    # Pattern for glycerol backbone with vinyl ether at sn-1 and acyl at sn-2
    glycerol_pattern = Chem.MolFromSmarts("[CH2X4]-[CHX4]-[CH2X4]")
    
    # Pattern for vinyl ether (O-C=C) at sn-1 position
    vinyl_ether_pattern = Chem.MolFromSmarts("O-C=C")
    
    # Pattern for acyl group at sn-2 position
    acyl_pattern = Chem.MolFromSmarts("C(=O)-O")
    
    # Pattern for phosphocholine group
    phosphocholine_pattern = Chem.MolFromSmarts("COP(=O)([O-])OCC[N+](C)(C)C")

    # Check for essential structural features
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "No glycerol backbone found"

    if not mol.HasSubstructMatch(vinyl_ether_pattern):
        return False, "No vinyl ether (O-C=C) group found"

    if not mol.HasSubstructMatch(acyl_pattern):
        return False, "No acyl group found"

    # Check if molecule contains phosphocholine group
    has_phosphocholine = mol.HasSubstructMatch(phosphocholine_pattern)

    # Handle wildcards (*) in SMILES
    if "*" in smiles:
        if has_phosphocholine:
            return True, "1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid"
        return False, "Does not match the required structural patterns for 1-O-(alk-1-enyl)-2-acyl-sn-glycerolipid"

    # Look for characteristic patterns in SMILES
    has_vinyl_ether = any(pattern in smiles for pattern in ["CO/C=C\\", "CO\\C=C/", "COC=C"])
    has_ester = "C(=O)O" in smiles or "OC(=O)" in smiles

    if has_vinyl_ether and has_ester:
        if has_phosphocholine:
            return True, "1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid"
        return False, "Does not match the required structural patterns for 1-O-(alk-1-enyl)-2-acyl-sn-glycerolipid"

    return False, "Does not match the required structural patterns for 1-O-(alk-1-enyl)-2-acyl-sn-glycerolipid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:167497',
                          'name': '1-O-(alk-1-enyl)-2-acyl-sn-glycerolipid',
                          'definition': 'A plasmalogen of unkown fatty acid '
                                        'composition and where the '
                                        'glycerolipid is not defined, R3 can '
                                        'be H or a phospholipid.',
                          'parents': ['CHEBI:35741']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.08849557522123892 is too low.\n'
               'True positives: '
               "[('CC(=O)O[C@H](CO\\\\C=C/[*])COP([O-])(=O)OCC[N+](C)(C)C', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid'), "
               "('CCCCCCCCCCCCCCCC(=O)O[C@H](COC=C[*])COP([O-])(=O)OCC[N+](C)(C)C', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid'), "
               "('C(OC[C@H](COP(OCC[N+](C)(C)C)(=O)[O-])OC(*)=O)=C*', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid'), "
               "('C(OC[C@H](COP(OCC[N+](C)(C)C)(=O)[O-])OC(*)=O)=C*', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid'), "
               "('[C@@H](CO/C=C\\\\CCCCCCCCCCCCCCCC)(COP(OCC[N+](C)(C)C)(=O)[O-])OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid')]\n"
               'False positives: '
               "[('P(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('[C@](CO/C=C\\\\CCCCCCCCCCCCCC)(OC(=O)CCC/C=C\\\\C/C=C\\\\C=C\\\\[C@H](C/C=C\\\\CCCCC)O)([H])COP(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCC)CO/C=C\\\\CCCCCCCCCCCCCC)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)O[C@H](CO\\\\C=C/CCCCCCCC\\\\C=C/CCCCCC)COP(O)(=O)OCCN', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO/C=C\\\\CCCCCCCCCCCCCC)(O)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('CCCCCCCCCCCCCCCC(=O)O[C@H](CO\\\\C=C/CCCCCCCC\\\\C=C/CCCCCC)COP(O)(=O)OCCN', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('OCC(CO/C=C\\\\*)OC(=O)*', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCC)(O)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(O)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO/C=C\\\\CCCCCCCCCCCCCC)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCC/C=C\\\\CCCCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H]1O[C@@H](OC[C@H]2O[C@@H](OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCC)CO/C=C\\\\CCCCCCCCCCCC)C(O)C(O)[C@@H]2O)C(O)C(O)[C@@H]1O)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('CC(=O)O[C@H](CO\\\\C=C/[*])COP([O-])(=O)OCC[NH3+]', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('CCCCCCCCCCCCCCCCCC(=O)OC(CO)CO\\\\C=C/CCCCCC\\\\C=C/CCCCCCCC', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCC)CO/C=C\\\\CCCCCCCCCCCCCC)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO/C=C\\\\CCCCCCCC/C=C\\\\CCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('C(OC[C@H](COP(OCC[NH3+])(=O)[O-])OC(*)=O)=C*', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO/C=C\\\\CCCCCC/C=C\\\\CCCCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('CCCCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCC(=O)O[C@H](COC=C[*])COP([O-])(=O)OCC[NH3+]', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCC)CO/C=C\\\\CCCCCCCCCCCCCCCC)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@@H](CO/C=C\\\\CCCCCCCCCCCCCCCC)OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(=O)(OCCN)O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCC)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO/C=C\\\\CCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@@H](COC(*)=O)O/C=C/*)(=O)(OCC[N+](C)(C)C)[O-]', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCC)(O)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO/C=C\\\\CCCCCCCC/C=C\\\\CCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCC/C=C\\\\CCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCC)(O)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCC)([O-])=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid'), "
               "('P(OC[C@H](OC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCC/C=C\\\\CCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OCC(OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C=C\\\\C(O)C/C=C\\\\C/C=C\\\\CC)CO/C=C\\\\CCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)O[C@H](COC=C[*])COP([O-])(=O)OC[C@H]([NH3+])C([O-])=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('C(*)(=O)O[C@@H](COP(=O)(OCCNC(*)=O)[O-])CO/C=C\\\\*', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCC)([O-])=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('S([C@@]12N(C(=O)[C@]3(SC)CC=4[C@H](N3C1=O)[C@@H](OC(=O)C[C@@H](O)CCCCC)C=CC4)[C@@H]5[C@@H](OC(=O)C[C@@H](O)CCCCC)C=COC=C5C2)C', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@@H](COC(*)=O)OC=C*)(=O)(OCC[NH3+])[O-]', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCC/C=C\\\\CCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OCC(OC(=O)CC/C=C\\\\CC(O)/C=C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO/C=C\\\\C/C=C\\\\CCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('[H][C@@](CO\\\\C=C/CCCCCCCCCCCCCC)(COP([O-])(=O)OCC[NH3+])OC(=O)CCCCCCCCCCCCCCC', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OCC(OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C=C\\\\C(O)CCCCC)CO/C=C\\\\CCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OCC[N+](C)(C)C)(OCC(OC(=O)CCCCCCCCCCCCCC)CO/C=C\\\\CCCCCC/C=C\\\\CCCCCCCC)([O-])=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OCC[N+](C)(C)C)(OCC(OC(=O)CCCCCCCC(O)/C=C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCCCCCCCC)([O-])=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCC)([O-])=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid'), "
               "('P(=O)(OCC(OC(=O)CCCCCCCCCCCC(C)C)CO/C=C\\\\CCCCCCCCCCC(C)C)(OCCN)O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCC/C=C\\\\CCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OCC[N+](C)(C)C)(OCC(OC(=O)CCC/C=C\\\\CC(O)/C=C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO/C=C\\\\CCCCCCCCCCCCCCCC)([O-])=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid'), "
               "('C(OC[C@H](COP(OCC(CO)O)(=O)O)OC(*)=O)=C*', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('[C@](CO/C=C\\\\CCCCCCCCCCCCCC)(OC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)([H])COP(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)([O-])=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('CCCCCCCC(=O)O[C@H](COC=C[*])COP([O-])(=O)OCC[NH3+]', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCC)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('CC(=O)O[C@H](COC=C[*])COP([O-])(=O)OCC[NH3+]', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('C([C@](COP(O)(=O)OC[C@@](CO/C=C\\\\CCCCCCCCCCCCCC)(OC(=O)CCCCCCCCCCCC)[H])(N)[H])(=O)O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OCC[N+](C)(C)C)(OCC(OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C\\\\C=C/C=C\\\\C(O)C/C=C\\\\CC)CO/C=C\\\\CCCCCCCCCCCCCC)([O-])=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)([O-])=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid'), "
               "('P(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO/C=C\\\\CCCCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCC/C=C\\\\CCCCCC)([O-])=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCC)CO/C=C\\\\CCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('C(OCC(COP(OCC(CO)O)(=O)[O-])OC(*)=O)=C*', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCC)CO/C=C\\\\CCCCCC/C=C\\\\CCCCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('[C@](CO/C=C\\\\CCCCCCCCCCCCCCCC)(OC(=O)CC/C=C\\\\C/C=C\\\\C\\\\C=C/C=C/C(C/C=C\\\\C/C=C\\\\CC)O)([H])COP(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('C(OCC(COP(OCC(CO)O)(=O)O)OC(*)=O)=C*', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('S([C@@]12N(C(=O)[C@]3(SC)CC=4[C@H](N3C1=O)[C@@H](OC(=O)C[C@@H](O)CCCCC)C=CC4)[C@@H]5[C@@H](O)C=COC=C5C2)C', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('C(*)(=O)O[C@@H](COP(=O)(OCCNC(*)=O)O)CO/C=C\\\\*', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(OC[C@H](N)C(O)=O)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCCC)CO/C=C\\\\CCCCCC/C=C\\\\CCCCCCCC)(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO/C=C\\\\CCCCCCCCCCCCCC)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCC)(O)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('[C@](CO/C=C\\\\CCCCCCCCCCCCCCCC)(OC(=O)CCCCCCCCCCCCCC)([H])COP(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('[C@](CO/C=C\\\\CCCCCCCCCCCCCC)(OC(=O)CC/C=C\\\\C/C=C\\\\C\\\\C=C/C=C/C(C/C=C\\\\C/C=C\\\\CC)O)([H])COP(OCCN)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('C(OC[C@H](COP(OC[C@@H](C(O)=O)N)(=O)O)OC(*)=O)=C*', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO/C=C\\\\CCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(OC[C@@H](O)CO)(O)=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycerol'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)([O-])=O', "
               "'1-O-(alk-1-enyl)-2-acyl-sn-glycero-phospholipid')]\n"
               'False negatives: '
               "[('[C@@H](OC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)(CO/C=C\\\\CCCCCCCCCCCCCC)COP(OCC[N+](C)(C)C)(=O)[O-]', "
               "'Does not match the required structural patterns for "
               "1-O-(alk-1-enyl)-2-acyl-sn-glycerolipid'), "
               "('C[N+](C)(C)CCOP([O-])(=O)OC[C@@H](COC=C[*])OC([*])=O', 'Does "
               'not match the required structural patterns for '
               "1-O-(alk-1-enyl)-2-acyl-sn-glycerolipid'), "
               "('[C@@H](OC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)(CO/C=C\\\\CCCCCCCCCCCCCCCC)COP(OCC[N+](C)(C)C)(=O)[O-]', "
               "'Does not match the required structural patterns for "
               "1-O-(alk-1-enyl)-2-acyl-sn-glycerolipid')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 6,
    'num_false_positives': 20,
    'num_true_negatives': 183867,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.23076923076923078,
    'recall': 0.75,
    'f1': 0.3529411764705882,
    'accuracy': 0.9998803665134995}