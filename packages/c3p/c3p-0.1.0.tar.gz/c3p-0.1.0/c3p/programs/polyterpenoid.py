"""
Classifies: CHEBI:26207 polyterpenoid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_polyterpenoid(smiles: str):
    """
    Determines if a molecule is a polyterpenoid (C5n skeleton where n > 8).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a polyterpenoid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Get number of carbons
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    
    # Check if number of carbons is divisible by 5 (C5n)
    if num_carbons % 5 != 0:
        return False, f"Number of carbons ({num_carbons}) is not divisible by 5"
        
    # Calculate n from C5n
    n = num_carbons / 5
    
    # Check if n > 8 for polyterpenoid
    if n <= 8:
        return False, f"n = {n} is not greater than 8 (C{num_carbons} skeleton)"
        
    # Check for presence of isoprene units (branched 5-carbon units)
    # Look for methyl branches which are characteristic of terpenes
    methyl_count = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            # Count carbons with single methyl group
            if len([n for n in atom.GetNeighbors() if n.GetSymbol() == 'C' and n.GetDegree() == 1]) == 1:
                methyl_count += 1
                
    if methyl_count < n: # Should have roughly one methyl per isoprene unit
        return False, f"Insufficient methyl branches ({methyl_count}) for a terpenoid structure"
    
    # Additional check for presence of oxygen (most terpenoids are oxygenated)
    has_oxygen = any(atom.GetSymbol() == 'O' for atom in mol.GetAtoms())
    
    return True, f"Polyterpenoid with C{num_carbons} skeleton (n={n}){' containing oxygen' if has_oxygen else ''}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26207',
                          'name': 'polyterpenoid',
                          'definition': 'A polymeric terpenoid having a C5n '
                                        'skeleton, where n is greater than 8.',
                          'parents': ['CHEBI:26873']},
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
    'num_true_positives': 2,
    'num_false_positives': 55,
    'num_true_negatives': 183847,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.03508771929824561,
    'recall': 0.6666666666666666,
    'f1': 0.06666666666666667,
    'accuracy': 0.9996954949566352}