"""
Classifies: CHEBI:146181 mannotriose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import BRICS
from rdkit.Chem.Draw import IPythonConsole

def is_mannotriose(smiles: str):
    """
    Determines if a molecule is a mannotriose (trisaccharide of 3 mannose units)
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a mannotriose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check if molecule has expected formula for mannotriose (C18H32O16)
    formula = rdMolDescriptors.CalcMolFormula(mol)
    if formula != "C18H32O16":
        return False, f"Incorrect molecular formula: {formula}, expected C18H32O16"

    # Pattern matching for mannose unit
    mannose_pattern = Chem.MolFromSmarts("[CH2][CH]1O[CH]([CH]([CH]([CH]1O)O)O)O")
    if mannose_pattern is None:
        return None, "Error creating mannose pattern"
        
    # Find all mannose units
    matches = mol.GetSubstructMatches(mannose_pattern)
    
    if len(matches) != 3:
        return False, f"Found {len(matches)} mannose units, expected 3"
    
    # Check if units are connected by glycosidic bonds
    glycosidic_pattern = Chem.MolFromSmarts("[CH]1O[CH][CH][CH][CH][CH]1O[CH]")
    glycosidic_matches = mol.GetSubstructMatches(glycosidic_pattern)
    
    if len(glycosidic_matches) < 2:
        return False, "Mannose units not properly connected by glycosidic bonds"
        
    return True, "Contains 3 mannose units connected by glycosidic bonds"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:146181',
                          'name': 'mannotriose',
                          'definition': 'Any trisaccharide composed of 3 '
                                        'mannose moieties.',
                          'parents': ['CHEBI:25174', 'CHEBI:27150']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
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
    'num_true_negatives': 183911,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999891252929374}