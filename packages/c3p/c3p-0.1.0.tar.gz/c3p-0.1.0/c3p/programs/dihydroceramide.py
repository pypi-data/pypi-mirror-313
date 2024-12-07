"""
Classifies: CHEBI:139048 dihydroceramide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole

def is_dihydroceramide(smiles: str):
    """
    Determines if a molecule is a dihydroceramide based on structural features.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a dihydroceramide, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for amide group (NC=O)
    amide_pattern = Chem.MolFromSmarts('[NH]-[C;X3]=[O;X1]')
    if not mol.HasSubstructMatch(amide_pattern):
        return False, "Missing required amide group"
        
    # Check for alcohol groups
    alcohol_pattern = Chem.MolFromSmarts('[CH]-[OH]')
    alcohol_matches = mol.GetSubstructMatches(alcohol_pattern)
    if len(alcohol_matches) < 1:
        return False, "Missing required alcohol group"
        
    # Check for primary alcohol (CH2-OH)
    primary_alcohol = Chem.MolFromSmarts('[CH2]-[OH]')
    if not mol.HasSubstructMatch(primary_alcohol):
        return False, "Missing required primary alcohol group"
        
    # Check for long alkyl chains
    carbon_chain = Chem.MolFromSmarts('CCCC')
    if not mol.HasSubstructMatch(carbon_chain):
        return False, "Missing required long alkyl chains"

    # Check for basic dihydroceramide core structure
    core_pattern = Chem.MolFromSmarts('[CH2][OH].[CH]([CH2]*)[NH]C(=O)*.[CH]([OH])[CH2]*')
    if not mol.HasSubstructMatch(core_pattern):
        return False, "Does not match dihydroceramide core structure"

    # If all checks pass, it's likely a dihydroceramide
    return True, "Matches dihydroceramide structural features"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139048',
                          'name': 'dihydroceramide',
                          'definition': 'An N-acylsphingoid obtained by formal '
                                        'condensation of the carboxy group of '
                                        'any fatty acid with the amino group '
                                        'of any dihydrosphingoid base.',
                          'parents': ['CHEBI:83273']},
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
    'num_false_positives': 100,
    'num_true_negatives': 7305,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9852980847046129}