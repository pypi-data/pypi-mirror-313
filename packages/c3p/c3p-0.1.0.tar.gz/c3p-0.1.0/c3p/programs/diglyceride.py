"""
Classifies: CHEBI:18035 diglyceride
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_diglyceride(smiles: str):
    """
    Determines if a molecule is a diglyceride based on its SMILES structure.
    A diglyceride has a glycerol backbone with 2 fatty acid chains attached via ester bonds.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a diglyceride, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Replace * with C for analysis if molecule contains wildcards
    has_wildcards = "*" in smiles
    if has_wildcards:
        smiles = smiles.replace("*", "C")
        mol = Chem.MolFromSmiles(smiles)

    # Look for glycerol backbone pattern with proper connectivity
    glycerol_pattern = Chem.MolFromSmarts("[CH2X4,CH1X4]-[CH1X4,CH2X4]-[CH2X4,CH1X4]")
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "No glycerol backbone found"

    # Look for ester groups (-O-C(=O)-)
    ester_pattern = Chem.MolFromSmarts("[OX2][CX3](=[OX1])[#6]")
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    
    if len(ester_matches) < 2:
        return False, f"Found {len(ester_matches)} ester groups, need at least 2 for diglyceride"

    # Look for ester groups connected to glycerol backbone
    backbone_ester_pattern = Chem.MolFromSmarts("[CH2X4,CH1X4]-[OX2][CX3](=[OX1])[#6]")
    backbone_ester_matches = mol.GetSubstructMatches(backbone_ester_pattern)
    
    if len(backbone_ester_matches) != 2:
        return False, f"Found {len(backbone_ester_matches)} ester groups connected to backbone, need exactly 2"

    # Look for exactly one free hydroxyl on the glycerol backbone
    backbone_oh_pattern = Chem.MolFromSmarts("[CH2X4,CH1X4]-[OX2H]")
    oh_matches = mol.GetSubstructMatches(backbone_oh_pattern)
    if len(oh_matches) != 1:
        return False, f"Found {len(oh_matches)} free hydroxyl groups, need exactly 1"

    # Check for phosphate groups
    phosphate_pattern = Chem.MolFromSmarts("[PX4](=[OX1])([$([OX2H]),$([OX2-])])([OX2])([OX2])")
    if mol.HasSubstructMatch(phosphate_pattern):
        return False, "Contains phosphate group (likely a phospholipid)"

    # For non-wildcard molecules, check fatty acid chain length
    if not has_wildcards:
        # Count carbons in fatty acid chains
        fatty_chain_pattern = Chem.MolFromSmarts("[CH2X4,CH1X4]-[OX2][CX3](=[OX1])[#6]-[#6]")
        matches = mol.GetSubstructMatches(fatty_chain_pattern)
        if len(matches) < 2:
            return False, "Fatty acid chains too short"
            
        carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
        if carbon_count < 7:  # Minimum size for diglyceride
            return False, f"Carbon count ({carbon_count}) too low for diglyceride"

    return True, "Diglyceride with 2 ester groups and glycerol backbone"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18035',
                          'name': 'diglyceride',
                          'definition': 'A glyceride that is glycerol in which '
                                        'any two of the hydroxy groups have '
                                        'been acylated. In the structure '
                                        'shown, two of the R groups (positions '
                                        'not specified) are acyl groups while '
                                        'the remaining R group can be either H '
                                        'or an alkyl group.',
                          'parents': ['CHEBI:47778', 'CHEBI:76578']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.5555555555555555 is too low.\n'
               'True positives: '
               "[('C(CCCCCC(O[C@@H](CO)COC(CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)=O)CCC/C=C\\\\CCCCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCCCC/C=C\\\\CCCCCC)=O)(OC(CCCCCCCCCCCCCCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('CCCCCCCCCCCCCC(=O)OC[C@@H](CO)OC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCCCCCCCCCCC)[C@H](COC(=O)CCCCCCCCCCCCCCCC)CO', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCCCCCCCCCCCCCCCC)[C@H](COC(=O)CCCCCCCCCCCCCCCCCC(C)C)CO', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C[C@H](O)COC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)C(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(CCCCCCC/C=C\\\\CCCCCCCC)=O)CC(COC(=O)CCCCCCCCCCC)O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C[C@](CO)(OC(CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])C(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCC)=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\CCCC)=O)(OC(CCCCCCC/C=C\\\\CCCCCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C[C@](CO)(OC(CCCCCCCCCCCCCCCCCCCCC)=O)[H])C(CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCCCC/C=C\\\\CCCCCC)=O)(OC(CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCCCCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCCCCCCCCC)C[C@@H](O)COC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)[C@H](COC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\CCCC)=O)(OC(CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCCCCCCCCCCCCCC)[C@H](COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCC)CO', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCCCCCCCCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCCCCCCC)C[C@@H](OC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCCCCCCCCCCCCCC)=O)(OC(CCCCCCCCCCCCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(CC(CO)OC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)C(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCC/C=C\\\\CCCCCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OC[C@@H](CO)OC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCCCCCC/C=C\\\\CCCCCCCC)[C@H](COC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCCCCCCCCCCCCC)C[C@H](O)COC(=O)CCCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\CCCCCC)=O)(OC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\CCCCCC)=O)(OC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)(OC(CCCCCCC/C=C\\\\CCCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O([C@H](COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCC)CO)C(=O)CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@@H](CO)OC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCCCCCCCCCCCCC)C[C@@H](O)COC(=O)CCCCCCCCCC(C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCCCC/C=C\\\\CCCCCC)C[C@@H](O)COC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCCCCCCCCCCCCCCCC)=O)(OC(CCCCCCCCCCCCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCCC/C=C\\\\CCCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)(OC(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCCCC/C=C\\\\CCCCCC)=O)(OC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCCCCCCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\CCCC)=O)(OC(CCCCCCCCCCCCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCCCCCCCCCCCCCC)C[C@@H](O)COC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C(CCCCCC)CCC(=O)OCC(CO)OC(CCCCCCC/C=C\\\\CCCCCCCC)=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCCCCC(C)C)[C@H](COC(=O)CCCCCCCCCCCCCCCC(C)C)CO', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCCCCCCCC)=O)(OC(CCCCCCCCCCCCCCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C[C@](CO)(OC(CCCCCCC/C=C\\\\CCCCCC)=O)[H])C(CCCCCCCCC/C=C\\\\CCCCCCCC)=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C[C@](CO)(OC(CCCCCCCCCCCCCCC)=O)[H])C(CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCCCCCCCCCCCC)=O)(OC(CCCCCCC/C=C\\\\CCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C(O)C(OC(=O)*)COC(*)=O', 'Diglyceride with 2 ester groups "
               "and glycerol backbone'), "
               "('O(C[C@](CO)(OC(CCCCCCCCC/C=C\\\\CCCCCC)=O)[H])C(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCC)=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCCCCCCCC)=O)(OC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCCCC/C=C\\\\CCCCCC)C[C@@H](O)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C(O)C(OC(=O)*)COC(*)=O', 'Diglyceride with 2 ester groups "
               "and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\CCCC)=O)(OC(CCCCCCCCC/C=C\\\\CCCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCC/C=C\\\\CCCCCCC)C[C@@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('OC[C@@H](COC([*])=O)OC([*])=O', 'Diglyceride with 2 ester "
               "groups and glycerol backbone'), "
               "('CCCCCCCCCCCCCCCCCC(=O)OC[C@H](O)COC(=O)CCCCCCCCCCCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCCCCCCCC)C[C@@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)CO', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCCCCCCCCCCCC)C[C@@H](O)COC(=O)CCCCCCCCC/C=C\\\\CCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCCCCCCCC(C)C)C[C@H](O)COC(=O)CCCCCCCCCCCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\CCCCCC)=O)(OC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C[C@](CO)(OC(CCCCCCC/C=C\\\\CCCCCCCC)=O)[H])C(CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O[C@@H](CCCCCCCC(O[C@H](COC(=O)CCCCCCC)CO)=O)[C@@H](O)C/C=C\\\\CCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O([C@H](COC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CO)C(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)C[C@H](O)COC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)CCCCCCC/C=C\\\\CCCCCCCC)C[C@@H](O)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCC/C=C\\\\CCCCCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C[C@](CO)(OC(CCCCCCCCCCCCCCCCCCC)=O)[H])C(CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCCCCCCCCCCCCCCCC)=O)(OC(CCCCCCCCCCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('CCCCCCCCCCCCCC(=O)OCC(CO)OC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\CCCCCC)=O)(OC(CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCCCCC/C=C\\\\CCCCCC)=O)(OC(CCCCCCCCCCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C([C@@](COC(CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCCC/C=C\\\\CCCCCCCC)=O)[H])O', "
               "'Diglyceride with 2 ester groups and glycerol backbone')]\n"
               'False positives: '
               "[('CC(\\\\C=C\\\\C=C(/C)C(=O)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=C/C=C/C=C(C)/C=C/C=C(\\\\C)C(=O)O[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('N1(C(=O)[C@]2(N(C([C@](NC([C@H](C([C@@](OC(C[C@@H]([C@H](NC([C@H]([C@H](OC([C@@]1(CC=3C=CC(=CC3)OC)[H])=O)C)NC([C@](N(C)C(=O)[C@]4(N(CCC4)C(=O)C(C)=O)[H])(CC(C)C)[H])=O)=O)[C@](CC)(C)[H])O)=O)(C(C)C)[H])=O)C)=O)([H])CC(C)C)=O)CCC2)[H])C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OC[C@H](CO[C@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O)OC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1OC[C@@]23[C@@]4([C@@]5(OC5)[C@H](O[C@@H]2C=C(C)CC3)C[C@H]4OC(=O)C=CC=C[C@@H](OCCC(=C1)C)[C@H](O)C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCC)COC(=O)CCCCCCCCCCCCCCCC)([O-])=O.[NH4+]', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1O[C@@H]2[C@@](O[C@@H](C)[C@@H]([C@H]2C)OC(=O)/C=C/C(=O)CCCC)(C)[C@H]([C@H]1C)O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O[C@@H]1[C@@H](COC(=O)CC(O)=O)O[C@@H](Oc2cc(O)cc3[o+]c(c(O[C@@H]4O[C@H](COC(=O)\\\\C=C\\\\c5ccc(O)cc5)[C@@H](O)[C@H](O)[C@H]4O)cc23)-c2cc(O)c(O)c(O)c2)[C@H](O)[C@H]1O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1O[C@H]([C@@H](NC(=O)[C@@H](O)[C@H]2OC(=O)CC2)CC(C)C)CC=3C1=C(O)C=CC3', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C[C@@H](COP([O-])(=O)OC[C@H](COC(CCCCCCCCCCCCC)=O)O)O)C(CCCCCCCCCCCCC)=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('COc1c(O)cc2C(=O)OC3C(O)C(O)C(COC(=O)c4cc(O)c(O)c(O)c4)OC3c2c1O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('COc1c(O)cc2C(=O)OC3C(OC(=O)c4cc(O)c(O)c(O)c4)C(O)C(CO)OC3c2c1O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('[C@@]12([C@H]([C@@H](C[C@](O1)(CC=CC=CC(O[C@]3(C[C@](C=CCC=CC(=C2)C)(O[C@@H]([C@]3(CO)C)C/C=C\\\\C[C@@H](C(OCC(CCC(C)C)=C)=O)O)[H])[H])=O)[H])O)C)[H]', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('CC[C@H]1OC(=O)[C@H](C)[C@@H](O[C@H]2C[C@@](C)(O)[C@@H](OC(C)=O)[C@H](C)O2)[C@H](C)[C@@H](O[C@@H]2O[C@H](C)C[C@@H]([C@H]2O)N(C)C)[C@@](C)(C[C@@H](C)C(=O)[C@H](C)[C@@H](O)[C@]1(C)O)O[C@H]1C[C@H]([C@@H](O)[C@H](C)O1)N(C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O1C([C@@H](O)[C@H](O)C(OC(=O)/C=C/C2=CC(O)=C(O)C=C2)[C@@H]1OC3=C(O)C(O)=C(C=C3)C(=O)/C=C/C4=CC(O)=C(O)C=C4)COC(=O)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('[C@H]1(OP([O-])([O-])=O)[C@H](OC(=O)C[C@@H](*)O)[C@@H](NC(=O)C[C@@H](*)O)[C@@H](O[C@@H]1CO[C@@]2(C(=O)[O-])O[C@@H]([C@H](O)[C@@H](C2)OP(=O)([O-])[O-])[C@@H](CO)O)OC[C@@H]3[C@H]([C@@H]([C@H]([C@H](O3)OP(=O)([O-])[O-])NC(=O)C[C@@H](*)O)OC(=O)C[C@@H](*)O)O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('[C@@H]1([C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O)O)O)OC(=O)*)OP(OC[C@H](CO*)OC(=O)*)(=O)[O-])O[C@@H]2[C@H]([NH3+])[C@@H](O)[C@@H]([C@H](O2)CO)O[C@@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO[C@@H]4[C@H]([C@H]([C@@H]([C@H](O4)COP([O-])(=O)OCC[NH3+])O)O)O[C@@H]5[C@H]([C@H]([C@@H]([C@H](O5)COP([O-])(=O)OCC[NH3+])O)O)O)O)O)OP([O-])(=O)OCC[NH3+]', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C1C(C2C(C3C(C4(C(C5C(C(O)C4)(CCC(C5)(C)C)C(OC6OCC(O)C(OC7OC(C(O)C(O)C7O)CO)C6OC(=O)CCC8=CC=C(O)C=C8)=O)=CC3)C)(CC2)C)(CC1)C)(C)C)C9OC(C(O)C(O)C9O)C(O)=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('Cl.[H][C@@]12[C@H](OC(=O)CCN(C)C)[C@H](OC(C)=O)[C@@]3(C)O[C@](C)(CC(=O)[C@]3(O)[C@@]1(C)[C@@H](O)CCC2(C)C)C=C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('CO[C@@H]1C[C@H]2[C@]3(C)CC[C@H]4C(C)(C)CCC[C@]4(C)[C@H]3C[C@@H](OC(C)=O)[C@]2(C)C2=C1C(=O)O[C@H]2O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1O[C@@H]([C@@]2(C=3[C@H](OC(=O)C(CC)C)C[C@]4([C@H](C3C([C@@]52[C@H]1[C@@H](O)NC5=O)=O)CCC4=O)C)C)COC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C1=C(C=C(C2=C1[O+]=C(C(=C2)O[C@@H]3O[C@@H]([C@H]([C@@H]([C@H]3O[C@H]4[C@@H]([C@H]([C@@H](CO4)O)O)OC(/C=C/C5=CC(=C(C(=C5)OC)O)OC)=O)O)O)COC(/C=C/C6=CC=C(C=C6)O)=O)C7=CC(=C(C=C7)O)O)O[C@@H]8O[C@@H]([C@H]([C@@H]([C@H]8O)O)O)CO)[O-]', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O([C@H]1[C@H](O)C(O[C@@H](OC=2C=C3OC(=CC(=O)C3=C(O)C2)C4=CC=C(OC)C=C4)C1O)COC(=O)C)[C@@H]5OC([C@@H](O)[C@H](O)C5O)CO[C@@H]6OC([C@H](OC(=O)C)C(O)[C@@H]6O)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('[H][C@@]12CC[C@@]3([H])[C@@]4(CC[C@H](O)[C@@](C)(COC(C)=O)[C@H]4C=O)C(OC(=O)[C@]3(C1)C(=O)C2=C)C(C)=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('[C@@H]1(O)[C@@H](CO)O[C@@H]([C@@H]([C@H]1O)O[C@@H]2[C@@H]([C@H]([C@H]([C@H](O2)CO)O)O)O)OCC(COC(=O)*)OC(*)=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C(=O)(OC[C@H](COP(=O)(OC[C@H](COP(=O)([O-])[O-])O)[O-])OC(*)=O)*', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1O[C@H]([C@@H](C=CC(O)CCC[C@@H](O)C[C@@H](O)C[C@H](O)C[C@@H]2O[C@@](C([C@H](C(CCC(CCCC(CC(CC=C1)O)O)O)C)O)=O)(O)[C@@H](O)[C@@H](C2)O)C)[C@@H]([C@@H](O)[C@H]([C@@H](O)[C@@H]([C@H](O[C@H]3O[C@@H]([C@H](O[C@H]4O[C@@H]([C@H](OC(=O)[C@@H]([C@H](O[C@H]5O[C@@H]([C@H](O)CC5)C)C6=CC=7C(=O)C=C(C)C(C7C=C6)=O)C)CC4)C)[C@](C3)(O)C)C)CC)C)C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C(O[C@@H]1OC[C@@H](O)[C@@H]([C@H]1OC(=O)CCCCCCCCCCC(C)C)O)/C(=C/C=C/C(=C/C=C/C(=C/C=C/C=C(/C=C/C=C(/C=C/C=C(/C(=O)O)\\\\C)\\\\C)\\\\C)/C)/C)/C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C(O[C@H]1[C@H](OC(=O)C)C(C2CCC3=C([C@]2(C1)C)C[C@H](O)[C@]4([C@]3(CCC4C5C(O[C@@H](C(O)(C)C)CC5)O)C)C)(C)C)CC(O)(CC(=O)O)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O[C@@H]1[C@@H](COC(=O)CC(O)=O)O[C@@H](Oc2cc(O)cc3[o+]c(c(O[C@@H]4O[C@H](COC(=O)\\\\C=C\\\\c5ccc(O)cc5)[C@@H](O)[C@H](O)[C@H]4O)cc23)-c2ccc(O)c(O)c2)[C@H](O)[C@H]1O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C[C@H](OC(=O)CCCCCCCCCCCCCCC)COC(CCCCCCC/C=C\\\\CCCCCCCC)=O)[C@H]1[C@@H]([C@H]([C@@H](O)[C@@H](CO)O1)O)O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O([C@H](COC(=O)CCCCCCCCCCCCCCC)COP(OCC[N+](C)(C)C)(=O)[O-])C(=O)CCCCCCCCO', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O(C(=O)C1=CC(O)=C(O)C(O)=C1)C[C@H]2O[C@@H](O[C@@]34[C@]5([C@@](C3)([C@H](O)C[C@@]4(OC5=O)C)[H])COC(=O)C6=CC=CC=C6)[C@H](O)[C@@H](O)[C@@H]2O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1OCC2C=C(C34OC5CC(C3C(C5)C=CC4C(OC)C(C(OC2C(O)COC=CC6=C(CC1)C(=O)OC6=O)=O)OC)O)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OC[C@@H](O)COP([O-])(=O)OCC(O)COP([O-])(=O)OC[C@H](O)COC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1C([C@H]2[C@](C3=C([C@]4([C@]([C@@H]([C@H](C(=O)OC5O[C@@H]([C@@H](O)[C@@H]([C@H]5O)O)CO)CCC(=C)C(C)C)[C@@H](C4)OC(=O)C)(C)CC3)C)CC2)(C)CC1)(C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O1[C@@H]([C@H](O)[C@H](O)[C@@H](O)[C@@H]1OC[C@H](OC(=O)CCCCC/C=C\\\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCC)CO', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('CCCCCCCC\\\\C=C/CCCCCCCC(=O)OC[C@H](COP([O-])(=O)OC[C@@H](O)CO)OC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1OC2C3(C4(C5C(C(O)(C)CC4)CC3(O)C(C2)O5)COC(=O)C6C7(C(C(=CCC=C1)OCC7)O)O6)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C(OC(COC(=O)CCCCCCCCCCCC(C)C)COC1OC(C(O)C(C1O)O)COC2OC(C(O)C(C2O)O)CO)CCCCCCCCCCCC(C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O[C@H]1[C@@H]([C@H](C(=O)C1)C/C=C\\\\CCCC(O[C@H](COC(=O)C)CO)=O)/C=C/[C@@H](O)CCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('P(OC[C@H](OC(=O)CCCCCCCCCCCCC=1OC(=C(C1C)C)CCCCC)COC(=O)CCCCC(=O)C[C@@H]2[C@H]([C@H](O)C[C@@H]2O)/C=C/[C@@H](O)CCCCC)(OCC[N+](C)(C)C)([O-])=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1OC[C@@]23C4(C5(O)C(O[C@@H]2[C@@H]([C@](O)(C)CC3)C5)C(C4OC(=O)C=CC=C[C@@H]6O[C@H](CC(=C1)C)O[C@H]6C)O)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('COc1ccc(C[C@@H]2N(C)C(=O)[C@@H]3CCCN3C(=O)[C@H](CC(C)C)NC(=O)[C@@H](C)C(=O)[C@@H](OC(=O)C[C@H](O)[C@H](NC(=O)[C@@H](NC(=O)[C@@H](CC(C)C)N(C)C(=O)[C@@H]3CCCN3C(=O)[C@H](C)O)[C@@H](C)OC2=O)C(C)C)C(C)C)cc1', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('[H][C@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@@H]1OC=C(C(=O)OC[C@@H](O)[C@@H](O)[C@H](O)[C@H](O)CO)[C@@]2([H])C[C@H](OC(=O)\\\\C=C\\\\c3ccc(O)c(O)c3)C(=C)[C@@]12[H]', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('CCCCCCCCCCCCCCCC(=O)O[C@@H](CO[C@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C(O)=O)COC(=O)CCCCCCCC[C@H](C)CCCCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1N[C@H](C(=O)N([C@H](C(=O)N2[C@H](C(=O)O[C@@H]([C@@H](CC)C)C(N([C@H](C(N[C@H](C(OC(C1(C)C)CCCC#C)=O)C(C)C)=O)C(C)C)C)=O)CCC2)CC3=CC=CC=C3)C)[C@H](O)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O([C@H]1[C@H](OC(=O)/C=C/C2=CC(O)=C(O)C=C2)[C@H](O[C@@H](OCCC3=CC(O)=C(O)C=C3)[C@@H]1OC(=O)C)CO[C@@H]4O[C@@H]([C@@H](O)[C@H](O)[C@H]4O)CO)[C@@H]5O[C@H]([C@H](O)[C@@H](O)[C@H]5O)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C(OC[C@@]12[C@@]3([C@@]4(OC4)[C@H](O[C@@H]1[C@@H]5O[C@]5(C)CC2)C[C@H]3OC(=O)/C=C\\\\C=C\\\\[C@@H](O)[C@H](O)C)C)/C=C(/CCO)\\\\C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=P([O-])(O[C@@H]1[C@@H]([C@@H]([C@H]([C@@H]([C@H]1O)O)O)O)O)OC[C@@H](COC(CCCCCCC/C=C\\\\CCCCCCCC)=O)OC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('OC[C@H]1O[C@H](Oc2ccc(COC(=O)CC(O)(CC(=O)OCc3ccc(O[C@@H]4O[C@H](CO)[C@@H](O)[C@H](O)[C@H]4O)cc3)C(O)=O)cc2)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C(CC1=CC(OC1O)=O)[C@]2([C@@H](C[C@H]([C@]3(C(CCC[C@@]32C)(C)C)[H])OC(=O)C)C)O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C1([C@H](CO)NC(=O)C2=C3C(=CC=C2)O[Fe-3]456(O3)OC7=C(C=C(C=C7O4)[C@H]8[C@@H]([C@H]([C@@H]([C@H](O8)CO)O)O)O)C(=O)N[C@H](C(OC[C@@H](C([O-])=O)NC(=O)C9=C(C(=CC(=C9)[C@H]%10[C@@H]([C@H]([C@@H]([C@H](O%10)CO)O)O)O)O5)O6)=O)CO1)=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1O[C@H](O)[C@@H]2[C@]13[C@@H](O)[C@@H](OC(=O)[C@H](O)CCCCCCCC)CC([C@@H]3CC=C2C=O)(C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1N2[C@H](C(=O)NCC(=O)N[C@H](C(=O)N3[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)O)CC(C)C)CC4=CC=CC=C4)CC(=O)O)CCC3)CC(=O)O[C@@H]([C@@H]5NC(=O)[C@@H](NC([C@@H](NC([C@H]([C@H](OC(C[C@@H](C(N[C@H]1CC(=O)O)=O)NC(=O)CNC(=O)[C@@H](NC(=O)[C@H]6N(C(=O)CNC5=O)CCC6)CC(=O)N)=O)C)NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)CNC(=O)[C@@H](N)CCCCN)CC(=O)O)[C@H](O)C)=O)CC=7NC=NC7)=O)C)C)CCC2', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('[C@@H]1([C@@H]([C@@H]([C@@H]([C@H]([C@@H]1O)O)O)OC(=O)*)OP(OC[C@H](CO*)OC(=O)*)(=O)[O-])O[C@@H]2[C@H]([NH3+])[C@@H](O)[C@@H]([C@H](O2)CO)O[C@@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO[C@@H]4[C@H]([C@H]([C@@H]([C@H](O4)CO)O)O)O[C@@H]5[C@H]([C@H]([C@@H]([C@H](O5)CO)O)O)O)O)O)OP([O-])(=O)OCC[NH3+]', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1OC(CC=2C1=C(O)C3=C(O)C=C(OC)C(=C3C2)C4=C(OC)C=C(O)C=5C4=CC=6CC(C)OC(C6C5O)=O)C[C@H](O)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1C2=C(O)C=C(O[C@H]3O[C@H](CO)[C@H]([C@H]3OC(=O)C)OC(=O)C)C=C2C(=O)C=4C1=C(O)C=C(C)C4', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1OC(C2=CC=CC=C2)=CC3=C1[C@H](O)[C@@H]4[C@@]5([C@H]([C@@]([C@@H](O)CC5)(COC(=O)C)C)C[C@@H]([C@]4(O3)C)OC(=O)C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O([C@@H]1[C@@]([C@]2([C@@]([C@@]3([C@]([C@]4(C([C@]5([C@@](CC4)(CCC(C5)(C)C)C(O[C@@H]6O[C@@H]([C@H](OC(=O)/C=C/C7=CC=C(OC)C=C7)[C@H](O[C@@H]8O[C@H]([C@H](O)[C@@H](O)[C@H]8O)C)[C@H]6O[C@@H]9O[C@H]([C@H](O[C@@H]%10OC[C@@H](O[C@@H]%11O[C@@H]([C@H](O)[C@H](O)[C@H]%11O)CO)[C@H](O)[C@H]%10O)[C@@H](O)[C@H]9O)C)C)=O)[H])=CC3)CO)(CC2)C)[H])(C[C@@H]1O)C)[H])(C)C(O)=O)[C@@H]%12O[C@@H]([C@@H](O)[C@H](O)[C@H]%12O)CO', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('CC[C@H](C)[C@@H]1OC(=O)[C@H](C)N(C)C(=O)[C@@H](NC(=O)CN(C)C(=O)[C@@H](Cc2ccccc2)N(C)C(=O)[C@H](C)NC(=O)[C@H](OC(=O)\\\\C(C)=C\\\\C[C@H](O)[C@@H]1C)[C@@H](C)CC)[C@H](C)CC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('[H][C@@]12C[C@@H](O)C=C3[C@@H](OC)O[C@H](OC(C)=O)[C@@]13[C@@H](O)[C@H](OC(=O)\\\\C=C/C=C/CCCCC)[C@@H](C)[C@@]2(C)CCC(=C)C=C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('[H][C@@](COC([*])=O)(COP([O-])(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP([O-])([O-])=O)[C@H](O)[C@H]1O)OC([*])=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O1[C@@H]([C@H]([C@@H](O)CC1O)C/C=C\\\\CCCC(O[C@H](COC(=O)CCCCCCCCCCCCC)CO)=O)/C=C/[C@@H](O)CCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('CCCCCCCCCCCCCCCCCCCCCCCCCC(CC(=O)N[C@H](Cc1ccccc1)C(=O)N[C@H]([C@@H](C)O[C@@H]1O[C@@H](C)[C@@H](OC(C)=O)[C@@H](OC(C)=O)[C@H]1O)C(=O)N[C@H](C)C(=O)N[C@@H](C)CO[C@@H]1O[C@@H](C)[C@H](OC)[C@@H](OC)[C@H]1O)OC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1O[C@@H](/C(=C\\\\C)/C)CC=C([C@@H](O[C@H]2O[C@H](CO)[C@H]([C@@H]2O)O)[C@@H](C(C=C[C@@H]1C)=O)OC(=O)CC(C)C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1OC(C2=CN=CC=C2)=CC3=C1[C@H](O)[C@@H]4[C@@]5([C@H]([C@@]([C@@H](O)CC5)(COC(=O)C)C)C[C@@H]([C@]4(O3)C)OC(=O)C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('[C@@]123O[C@]([C@H](C)CC1(C)C)(CC(O[C@@]([C@@H](C)O)(CC(OC(C2)[C@H](C)[C@](O3)([C@H](CC[C@@H](C=4C(=CC(=C(C4)O)Br)Br)OC)C)[H])=O)[H])=O)O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('CCOC(=O)[C@H](C(C)C)N(C)C(=O)[C@@H]1CCCN1C(=O)[C@@H](OC(=O)[C@H](C(C)C)N(C)C(=O)[C@@H](NC(=O)[C@@H](C)[C@H](O)CCCC#CBr)C(C)C)[C@@H](C)CC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('CCCCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](OP([O-])([O-])=O)[C@H]1O)OC(=O)CCCCCCC\\\\C=C/CCCCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C(O)C(O)CCCCCCCCCCCCCC(OC1OCC(O)C(C1OC2OCC(OC(=O)C)C(C2OC3OC(C(O)C(C3O)O)COC(=O)C)O)O)CCCC(O)CCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1ccc(N)nc1=O)OC(=O)CCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1C2=C(C(=O)CC3[C@@]2(CC[C@@H](C3(C)C)O)C)[C@@]4(C(=O)C[C@@H]([C@]4([C@@H]1OC(=O)C)C)[C@@H](CCC(=O)OCCCC)C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1N[C@H](C(=O)N[C@H](C(=O)O)CCCNC(=N)N)CC(=O)NCCCC[C@@H]2NC(=O)[C@@H](NC([C@H]([C@H](OC(C[C@H]3C(N[C@H](C(N[C@H]1CCC(=O)OC[C@H](NC(=O)[C@H]4C(C(=O)[C@@H](NC2=O)CC5=CC=CC=C5)CCC4)C(=O)N3)=O)CC(C)C)=O)=O)C)NC(=O)[C@@H](NC(=O)[C@H]6N(C(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)CNC(=O)[C@@H](N)CCC(=O)O)[C@H](O)C)CCC(=O)O)C(C)C)CCC6)CC=7C8=C(C=CC=C8)NC7)=O)CC9=CC=C(O)C=C9', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O1C(C(O)C(OC(=O)/C=C/C2=CC=C(O)C=C2)C(OC(=O)/C=C/C3=CC=C(O)C=C3)C1OC4=C(OC=5C(C4=O)=C(O)C=C(O)C5)C6=CC=C(O)C=C6)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('OC(C1C2(C(C3C(C4(C(=CC3)CC(O)CC4OC(=O)C)C)CC2)CC1)C)(C(O)CC5C(C(OC5)=O)C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('C[C@@H](O)[C@H](NC(=O)[C@H](CCCNC(N)=N)NC(=O)c1cccc(O)c1O)C(=O)O[C@H](C)[C@H](NC(=O)[C@H](CCCNC(N)=N)NC(=O)c1cccc(O)c1O)C(=O)O[C@H](C)[C@H](NC(=O)[C@H](CCCNC(N)=N)NC(=O)c1cccc(O)c1O)C(O)=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1O[C@@H](C[C@H](C1)O)CC[C@@H]2[C@@H]3C(C=C[C@@H]2C)=C[C@H](C)C[C@@H]3OC(=O)[C@@H](CC)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O([C@@H]1[C@@]([C@@]2([C@](C3[C@@](CC2)([C@@]4(C(=C[C@H]3O)C(C(O[C@@H]5OC[C@@H](OC(=O)C)[C@H](O)[C@H]5O)CC4)(C)C)[H])C)(C1)C)C)([C@@H](CCC=C(C)C)C)[H])[C@@H]6O[C@@H]([C@@H](O)[C@H](O)[C@H]6O)COC(=O)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1O[C@H](C(C=CC=C([C@@H](O)C[C@H](O)C[C@@H](O)C[C@H](OC(=O)C(N)C(C)C)C[C@@H]2O[C@@](C[C@@H]([C@H](CCC(C(C(CC(C(C=CC=C1C)C)O)O)C)O)C)O)(O)[C@@H](O)[C@@H](C2)O)C)C)[C@H](CCCC=CCCCNC(=NC)NC)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1C2=C(O)C(C3=C(O)C4=C(O[C@]56C(=O)O[C@H]([C@@]5(C4=O)O)C[C@@H]([C@@H]6O)C)C=C3)=CC=C2O[C@@]78[C@]1(O)[C@@H](OC7=O)C[C@@H]([C@@H]8O)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O([C@H]1[C@H](O)C(O)[C@@H](OC1COC(=O)C)OCC(O)CCCCCCCCCCCCC(O)C(O)=O)[C@@H]2OC([C@@H](O)[C@H](O)C2OC(=O)CC(O)CCC)CO', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('ClC1=CC(=C(NC)C=C1)C(=O)OC[C@@]2([C@@H](O)CC[C@]3([C@H]2CC[C@]4([C@@H]3C[C@H](OC)[C@H]([C@@H]4C5=C(O)C(=O)OC5O)C)C)C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('[H][C@]1(O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)O[C@H]1[C@@H](O)C[C@@]2(C)[C@@]([H])(CC[C@]3(C)[C@]2([H])CC=C2[C@]4([H])CC(C)(C)CC[C@@]4([C@H](O)C[C@@]32C)C(=O)O[C@@H]2OC[C@H](O)[C@H](O)[C@H]2O[C@]2([H])O[C@@H](C)[C@]([H])(O[C@@H]3OC[C@@H](O)[C@]([H])(O[C@@H]4OC[C@](O)(CO)[C@H]4O)[C@H]3O)[C@@H](O)[C@H]2OC(C)=O)C1(CO)CO', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1N(C(C(=O)O)C(OC(=O)CC(OC(=O)CC(CC(=O)O)C)CCCCCCCCCC)CN(C1C(OC2OC(CN)C(C2O)O)C3OC(N4C(=O)NC(=O)C=C4)C(C3O)O)C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1OC[C@@]23[C@@]4([C@@]5(OC5)[C@H](O[C@@H]2C=C(CO)CC3)C[C@H]4OC(=O)C=CC=C[C@@H](OCCC(=C1)C)[C@H](O)C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('Nc1ccn([C@@H]2O[C@H](COP([O-])(=O)OP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O)[C@@H](O)[C@H]2O)c(=O)n1', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1OCC2=C1[C@@]3([C@H](C(CC[C@H]3O)(C)C)[C@H](C2)OC(=O)/C=C/C4=CC=CC=C4)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1O[C@H]2C3=C[C@H]4OC(=O)[C@@]5([C@H]4[C@@]([C@]3(O)[C@H]([C@@]2(C)CC1)O)(CCC5)C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O1C23C(C(OC(=O)C)C(C2=CC(=O)C4=C3OC5(C(C6(C(OC(CC6OC(=O)C)C(O)(C)C)CC5)C)C4O)C)C)(C1C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1OCC2=C1[C@H](C=C(C(=O)OC[C@@]3(O)[C@@H](C(=O)O)[C@H](C=C(C(=O)O)CO)[C@@H](C(C)C)CC3)CO)[C@@H](C(C)C)CC2', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O1C(C(O)C(O)C(OC(=O)/C=C\\\\C2=CC=C(O)C=C2)C1OC(=O)C3=CC(O)=C(O)C(O)=C3)CO', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('[H][C@]12[C@H](OC(=O)c3ccccc3)[C@]3(O)C[C@H](O)C(C)=C([C@@H](OC(C)=O)C(=O)[C@]1(C)[C@@H](O)C[C@H]1OC[C@@]21OC(C)=O)C3(C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('[H][C@@]12OC3(O[C@@H]([C@@H](C)[C@]4(O3)[C@]3([H])C[C@H](C)[C@H](OC(C)=O)[C@@]3(OC(C)=O)[C@H](O)[C@](C)(OC(=O)c3ccccc3)[C@@H](OC(C)=O)[C@@]14[H])[C@@]2(O)C(C)=C)c1ccccc1', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C1O[C@@H]([C@H](C=CC(O)CCC[C@H](O)C[C@H](O)C[C@@H](O)C[C@H]2O[C@](C([C@@H](C(CCC(CCCC(CC(CC=C1)O)O)O)C)O)=O)(O)[C@H](O)[C@H](C2)O)C)[C@H]([C@H](O)[C@@H]([C@H](O)[C@H]([C@@H](O[C@@H]3O[C@H]([C@@H](O[C@@H]4O[C@H]([C@@H](OC(=O)[C@H]([C@@H](O[C@@H]5O[C@H]([C@@H](O)CC5)C)C6=CC=7C(=O)C=C(C)C(C7C=C6)=O)C)[C@H](C4)O)C)[C@@](C3)(O)C)C)CC)C)C)C', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('CCCCCC\\\\C=C/CCCCCCCCCC(=O)OC[C@H](CO[C@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)OC(=O)CCCCCCCCC\\\\C=C/CCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O=C(O)[C@@]1(O)C2(OC(CCC[C@@H](OC(=O)C)[C@@H](C/C=C/C3=CC=CC=C3)C)(O[C@@H]1C(=O)O)[C@@H]([C@H]2OC(=O)CCCCCCC)O)C(=O)O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('CCCCCCCCCCCCCCCC(=O)O[C@H]1[C@H](O[C@H](CO)[C@@H](O)[C@@H]1OC(=O)CCCCCCCCCCCCCCCO)O[C@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1OS(O)(=O)=O', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP([O-])([O-])=O)[C@H](O)[C@H]1O)OC(=O)CCCCCCCCCCCCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O1C(C(O)C(OC(=O)/C=C/C2=CC=C(O)C=C2)C(O)C1OC3=C(OC=4C(C3=O)=C(O)C=C(O)C4)C5=CC=C(O)C=C5)COC(=O)/C=C/C6=CC=C(O)C=C6', "
               "'Diglyceride with 2 ester groups and glycerol backbone'), "
               "('O[C@H](CCCCCCCC(OC[C@@H](OC(=O)CCCCCCC)CO)=O)[C@H](O)C/C=C\\\\CCCCC', "
               "'Diglyceride with 2 ester groups and glycerol backbone')]\n"
               "False negatives: [('C(O*)(COC(CCCCCCC)=O)CO*', 'Found 1 ester "
               "groups, need at least 2 for diglyceride'), "
               "('C(CCCCCCC/C=C\\\\CCCCCCCC)(=O)O[C@@H](COP(=O)([O-])[O-])CO/C=C\\\\CCCCCCCCCCCCCCCC', "
               "'Found 1 ester groups, need at least 2 for diglyceride'), "
               "('O(CCCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCC', "
               "'No free hydroxyl group on glycerol backbone'), "
               "('O(C(COC(=O)C)CO)C(=O)C', 'Carbon count (7) too low for "
               "typical diglyceride'), ('C(O*)C(O*)CO*', 'Found 0 ester "
               "groups, need at least 2 for diglyceride'), "
               "('O[C@H]1[C@@H](O)[C@@H](COC([*])=O)O[C@@H](OC[C@@H](COC([*])=O)OC([*])=O)[C@@H]1O', "
               "'Contains more than 2 ester groups on glycerol backbone "
               "(likely a triglyceride)'), "
               "('P(OCC[N+](C)(C)C)(OCC(O/C=C\\\\CCCCCC/C=C\\\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCC)([O-])=O', "
               "'Found 1 ester groups, need at least 2 for diglyceride'), "
               "('O(CCCCCCCCCCCCCCCCCC)C(COC(=O)CCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCC', "
               "'No free hydroxyl group on glycerol backbone'), "
               "('C(O*)C(O*)CO*', 'Found 0 ester groups, need at least 2 for "
               "diglyceride'), ('[*]OCC(CO[*])O[*]', 'Found 0 ester groups, "
               "need at least 2 for diglyceride'), "
               "('O(CCCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCCCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC', "
               "'No free hydroxyl group on glycerol backbone'), "
               "('O(CCCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC', "
               "'No free hydroxyl group on glycerol backbone'), "
               "('OC[C@](COC(CCCCCCC)=O)(OC(=O)CCCCCCC)[H]', 'Carbon count "
               "(19) too low for typical diglyceride'), "
               "('O(CCCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCCCC', "
               "'No free hydroxyl group on glycerol backbone'), "
               "('[*]OCC(CO[*])O[*]', 'Found 0 ester groups, need at least 2 "
               "for diglyceride'), ('[*]OCC(CO[*])O[*]', 'Found 0 ester "
               "groups, need at least 2 for diglyceride'), "
               "('O(CCCCCCCCCCCCCCCCCC)[C@@H](COC(=O)CCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCC/C=C\\\\CCCCCCCC', "
               "'No free hydroxyl group on glycerol backbone'), "
               "('O([C@H](COC(=O)CCC)CO)C(=O)CCC', 'Carbon count (11) too low "
               "for typical diglyceride'), ('[*]OCC(CO[*])O[*]', 'Found 0 "
               "ester groups, need at least 2 for diglyceride'), "
               "('O(CCCCCCCCCCCCCCCCCC)C[C@@H](OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCC/C=C\\\\CCCCCCCC', "
               "'No free hydroxyl group on glycerol backbone')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 76,
    'num_false_positives': 100,
    'num_true_negatives': 36223,
    'num_false_negatives': 19,
    'num_negatives': None,
    'precision': 0.4318181818181818,
    'recall': 0.8,
    'f1': 0.5608856088560885,
    'accuracy': 0.996732385084299}