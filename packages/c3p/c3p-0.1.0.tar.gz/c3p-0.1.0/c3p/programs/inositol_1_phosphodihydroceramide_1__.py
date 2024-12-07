"""
Classifies: CHEBI:139052 inositol-1-phosphodihydroceramide(1-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_inositol_1_phosphodihydroceramide_1__(smiles: str):
    """
    Determines if a molecule is an inositol-1-phosphodihydroceramide(1-).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an inositol-1-phosphodihydroceramide(1-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of inositol ring with correct stereochemistry
    inositol_pattern = Chem.MolFromSmarts('[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O')
    if not mol.HasSubstructMatch(inositol_pattern):
        return False, "No inositol ring with correct stereochemistry found"

    # Check for phosphate group with negative charge
    phosphate_pattern = Chem.MolFromSmarts('OP([O-])(=O)O')
    if not mol.HasSubstructMatch(phosphate_pattern):
        return False, "No phosphate group with negative charge found"

    # Check for ceramide backbone
    ceramide_pattern = Chem.MolFromSmarts('[C,H][C@H](O)[C@H](COP([O-])(=O)O)NC(=O)[C,*]')
    if not mol.HasSubstructMatch(ceramide_pattern):
        return False, "No ceramide backbone with correct stereochemistry found"

    # Check for specific connection between phosphate and inositol
    phosphoinositol_pattern = Chem.MolFromSmarts('O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1OP([O-])(=O)O')
    if not mol.HasSubstructMatch(phosphoinositol_pattern):
        return False, "Incorrect connection between phosphate and inositol"

    # All required structural features found with correct connectivity
    return True, "Contains inositol ring, phosphate group, and ceramide backbone with correct connectivity"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139052',
                          'name': 'inositol-1-phosphodihydroceramide(1-)',
                          'definition': 'An inositol phosphoceramide(1-) '
                                        'obtained by deprotonation of the free '
                                        'phosphate OH group of any '
                                        'inositol-1-phosphodihydroceramide; '
                                        'major species at pH 7.3.',
                          'parents': ['CHEBI:64916']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: 'Mol' object has no attribute "
               "'HasSubstructMatches'",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 3,
    'num_false_positives': 79,
    'num_true_negatives': 183833,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.036585365853658534,
    'recall': 1.0,
    'f1': 0.07058823529411765,
    'accuracy': 0.9995704537422179}