"""
Classifies: CHEBI:16799 16alpha-hydroxy steroid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdmolops import GetDistanceMatrix

def is_16alpha_hydroxy_steroid(smiles: str):
    """
    Determines if a molecule is a 16alpha-hydroxy steroid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 16alpha-hydroxy steroid, False otherwise
        str: Reason for classification
    """
    # Create RDKit molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Add hydrogen atoms explicitly
    mol = Chem.AddHs(mol)
    
    # Check for steroid core structure
    steroid_pattern = Chem.MolFromSmarts("[#6]~1~[#6]~[#6]~[#6]~2~[#6]~[#6]~[#6]~3~[#6]~[#6]~[#6]~4~[#6]~[#6]~[#6]~[#6]~4~[#6]~3~[#6]~[#6]~2~1")
    if not mol.HasSubstructMatch(steroid_pattern):
        return False, "Not a steroid - missing core structure"

    # Pattern for 16-OH with alpha stereochemistry
    # Note: The pattern looks for C16-OH with specified stereochemistry
    oh_pattern = Chem.MolFromSmarts('[C@@H]1CC[C@]2([C@H](O)CC[C@@]3([H])[C@@]2([H])CC=C3)C1')
    
    if not mol.HasSubstructMatch(oh_pattern):
        return False, "No 16-alpha hydroxy group found"

    return True, "16-alpha hydroxy steroid identified"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16799',
                          'name': '16alpha-hydroxy steroid',
                          'definition': 'A 16-hydroxy steroid in which the '
                                        'hydroxy group at position 16 has '
                                        'alpha-configuration.',
                          'parents': ['CHEBI:36840']},
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
    'num_true_negatives': 183915,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999891255294507}