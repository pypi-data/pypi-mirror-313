"""
Classifies: CHEBI:25754 oxo carboxylic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_oxo_carboxylic_acid(smiles: str):
    """
    Determines if a molecule is an oxo carboxylic acid (contains both a carboxylic acid group
    and an aldehyde/ketone group).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an oxo carboxylic acid, False otherwise
        str: Reason for classification
    """
    # Create RDKit molecule object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxylic_acid_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
    has_carboxylic_acid = len(mol.GetSubstructMatches(carboxylic_acid_pattern)) > 0
    
    if not has_carboxylic_acid:
        return False, "No carboxylic acid group found"

    # Check for aldehyde group
    aldehyde_pattern = Chem.MolFromSmarts('[CX3H1](=O)[#6]')
    has_aldehyde = len(mol.GetSubstructMatches(aldehyde_pattern)) > 0

    # Check for ketone group 
    ketone_pattern = Chem.MolFromSmarts('[#6][CX3](=O)[#6]')
    has_ketone = len(mol.GetSubstructMatches(ketone_pattern)) > 0

    if not (has_aldehyde or has_ketone):
        return False, "No aldehyde or ketone group found"

    # Determine which oxo groups are present
    oxo_groups = []
    if has_aldehyde:
        oxo_groups.append("aldehyde")
    if has_ketone:
        oxo_groups.append("ketone")
        
    return True, f"Contains carboxylic acid and {' and '.join(oxo_groups)} groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25754',
                          'name': 'oxo carboxylic acid',
                          'definition': 'Any compound that has an aldehydic or '
                                        'ketonic group as well as a carboxylic '
                                        'acid group in the same molecule.',
                          'parents': ['CHEBI:33575']},
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
    'num_true_positives': 53,
    'num_false_positives': 100,
    'num_true_negatives': 4514,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 0.3464052287581699,
    'recall': 0.8412698412698413,
    'f1': 0.49074074074074076,
    'accuracy': 0.9764806499893094}