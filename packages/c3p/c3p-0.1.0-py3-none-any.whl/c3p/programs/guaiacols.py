"""
Classifies: CHEBI:134251 guaiacols
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_guaiacols(smiles: str):
    """
    Determines if a molecule contains a guaiacol moiety (phenol with methoxy substituent in ortho position).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains guaiacol, False otherwise
        str: Reason for classification
    """
    # Try to create mol object with sanitization
    try:
        mol = Chem.MolFromSmiles(smiles, sanitize=True)
    except:
        return None, "Invalid SMILES string or molecule could not be sanitized"
        
    if mol is None:
        return None, "Invalid SMILES string"

    # SMARTS pattern for guaiacol:
    # Phenol with methoxy in ortho position
    # c: aromatic carbon
    # O: oxygen
    # [CH3]: methyl group
    guaiacol_pattern = '[OH]c1c(OC)cccc1'
    
    try:
        substructure = Chem.MolFromSmarts(guaiacol_pattern)
        if mol.HasSubstructMatch(substructure):
            return True, "Contains guaiacol moiety (phenol with ortho-methoxy group)"
        return False, "Does not contain guaiacol moiety"
    except:
        return None, "Error in substructure matching"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134251',
                          'name': 'guaiacols',
                          'definition': 'Any phenol carrying an additional '
                                        'methoxy substituent at the '
                                        'ortho-position.',
                          'parents': ['CHEBI:25235', 'CHEBI:33853']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: Can't kekulize mol.  Unkekulized atoms: 0 1 2 "
               '3 4 5 6 7 9 10 11 13 14 15 16 18 19 20 21 22 23 24 25 26 27 28 '
               '29 30 31 32 33 34 35 36 37 38 39 41 42 44 45 46 47 48 50 51 53 '
               '54 55 56 57 58 59 60 61 69 70 71 72 73 74 75 76 78 80 81 82 83 '
               '88 89',
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 9,
    'num_false_positives': 100,
    'num_true_negatives': 4478,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.08256880733944955,
    'recall': 1.0,
    'f1': 0.15254237288135594,
    'accuracy': 0.9781992587747983}