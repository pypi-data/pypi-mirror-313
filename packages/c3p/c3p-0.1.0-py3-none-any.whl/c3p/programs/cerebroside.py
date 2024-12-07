"""
Classifies: CHEBI:23079 cerebroside
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole

def is_cerebroside(smiles: str):
    """
    Determines if a molecule is a cerebroside (monoglycosylceramide).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a cerebroside, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of required functional groups
    
    # 1. Must have a sugar moiety (pyranose ring)
    sugar_pattern = '[OX2H1,OX2H0][CH1]1[OX2H0][CH1]([CH2][OX2H1])[CH1]([OX2H1])[CH1]([OX2H1])[CH1]1[OX2H1]'
    sugar_match = mol.HasSubstructMatch(Chem.MolFromSmarts(sugar_pattern))
    if not sugar_match:
        return False, "Missing sugar (glucose/galactose) moiety"

    # 2. Must have an amide linkage
    amide_pattern = '[NX3H1][CX3](=[OX1])[CX4]'
    amide_match = mol.HasSubstructMatch(Chem.MolFromSmarts(amide_pattern))
    if not amide_match:
        return False, "Missing amide linkage"

    # 3. Must have a long alkyl chain
    alkyl_pattern = '[CH2][CH2][CH2][CH2][CH2][CH2]'
    alkyl_match = mol.HasSubstructMatch(Chem.MolFromSmarts(alkyl_pattern))
    if not alkyl_match:
        return False, "Missing long alkyl chain"

    # 4. Must have hydroxyl groups
    hydroxyl_pattern = '[OX2H1]'
    hydroxyl_matches = len(mol.GetSubstructMatches(Chem.MolFromSmarts(hydroxyl_pattern)))
    if hydroxyl_matches < 2:
        return False, "Insufficient hydroxyl groups"

    # 5. Check for glycosidic linkage between sugar and ceramide
    glycosidic_pattern = '[CH2]O[CH1]1O[CH1][CH1][CH1][CH1][CH1]1'
    glycosidic_match = mol.HasSubstructMatch(Chem.MolFromSmarts(glycosidic_pattern))
    if not glycosidic_match:
        return False, "Missing glycosidic linkage"

    return True, "Molecule contains required cerebroside structural features: sugar moiety, amide linkage, long alkyl chain, hydroxyl groups, and glycosidic linkage"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23079',
                          'name': 'cerebroside',
                          'definition': 'Any member of a group of '
                                        'glycosphingolipids, also known as '
                                        'monoglycosylceramides, which are '
                                        'important components in animal muscle '
                                        'and nerve cell membranes.',
                          'parents': ['CHEBI:17761', 'CHEBI:25513']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': None,
    'attempt': 0,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183746,
    'num_false_negatives': 24,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9998694019698536}