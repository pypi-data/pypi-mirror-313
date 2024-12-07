"""
Classifies: CHEBI:19569 2-deoxyribose phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_2_deoxyribose_phosphate(smiles: str):
    """
    Determines if a molecule contains a 2-deoxyribose phosphate moiety.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains 2-deoxyribose phosphate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS patterns for 2-deoxyribose phosphate
    # Matches furanose ring with:
    # - No OH/O at C2 position (2-deoxy)
    # - OH at C3 position
    # - Phosphate group at C5 position
    # Multiple patterns to catch different stereochemistry
    patterns = [
        # Pattern 1 
        "[O;R1][CH]1C[CH](O)[CH](COP(=O)(O)O)O1",
        # Pattern 2
        "[O;R1][CH]1C[CH](O)[CH](COP(=O)(O)OP(=O)(O)O)O1",
        # Pattern 3
        "[O;R1][CH]1C[CH](O)[CH](COP(=O)(O)OP(=O)(O)OP(=O)(O)O)O1",
        # Pattern 4 - aldehyde form
        "O=CC[CH](O)[CH](COP(=O)(O)O)O"
    ]

    for pattern in patterns:
        if mol.HasSubstructMatch(Chem.MolFromSmarts(pattern)):
            if "OP(=O)(O)OP(=O)(O)OP(=O)(O)O" in smiles:
                return True, "Contains 2-deoxyribose triphosphate"
            elif "OP(=O)(O)OP(=O)(O)O" in smiles:
                return True, "Contains 2-deoxyribose diphosphate" 
            else:
                return True, "Contains 2-deoxyribose monophosphate"

    return False, "Does not contain 2-deoxyribose phosphate structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:19569',
                          'name': '2-deoxyribose phosphate',
                          'definition': 'A deoxyaldopentose phosphate in which '
                                        'the deoxyaldopentose is '
                                        '2-deoxyribose.',
                          'parents': ['CHEBI:23634']},
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
               "[('N1(C2=C(C(=NC=N2)N)N=C1)[C@@H]3O[C@@H]4COP(OP(OC[C@H]5O[C@H]([C@@H]([C@@H]5O)O)O[C@H]4[C@H]3O)(=O)[O-])(=O)[O-]', "
               "'Contains 2-deoxyribose diphosphate'), "
               "('N1(C2=C(C(=NC=N2)N)N=C1)[C@@H]3O[C@@H]4COP(OP(OC[C@H]5O[C@H]([C@@H]([C@@H]5O)O)O[C@@H]3[C@@H]4O)(=O)[O-])(=O)[O-]', "
               "'Contains 2-deoxyribose diphosphate'), "
               "('Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@@H]3OP([O-])(=O)O[C@@H]3[C@@H]2O)[C@@H](O)[C@H]1O', "
               "'Contains 2-deoxyribose diphosphate'), "
               "('P1(OC2C(O)[C@H](OC2O1)COP(OP(OC[C@H]3O[C@@H](N4C5=NC=NC(N)=C5N=C4)[C@H](O)[C@@H]3O)(O)=O)(O)=O)(O)=O', "
               "'Contains 2-deoxyribose diphosphate'), "
               "('Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]2O[C@@H]3OP(O)(=O)O[C@@H]3[C@@H]2O)[C@@H](O)[C@H]1O', "
               "'Contains 2-deoxyribose diphosphate'), "
               "('CC1([NH2+]CCCC[C@@H](C(*)=O)N*)O[C@H]2O[C@@H]([C@@H](O)[C@H]2O1)COP(=O)([O-])OP([O-])(=O)OC[C@H]3O[C@H]([C@H](O)[C@@H]3O)N4C=5N=CN=C(C5N=C4)N', "
               "'Contains 2-deoxyribose diphosphate'), "
               "('O[C@@H]1[C@@H](COP(O)(O)=O)O[C@@H]2OP(O)(=O)O[C@H]12', "
               "'Contains 2-deoxyribose monophosphate'), "
               "('O[C@@H]1[C@@H](COP([O-])([O-])=O)O[C@@H]2OP([O-])(=O)O[C@H]12', "
               "'Contains 2-deoxyribose monophosphate'), "
               "('O(P(OP(=O)(OC[C@H]1O[C@H]([C@@H]([C@@H]1O)O)N2C=NC3=C2N=CN=C3N)[O-])(=O)[O-])C[C@H]4O[C@H]5[C@@H]([C@@H]4O)OC([NH2+]CCCC[C@@H](C(*)=O)N*)(O5)C', "
               "'Contains 2-deoxyribose diphosphate')]\n"
               'False negatives: '
               "[('Nc1ncnc2n([C@H]3C[C@H](O)[C@@H](COP(O)(O)=O)O3)c(O)nc12', "
               "'Does not contain 2-deoxyribose phosphate structure'), "
               "('Cc1cn([C@@H]2C[C@@H](O)[C@H](COP(O)(O)=O)O2)c(=O)[nH]c1=O', "
               "'Does not contain 2-deoxyribose phosphate structure'), "
               "('Cc1cn([C@H]2C[C@H](O)[C@@H](COP(O)(=O)OP(O)(O)=O)O2)c(=O)[nH]c1=O', "
               "'Does not contain 2-deoxyribose phosphate structure'), "
               "('O[C@H](COP(O)(O)=O)[C@@H](O)CC=O', 'Does not contain "
               "2-deoxyribose phosphate structure'), "
               "('Nc1nc2n(cnc2c(=O)[nH]1)[C@H]1C[C@H](O)[C@@H](COP(O)(=O)OP(O)(O)=O)O1', "
               "'Does not contain 2-deoxyribose phosphate structure'), "
               "('O(P(O)(=O)O)C[C@H]1O[C@@H](N2C=C(CCCC(CO)O)C(NC2=O)=O)C[C@@H]1O', "
               "'Does not contain 2-deoxyribose phosphate structure')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 60,
    'num_true_negatives': 183806,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.01639344262295082,
    'recall': 0.16666666666666666,
    'f1': 0.02985074626865672,
    'accuracy': 0.9996464932126696}