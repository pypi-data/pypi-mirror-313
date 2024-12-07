"""
Classifies: CHEBI:26218 potassium salt
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_potassium_salt(smiles: str):
    """
    Determines if a molecule is a potassium salt (contains K+ cation).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a potassium salt, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for presence of K+ cation
    has_k_plus = False
    has_anion = False
    
    for atom in mol.GetAtoms():
        # Check for K+
        if atom.GetSymbol() == 'K' and atom.GetFormalCharge() == 1:
            has_k_plus = True
            
        # Check for negative charges indicating anion
        if atom.GetFormalCharge() == -1:
            has_anion = True
            
    if not has_k_plus:
        return False, "No K+ cation found"
        
    if not has_anion:
        return False, "No anion found"
        
    # Count formal charges
    total_pos_charge = sum(atom.GetFormalCharge() for atom in mol.GetAtoms() if atom.GetFormalCharge() > 0)
    total_neg_charge = abs(sum(atom.GetFormalCharge() for atom in mol.GetAtoms() if atom.GetFormalCharge() < 0))
    
    if total_pos_charge != total_neg_charge:
        return False, "Unbalanced charges - not a valid salt"
        
    return True, "Valid potassium salt - contains K+ cation and balanced anion"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26218',
                          'name': 'potassium salt',
                          'definition': 'Any alkali metal salt having '
                                        'potassium(1+) as the cation.',
                          'parents': ['CHEBI:26217', 'CHEBI:35479']},
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
    'num_true_positives': 7,
    'num_false_positives': 27,
    'num_true_negatives': 183831,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.20588235294117646,
    'recall': 1.0,
    'f1': 0.34146341463414637,
    'accuracy': 0.9998531531286542}