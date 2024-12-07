"""
Classifies: CHEBI:140402 tert-butyl ester
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_tert_butyl_ester(smiles: str):
    """
    Determines if a molecule contains a tert-butyl ester group.
    A tert-butyl ester is a carboxylic ester with a tert-butyl group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains a tert-butyl ester, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for tert-butyl ester: R-C(=O)-O-C(C)(C)C
    # Exclude carbamates and carbonates
    tert_butyl_ester_pattern = Chem.MolFromSmarts('[C,c;!$(C(=O)O);!$(C(=O)N)][CX3](=[OX1])[OX2][CX4;!$(C(O)(O))]([CH3])([CH3])[CH3]')
    
    if tert_butyl_ester_pattern is None:
        return None, "Invalid SMARTS pattern"
        
    matches = mol.GetSubstructMatches(tert_butyl_ester_pattern)
    
    # Check for carbonate groups
    carbonate_pattern = Chem.MolFromSmarts('[OX2][CX3](=[OX1])[OX2]')
    carbonate_matches = mol.GetSubstructMatches(carbonate_pattern) if carbonate_pattern else []
    
    # Filter out matches that are part of a carbonate
    valid_matches = []
    for match in matches:
        is_carbonate = False
        for carbonate in carbonate_matches:
            if match[1] in carbonate:  # Check if carbonyl carbon is part of carbonate
                is_carbonate = True
                break
        if not is_carbonate:
            valid_matches.append(match)
            
    if valid_matches:
        num_matches = len(valid_matches)
        if num_matches == 1:
            return True, "Contains 1 tert-butyl ester group"
        else:
            return True, f"Contains {num_matches} tert-butyl ester groups"
    
    return False, "No tert-butyl ester group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140402',
                          'name': 'tert-butyl ester',
                          'definition': 'A carboxylic ester resulting from the '
                                        'formal condensation of a carboxylic '
                                        'acid with tert-butanol.',
                          'parents': ['CHEBI:33308']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.2857142857142857 is too low.\n'
               "True positives: [('C(OC(C)(C)C)(C=1C=CC=CC1)=O', 'Contains 1 "
               "tert-butyl ester group'), "
               "('CC(C)C[C@@H](C(=O)OC(C)(C)C)NC(=O)C1=C(NC=N1)C(=O)NCC2=CC=CC=C2', "
               "'Contains 1 tert-butyl ester group'), "
               "('CCOC(=O)C1=CC=C(C=C1)NC(=O)C2=C(NC=N2)C(=O)N[C@@H](CCCCNC(=O)OC(C)(C)C)C(=O)OC(C)(C)C', "
               "'Contains 1 tert-butyl ester group')]\n"
               "False positives: [('C(*)(=O)OC(C)(C)C', 'Contains 1 tert-butyl "
               "ester group'), ('O(C(C)(C)C)C(=O)C1=CC(N)=CC=C1', 'Contains 1 "
               "tert-butyl ester group'), ('O(C(C)(C)C)C(=O)C1=CC=C(C=C1)C', "
               "'Contains 1 tert-butyl ester group'), "
               "('CC(C)(C)OC(=O)OC(=O)OC(C)(C)C', 'Contains 2 tert-butyl ester "
               "groups'), "
               "('O(C(=O)[C@H]1N(CCC1)C(=O)[C@@H](N[C@@H](CCC2=CC=CC=C2)C(O)=O)C)C(C)(C)C', "
               "'Contains 1 tert-butyl ester group'), "
               "('O(C(C)(C)C)C(=O)C(NC(=O)CCCCC)C(C)C', 'Contains 1 tert-butyl "
               "ester group'), ('C(OC(C)(C)C)(*)=O', 'Contains 1 tert-butyl "
               "ester group'), ('O(C(C)(C)C)C(=O)[C@@H](N)CCC(=O)N', 'Contains "
               "1 tert-butyl ester group'), "
               "('O(C(C)(C)C)C(=O)[C@H](N)CCC(O)=O', 'Contains 1 tert-butyl "
               "ester group'), "
               "('ClC1=CC=2C3(CCNC3=O)C(=O)N(C2C=C1)CC(OC(C)(C)C)=O', "
               "'Contains 1 tert-butyl ester group'), "
               "('O(C(C)(C)C)C(=O)C1=CC=C(CN2CCN(CC2)C=3C4=C(NC=C4)C=CC3)C=C1', "
               "'Contains 1 tert-butyl ester group'), "
               "('ClC=1SC(C(OC(C)(C)C)=O)=CN1', 'Contains 1 tert-butyl ester "
               "group'), "
               "('O(C(=O)[C@@H]([C@H](N([C@@H](C1=CC=CC=C1)C)CC2=CC=CC=C2)C=3C(N(CC=C)CC=C)=CC=CC3)CC#N)C(C)(C)C', "
               "'Contains 1 tert-butyl ester group'), "
               "('P(C1=CC=CC=C1)(C2=CC=CC=C2)(C3=CC=CC=C3)=CC(OC(C)(C)C)=O', "
               "'Contains 1 tert-butyl ester group'), "
               "('S(C(CC=C)(C1=CC=C(OC)C=C1)C(OC(C)(C)C)=O)CC=C', 'Contains 1 "
               "tert-butyl ester group')]\n"
               'False negatives: []',
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 12,
    'num_true_negatives': 183885,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.2,
    'recall': 1.0,
    'f1': 0.33333333333333337,
    'accuracy': 0.9999347471451876}