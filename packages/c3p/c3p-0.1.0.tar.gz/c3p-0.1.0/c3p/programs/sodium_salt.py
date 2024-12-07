"""
Classifies: CHEBI:26714 sodium salt
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_sodium_salt(smiles: str):
    """
    Determines if a molecule is a sodium salt (contains Na+ cation).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a sodium salt, False otherwise
        str: Reason for classification
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return False, "Invalid SMILES string"
            
        # Check for presence of Na+ ion
        has_sodium = False
        has_anion = False
        
        for atom in mol.GetAtoms():
            # Check for sodium cation
            if atom.GetSymbol() == 'Na':
                if atom.GetFormalCharge() == 1:
                    has_sodium = True
                    
            # Check for negative charge indicating anion
            if atom.GetFormalCharge() < 0:
                has_anion = True
                
        if not has_sodium:
            return False, "No sodium cation (Na+) found"
            
        if not has_anion:
            return False, "No anion found to form salt"
            
        return True, "Contains Na+ cation and anion"
        
    except Exception as e:
        return None, f"Error processing molecule: {str(e)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26714',
                          'name': 'sodium salt',
                          'definition': 'Any alkali metal salt having '
                                        'sodium(1+) as the cation.',
                          'parents': ['CHEBI:26712', 'CHEBI:35479']},
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
    'num_true_positives': 41,
    'num_false_positives': 100,
    'num_true_negatives': 87997,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.2907801418439716,
    'recall': 1.0,
    'f1': 0.45054945054945056,
    'accuracy': 0.9988654155982664}