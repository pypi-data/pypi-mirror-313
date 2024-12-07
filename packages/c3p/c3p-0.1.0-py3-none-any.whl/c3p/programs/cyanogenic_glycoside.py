"""
Classifies: CHEBI:23436 cyanogenic glycoside
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole

def is_cyanogenic_glycoside(smiles: str):
    """
    Determines if a molecule is a cyanogenic glycoside.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a cyanogenic glycoside, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for presence of glycoside (cyclic ether with multiple OH groups)
    # SMARTS pattern for pyranose ring
    pyranose_pattern = "[OX2r6]1[CR4r6][CR4r6][CR4r6][CR4r6][CR4r6]1"
    has_pyranose = len(mol.GetSubstructMatches(Chem.MolFromSmarts(pyranose_pattern))) > 0
    
    # Check for hydroxyl groups
    oh_pattern = "[OH]"
    has_hydroxyls = len(mol.GetSubstructMatches(Chem.MolFromSmarts(oh_pattern))) >= 3
    
    # Check for nitrile (C#N) group
    nitrile_pattern = "C#N" 
    has_nitrile = len(mol.GetSubstructMatches(Chem.MolFromSmarts(nitrile_pattern))) > 0
    
    # Check for O-glycosidic bond
    glycosidic_pattern = "[CR4][OX2][CR4]"
    has_glycosidic = len(mol.GetSubstructMatches(Chem.MolFromSmarts(glycosidic_pattern))) > 0

    if not has_pyranose:
        return False, "Missing pyranose ring structure"
        
    if not has_hydroxyls:
        return False, "Insufficient hydroxyl groups"
        
    if not has_nitrile:
        return False, "Missing nitrile (C#N) group"
        
    if not has_glycosidic:
        return False, "Missing O-glycosidic bond"
        
    # If all required structural features are present
    if has_pyranose and has_hydroxyls and has_nitrile and has_glycosidic:
        return True, "Contains pyranose ring, multiple hydroxyl groups, nitrile group and O-glycosidic bond"
        
    return False, "Does not meet all structural requirements"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23436',
                          'name': 'cyanogenic glycoside',
                          'definition': 'A glycoside in which the aglycone '
                                        'contains a cyanide group. A '
                                        'cyanogenic glycoside can release '
                                        'poisonous hydrogen cyanide if acted '
                                        'upon by some enzyme.',
                          'parents': ['CHEBI:18379', 'CHEBI:24400']},
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
    'num_true_negatives': 183899,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.999983686963709}