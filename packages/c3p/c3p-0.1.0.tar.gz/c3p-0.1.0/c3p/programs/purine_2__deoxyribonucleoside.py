"""
Classifies: CHEBI:19254 purine 2'-deoxyribonucleoside
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_purine_2__deoxyribonucleoside(smiles: str):
    """
    Determines if a molecule is a purine 2'-deoxyribonucleoside.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a purine 2'-deoxyribonucleoside, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for 2'-deoxyribose moiety
    deoxyribose_pattern = Chem.MolFromSmarts("[CH2]1[CH]([OH])[CH]([CH2][OH])[O][CH]1")
    if not mol.HasSubstructMatch(deoxyribose_pattern):
        return False, "No 2'-deoxyribose moiety found"

    # Check for purine core structure with N-glycosidic bond to deoxyribose
    purine_pattern1 = Chem.MolFromSmarts("[CH2]1[CH]([OH])[CH]([CH2][OH])[O][CH]1n2cnc3c2ncnc3") # Adenine core
    purine_pattern2 = Chem.MolFromSmarts("[CH2]1[CH]([OH])[CH]([CH2][OH])[O][CH]1n2cnc3c2nc[nH]c3=O") # Guanine/inosine core
    
    if mol.HasSubstructMatch(purine_pattern1):
        return True, "Purine 2'-deoxyribonucleoside with adenine core"
    elif mol.HasSubstructMatch(purine_pattern2):
        return True, "Purine 2'-deoxyribonucleoside with guanine/inosine core"
    else:
        return False, "No purine core with correct N-glycosidic linkage found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:19254',
                          'name': "purine 2'-deoxyribonucleoside",
                          'definition': "A 2'-deoxyribonucleoside that has a "
                                        'purine moiety as the nucleobase (the '
                                        'R group in the illustration).',
                          'parents': ['CHEBI:18274', 'CHEBI:60173']},
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
               "[('C[C@@H](Nc1nc2n(cnc2c(=O)[nH]1)[C@H]1C[C@H](O)[C@@H](CO)O1)C(O)=O', "
               "'No purine core structure found'), "
               "('OC[C@H]1O[C@H](C[C@@H]1O)n1cnc2c1nc[nH]c2=O', 'No purine "
               "core structure found')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 11,
    'num_true_negatives': 183898,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.15384615384615385,
    'recall': 1.0,
    'f1': 0.2666666666666667,
    'accuracy': 0.9999401884607229}