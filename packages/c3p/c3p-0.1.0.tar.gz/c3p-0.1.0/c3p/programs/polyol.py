"""
Classifies: CHEBI:26191 polyol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_polyol(smiles: str):
    """
    Determines if a molecule is a polyol (contains 2 or more hydroxy groups).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a polyol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Get all OH groups
    oh_pattern = Chem.MolFromSmarts('[OH]')
    oh_matches = mol.GetSubstructMatches(oh_pattern)
    
    num_oh = len(oh_matches)
    
    if num_oh < 2:
        return False, f"Contains only {num_oh} hydroxy group(s), minimum 2 required"
    
    return True, f"Contains {num_oh} hydroxy groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26191',
                          'name': 'polyol',
                          'definition': 'A compound that contains two or more '
                                        'hydroxy groups.',
                          'parents': ['CHEBI:33822']},
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
    'num_true_positives': 148,
    'num_false_positives': 100,
    'num_true_negatives': 122,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.5967741935483871,
    'recall': 1.0,
    'f1': 0.7474747474747475,
    'accuracy': 0.7297297297297297}