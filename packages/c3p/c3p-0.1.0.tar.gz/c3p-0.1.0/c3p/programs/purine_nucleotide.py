"""
Classifies: CHEBI:26395 purine nucleotide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_purine_nucleotide(smiles: str):
    """
    Determines if a molecule is a purine nucleotide.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a purine nucleotide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of phosphate group
    phosphate_pattern = Chem.MolFromSmarts('[P](=[O])([O,OH])[O,OH]')
    if not mol.HasSubstructMatch(phosphate_pattern):
        return False, "No phosphate group found"

    # Check for ribose/deoxyribose sugar
    sugar_pattern = Chem.MolFromSmarts('[CH2]O[CH]1[CH][CH][CH]([CH]1)N')
    if not mol.HasSubstructMatch(sugar_pattern):
        return False, "No ribose/deoxyribose sugar found"

    # Check for purine base (adenine or guanine pattern)
    adenine_pattern = Chem.MolFromSmarts('c1nc(N)nc2c1ncn2')
    guanine_pattern = Chem.MolFromSmarts('c1nc(N)c2c(n1)N=CN2')
    
    has_adenine = mol.HasSubstructMatch(adenine_pattern)
    has_guanine = mol.HasSubstructMatch(guanine_pattern)
    
    if not (has_adenine or has_guanine):
        return False, "No purine base (adenine/guanine) found"

    if has_adenine and has_guanine:
        return True, "Contains both adenine and guanine bases"
    elif has_adenine:
        return True, "Contains adenine base"
    else:
        return True, "Contains guanine base"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26395',
                          'name': 'purine nucleotide',
                          'definition': 'Any nucleotide that has a purine '
                                        'nucleobase.',
                          'parents': ['CHEBI:26401', 'CHEBI:36976']},
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
    'num_true_negatives': 183692,
    'num_false_negatives': 24,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9998693635829214}