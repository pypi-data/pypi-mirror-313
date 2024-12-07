"""
Classifies: CHEBI:176842 vitamin B9
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_vitamin_B9(smiles: str):
    """
    Determines if a molecule is vitamin B9 (folic acid) or a derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is vitamin B9, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for key structural features of vitamin B9
    
    # 1. Must contain pterin core (2-amino-4-oxo-3,4-dihydropteridine)
    # Multiple SMARTS patterns to catch different representations
    pterin_patterns = [
        Chem.MolFromSmarts('c1nc2c(n1)nc([nH]c2=O)N'),  # Basic pattern
        Chem.MolFromSmarts('c1nc2c(nc(N)nc2[nH]1)=O'),  # Alternative pattern
        Chem.MolFromSmarts('N=c1[nH]c(=O)c2nc[nH]c2[nH]1'),  # Another form
        Chem.MolFromSmarts('Nc1nc2NCC3CN(CN3c2c(=O)[nH]1)'),  # THF form
        Chem.MolFromSmarts('Nc1nc2N=CN(CN2c(=O)[nH]1)'),  # Another variant
    ]
    
    has_pterin = any(mol.HasSubstructMatch(pattern) for pattern in pterin_patterns)
    if not has_pterin:
        return False, "Missing pterin core structure"

    # 2. Must contain p-aminobenzoic acid (PABA) moiety with connecting chain
    paba_patterns = [
        Chem.MolFromSmarts('c1ccc(C(=O)NC)cc1'),
        Chem.MolFromSmarts('c1ccc(cc1)C(=O)N[CH]'),
    ]
    
    has_paba = any(mol.HasSubstructMatch(pattern) for pattern in paba_patterns)
    if not has_paba:
        return False, "Missing p-aminobenzoic acid moiety"

    # 3. Must contain glutamic acid moiety (including ionized forms)
    glutamate_patterns = [
        Chem.MolFromSmarts('NC(CCC(=O)O)C(=O)O'),
        Chem.MolFromSmarts('NC(CCC([O-])=O)C([O-])=O'),
        Chem.MolFromSmarts('NCC(CCC(=O)*)C(=O)*'),  # More general pattern
    ]
    
    has_glutamate = any(mol.HasSubstructMatch(pattern) for pattern in glutamate_patterns)
    if not has_glutamate:
        return False, "Missing glutamic acid moiety"

    # If all required structural features are present
    return True, "Contains pterin core, PABA, and glutamate moieties characteristic of vitamin B9"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:176842',
                          'name': 'vitamin B9',
                          'definition': 'Any B-vitamin that exhibits '
                                        'biological activity against vitamin '
                                        'B9 deficiency. Vitamin B9 refers to '
                                        'the many forms of folic acid and its '
                                        'derivatives, including '
                                        'tetrahydrofolic acid (the active '
                                        'form), methyltetrahydrofolate (the '
                                        'primary form found in blood), '
                                        'methenyltetrahydrofolate, folinic '
                                        'acid amongst others. They are present '
                                        'in abundance in green leafy '
                                        'vegetables, citrus fruits, and animal '
                                        'products. Lack of vitamin B9 leads to '
                                        'anemia, a condition in which the body '
                                        'cannot produce sufficient number of '
                                        'red blood cells. Symptoms of vitamin '
                                        'B9 deficiency include fatigue, muscle '
                                        'weakness, and pale skin.',
                          'parents': ['CHEBI:75769']},
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
               "[('[H][C@]12CNc3nc(N)[nH]c(=O)c3[N+]1=CN(C2)c1ccc(cc1)C(=O)N[C@@H](CCC([O-])=O)C([O-])=O', "
               "'Missing pterin core structure'), "
               "('CN(CC1=CN=C2C(=N1)C(=NC(=N2)N)N)C3=CC=C(C=C3)C(=O)NC(CCC(=O)O)C(=O)O', "
               "'Missing pterin core structure'), "
               "('Nc1nc2NCC3CN(CN3c2c(=O)[nH]1)c1ccc(cc1)C(=O)N[C@@H](CCC([O-])=O)C([O-])=O', "
               "'Missing pterin core structure')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 1,
    'num_true_negatives': 183896,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.5,
    'recall': 0.3333333333333333,
    'f1': 0.4,
    'accuracy': 0.9999836867862969}