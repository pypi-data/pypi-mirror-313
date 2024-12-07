"""
Classifies: CHEBI:139592 tertiary alpha-hydroxy ketone
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_tertiary_alpha_hydroxy_ketone(smiles: str):
    """
    Determines if a molecule contains a tertiary alpha-hydroxy ketone group.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains tertiary alpha-hydroxy ketone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for tertiary alpha-hydroxy ketone:
    # [C;!H3](=O)[C;!H2]([*,#1])([*,#1])[C;!H2]([*,#1])([*,#1])[OH]
    # Explanation:
    # [C;!H3](=O) - carbonyl carbon with no more than 2 hydrogens
    # [C;!H2]([*,#1])([*,#1]) - carbon with two non-H substituents
    # [C;!H2]([*,#1])([*,#1])[OH] - carbon with hydroxyl and two non-H substituents
    pattern = Chem.MolFromSmarts('[C;!H3](=O)[C;!H2]([*,#1])([*,#1])[C;!H2]([*,#1])([*,#1])[OH]')
    
    if pattern is None:
        return None, "Invalid SMARTS pattern"
        
    matches = mol.GetSubstructMatches(pattern)
    
    if matches:
        return True, "Contains tertiary alpha-hydroxy ketone group"
    else:
        return False, "Does not contain tertiary alpha-hydroxy ketone group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139592',
                          'name': 'tertiary alpha-hydroxy ketone',
                          'definition': 'An alpha-hydroxy ketone in which the '
                                        'carbonyl group and the hydroxy group '
                                        'are linked by a carbon bearing two '
                                        'organyl groups.',
                          'parents': ['CHEBI:139588', 'CHEBI:26878']},
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
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 23136,
    'num_false_negatives': 21,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 0.045454545454545456,
    'f1': 0.016260162601626018,
    'accuracy': 0.9947974890360306}