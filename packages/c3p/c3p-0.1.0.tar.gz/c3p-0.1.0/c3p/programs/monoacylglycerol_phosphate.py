"""
Classifies: CHEBI:16961 monoacylglycerol phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_monoacylglycerol_phosphate(smiles: str):
    """
    Determines if a molecule is a monoacylglycerol phosphate.
    These are derivatives of phosphoglycerols with only one fatty acid ester linkage.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a monoacylglycerol phosphate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for phosphate group
    phosphate_pattern = Chem.MolFromSmarts('[P](=O)([O,OH])[O,OH]')
    if not mol.HasSubstructMatch(phosphate_pattern):
        return False, "No phosphate group found"

    # Check for glycerol backbone
    glycerol_pattern = Chem.MolFromSmarts('[CH2][CH][CH2]')
    if not mol.HasSubstructMatch(glycerol_pattern):
        return False, "No glycerol backbone found"

    # Check for ester linkage
    ester_pattern = Chem.MolFromSmarts('[C](=O)[O][CH2,CH]')
    ester_matches = mol.GetSubstructMatches(ester_pattern)
    
    if len(ester_matches) == 0:
        return False, "No ester linkages found"
    elif len(ester_matches) > 1:
        return False, "More than one ester linkage found - not a monoacylglycerol phosphate"

    # Check for fatty acid chain (carbon chain of length >= 4)
    fatty_acid_pattern = Chem.MolFromSmarts('CC(=O)O[CH2,CH]')
    if not mol.HasSubstructMatch(fatty_acid_pattern):
        return False, "No fatty acid chain found"

    # If all checks pass, it's a monoacylglycerol phosphate
    return True, "Molecule contains one fatty acid ester linkage, glycerol backbone, and phosphate group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16961',
                          'name': 'monoacylglycerol phosphate',
                          'definition': 'Derivatives of phosphoglycerols which '
                                        'have only one of the alcohol groups '
                                        'of the glycerol backbone ester-linked '
                                        'with a fatty acid.',
                          'parents': ['CHEBI:26707', 'CHEBI:37739']},
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
    'num_true_positives': 9,
    'num_false_positives': 100,
    'num_true_negatives': 17242,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.08256880733944955,
    'recall': 0.6923076923076923,
    'f1': 0.1475409836065574,
    'accuracy': 0.9940074906367041}