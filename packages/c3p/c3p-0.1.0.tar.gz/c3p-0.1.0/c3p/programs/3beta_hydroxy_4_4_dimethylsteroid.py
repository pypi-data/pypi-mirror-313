"""
Classifies: CHEBI:143563 3beta-hydroxy-4,4-dimethylsteroid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetBestRMS

def is_3beta_hydroxy_4_4_dimethylsteroid(smiles: str):
    """
    Determines if a molecule is a 3beta-hydroxy-4,4-dimethylsteroid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule matches the pattern, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Define SMARTS pattern for steroid core with 3beta-OH and 4,4-dimethyl
    # Note: The pattern looks for:
    # - Basic steroid skeleton
    # - 3-beta hydroxyl group 
    # - Two methyl groups at position 4
    pattern = Chem.MolFromSmarts('[H][C@@]12CC[C@]3([H])[C@]1([H])CC[C@@]1([H])[C@@]4([H])CC[C@H](O)[C@](C)(C)[C@]4([H])CC[C@@]13C)[C@@]2([H])')
    
    if pattern is None:
        return None, "Invalid SMARTS pattern"

    # Check for matches
    matches = mol.GetSubstructMatches(pattern)
    
    if not matches:
        return False, "Does not contain required 3beta-hydroxy-4,4-dimethylsteroid core structure"
        
    return True, "Contains 3beta-hydroxy-4,4-dimethylsteroid core structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:143563',
                          'name': '3beta-hydroxy-4,4-dimethylsteroid',
                          'definition': 'Any 3beta-hydroxy steroid which is '
                                        'substituted by two methyl groups at '
                                        'position 4.',
                          'parents': ['CHEBI:36836']},
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
    'num_true_negatives': 183913,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999891254111953}