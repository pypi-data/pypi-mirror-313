"""
Classifies: CHEBI:16701 nucleoside 5'-phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_nucleoside_5__phosphate(smiles: str):
    """
    Determines if a molecule is a nucleoside 5'-phosphate.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a nucleoside 5'-phosphate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for phosphate group
    patt_phosphate = Chem.MolFromSmarts('[CH2]OP(=O)([O,OH])[O,OH]')
    if not mol.HasSubstructMatch(patt_phosphate):
        return False, "No phosphate group found at 5' position"

    # Check for ribose/deoxyribose
    patt_ribose = '[C@@H]1O[C@H](CO[P])[C@H](O)[C@@H]1O' # Simplified pattern
    patt_deoxyribose = '[C@@H]1O[C@H](CO[P])C[C@@H]1O'   # Simplified pattern
    
    has_ribose = mol.HasSubstructMatch(Chem.MolFromSmarts(patt_ribose))
    has_deoxyribose = mol.HasSubstructMatch(Chem.MolFromSmarts(patt_deoxyribose))
    
    if not (has_ribose or has_deoxyribose):
        return False, "No ribose/deoxyribose moiety found"

    # Check for purine or pyrimidine base
    base_patterns = [
        'c1ncnc2[nH]cnc12',          # Adenine core
        'c1nc2c([nH]c(=O)[nH]c2=O)n1', # Guanine core
        'c1c[nH]c(=O)[nH]c1=O',      # Uracil core
        'c1c[nH]c(=O)nc1N',          # Cytosine core
        'c1cn([C])c(=O)[nH]c1=O'     # Thymine core
    ]
    
    has_base = False
    for pattern in base_patterns:
        patt = Chem.MolFromSmarts(pattern)
        if mol.HasSubstructMatch(patt):
            has_base = True
            break
            
    if not has_base:
        return False, "No purine/pyrimidine base found"

    # Count phosphate groups
    patt_phosphate_chain = Chem.MolFromSmarts('[P](=O)([O,OH])[O,OH]')
    phosphate_count = len(mol.GetSubstructMatches(patt_phosphate_chain))
    
    if phosphate_count < 1 or phosphate_count > 4:
        return False, "Invalid number of phosphate groups"

    phosphate_types = {1: "mono", 2: "di", 3: "tri", 4: "tetra"}
    sugar_type = "ribose" if has_ribose else "deoxyribose"
    
    return True, f"Nucleoside 5'-{phosphate_types[phosphate_count]}phosphate with {sugar_type}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16701',
                          'name': "nucleoside 5'-phosphate",
                          'definition': 'A ribosyl or deoxyribosyl derivative '
                                        'of a pyrimidine or purine base in '
                                        'which C-5 of the ribose ring is '
                                        'mono-, di-, tri- or '
                                        'tetra-phosphorylated.',
                          'parents': ['CHEBI:29075']},
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
               "[('Cc1cn([C@H]2C[C@H](O)[C@@H](COP(O)([O-])=O)O2)c(=O)[nH]c1=O', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('Nc1ncnc2n(cnc12)[C@H]1C[C@H](O)[C@@H](COP(O)(O)=O)O1', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('C12C(C3(C1N(C(NC3=O)=O)[C@@H]4O[C@@H]([C@H](C4)O)COP(=O)(O)O)C)C(=NC(N2[C@@H]5O[C@@H]([C@H](C5)O)COP(=O)(O)O)=O)N', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('O[C@@H]1[C@@H](COP(O)(O)=O)O[C@H]([C@@H]1O)n1c(cc(=O)[nH]c1=O)C(O)=O', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(O)(=O)OC(=O)CCCCC2CCSS2)[C@@H](O)[C@H]1O', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('C[C@@H](O)[C@H](NC(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12)C(O)=O', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('C(N1C=2C(=NC3=C1C=C(C(=C3)C)N)C(NC(N2)=O)=O)[C@H](O)[C@H](O)[C@H](O)COP(O)(=O)O', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('[C@H]1([C@H](O[C@H]([C@@H]1O)N2C=NC3=C2N=C(NC3=O)N)COP(OP(O)(=O)O)(=O)O)OC(C=4C=CC=CC4NC)=O', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('C[C@@H](O)[C@H](N)C(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('O1[C@@H]([C@H]([C@H]([C@@H]1N2C(NC(C=C2)=O)=O)O)OC(=C)C(=O)O)COP(=O)(O)O', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('NC1=NC=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(O)O)[C@@H](OC([C@H](CC=4N=CNC4)N)=O)[C@H]3O', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('N1=C(C)C(NC(N1[C@@H]2O[C@H](COP(O)(=O)O)[C@H](C2)O)=O)=O', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('O[C@H]1C[C@H]([*])O[C@@H]1COP(O)(=O)OP(O)(=O)OP(O)(O)=O', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('NC1=NC=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(O)O)[C@@H](OC([C@H](C)N)=O)[C@H]3O', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('O[C@@H]1[C@@H](COP(O)(O)=O)O[C@H]([C@@H]1O)n1cnc2cncnc12', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('NC1=NC=NC2=C1N=CN2[C@@H]3O[C@H](COP(=O)(O)O)[C@@H](OC([C@@H]4CCCN4)=O)[C@H]3O', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('O[C@@H]1[C@@H](COP(O)(=O)OP(O)(=O)OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)O[C@H]([C@@H]1O)n1ccc(=O)[nH]c1=O', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('C1=C(CO[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O)O)O)C(NC(N1[C@@H]3O[C@H](COP(=O)(O)O)[C@H](C3)O)=O)=O', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('Nc1ncnc2ncn([C@@H]3O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]3O)c12', "
               "'Invalid ribose/deoxyribose SMARTS patterns'), "
               "('Nc1nc2n(cnc2c(=O)[nH]1)[C@@H]1O[C@H](COP(O)(O)=O)[C@@H](O)[C@H]1O', "
               "'Invalid ribose/deoxyribose SMARTS patterns')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 33,
    'num_true_negatives': 183693,
    'num_false_negatives': 18,
    'num_negatives': None,
    'precision': 0.05714285714285714,
    'recall': 0.1,
    'f1': 0.07272727272727272,
    'accuracy': 0.9997224429375333}