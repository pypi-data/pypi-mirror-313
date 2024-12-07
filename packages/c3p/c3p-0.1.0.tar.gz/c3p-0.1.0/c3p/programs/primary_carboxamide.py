"""
Classifies: CHEBI:140324 primary carboxamide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_primary_carboxamide(smiles: str):
    """
    Determines if a molecule contains a primary carboxamide group (RC(=O)NH2).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains primary carboxamide, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # SMARTS pattern for primary carboxamide: RC(=O)NH2
    # [CX3](=[OX1])[NX3H2]
    # CX3 = carbon with 3 bonds
    # =OX1 = oxygen double bond
    # NX3H2 = nitrogen with 3 bonds and 2 hydrogens
    pattern = Chem.MolFromSmarts('[CX3](=[OX1])[NX3H2]')
    
    if mol.HasSubstructMatch(pattern):
        # Get number of matches
        matches = mol.GetSubstructMatches(pattern)
        
        if len(matches) == 1:
            return True, "Contains one primary carboxamide group"
        else:
            return True, f"Contains {len(matches)} primary carboxamide groups"
            
    return False, "No primary carboxamide group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140324',
                          'name': 'primary carboxamide',
                          'definition': 'A carboxamide resulting from the '
                                        'formal condensation of a carboxylic '
                                        'acid with ammonia; formula RC(=O)NH2.',
                          'parents': ['CHEBI:37622']},
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
    'num_true_positives': 10,
    'num_false_positives': 100,
    'num_true_negatives': 2674,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.09090909090909091,
    'recall': 1.0,
    'f1': 0.16666666666666669,
    'accuracy': 0.9640804597701149}