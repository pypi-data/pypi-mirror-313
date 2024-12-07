"""
Classifies: CHEBI:22527 aminopurine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdDecomposition

def is_aminopurine(smiles: str):
    """
    Determines if a molecule is an aminopurine (any purine having at least one amino substituent).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an aminopurine, False otherwise
        str: Reason for classification
    """
    
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check for purine scaffold
    purine_smarts = 'c1nc2c([nH]1)ncnc2'
    purine_pattern = Chem.MolFromSmarts(purine_smarts)
    
    if not mol.HasSubstructMatch(purine_pattern):
        return False, "No purine scaffold found"
        
    # Check for amino group attached to purine
    amino_purine_smarts = '[NX3H2]-c1nc2c(n1)ncnc2'
    amino_purine_pattern = Chem.MolFromSmarts(amino_purine_smarts)
    
    if mol.HasSubstructMatch(amino_purine_pattern):
        return True, "Contains purine scaffold with amino substituent"
        
    # Also check for substituted amino groups
    subst_amino_purine_smarts = '[NX3H1;!$(NC=O)]-c1nc2c(n1)ncnc2'
    subst_amino_purine_pattern = Chem.MolFromSmarts(subst_amino_purine_smarts)
    
    if mol.HasSubstructMatch(subst_amino_purine_pattern):
        return True, "Contains purine scaffold with substituted amino group"
        
    return False, "No amino substituent found on purine scaffold"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22527',
                          'name': 'aminopurine',
                          'definition': 'Any purine having at least one amino '
                                        'substituent.',
                          'parents': ['CHEBI:26401']},
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
    'success': False,
    'best': True,
    'error': "cannot import name 'rdDecomposition' from 'rdkit.Chem' "
             '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}