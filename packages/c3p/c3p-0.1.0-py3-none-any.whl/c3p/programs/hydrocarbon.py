"""
Classifies: CHEBI:24632 hydrocarbon
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydrocarbon(smiles: str):
    """
    Determines if a molecule is a hydrocarbon (contains only carbon and hydrogen atoms).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydrocarbon, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Get all atoms
    atoms = mol.GetAtoms()
    
    # Check that all atoms are either carbon or hydrogen
    for atom in atoms:
        if atom.GetSymbol() not in ['C', 'H']:
            return False, f"Contains non-hydrocarbon atom: {atom.GetSymbol()}"
            
    # If we get here, all atoms are C or H
    return True, "Contains only carbon and hydrogen atoms"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24632',
                          'name': 'hydrocarbon',
                          'definition': 'A compound consisting of carbon and '
                                        'hydrogen only.',
                          'parents': ['CHEBI:33245']},
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
    'num_true_positives': 99,
    'num_false_positives': 100,
    'num_true_negatives': 41820,
    'num_false_negatives': 51,
    'num_negatives': None,
    'precision': 0.49748743718592964,
    'recall': 0.66,
    'f1': 0.5673352435530086,
    'accuracy': 0.9964107439980984}