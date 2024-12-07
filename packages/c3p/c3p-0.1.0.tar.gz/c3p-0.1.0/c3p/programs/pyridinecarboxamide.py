"""
Classifies: CHEBI:25529 pyridinecarboxamide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_pyridinecarboxamide(smiles: str):
    """
    Determines if a molecule is a pyridinecarboxamide (pyridine with at least one carboxamide substituent).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a pyridinecarboxamide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check for pyridine ring
    pyridine_pattern = Chem.MolFromSmarts('n1ccccc1')
    if not mol.HasSubstructMatch(pyridine_pattern):
        return False, "No pyridine ring found"
        
    # Check for carboxamide group attached to pyridine
    # Pattern matches pyridine ring with carboxamide substituent
    pyridine_carboxamide_pattern = Chem.MolFromSmarts('n1ccccc1C(=O)N')
    
    # Also check for N-substituted carboxamide
    n_subst_carboxamide_pattern = Chem.MolFromSmarts('n1ccccc1C(=O)N[#6,#1]')
    
    if not (mol.HasSubstructMatch(pyridine_carboxamide_pattern) or 
            mol.HasSubstructMatch(n_subst_carboxamide_pattern)):
        return False, "No carboxamide substituent found on pyridine ring"
    
    # Get number of matches to report in reason
    matches = len(mol.GetSubstructMatches(pyridine_carboxamide_pattern))
    matches += len(mol.GetSubstructMatches(n_subst_carboxamide_pattern))
    
    return True, f"Pyridine ring found with {matches} carboxamide substituent(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25529',
                          'name': 'pyridinecarboxamide',
                          'definition': 'A member of the class of pyridines '
                                        'that is a substituted pyridine in '
                                        'which at least one of the '
                                        'substituents is a carboxamide or '
                                        'N-substituted caraboxamide group.',
                          'parents': ['CHEBI:26421', 'CHEBI:37622']},
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
    'num_true_positives': 6,
    'num_false_positives': 100,
    'num_true_negatives': 30014,
    'num_false_negatives': 26,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 0.1875,
    'f1': 0.08695652173913045,
    'accuracy': 0.9958203410070988}