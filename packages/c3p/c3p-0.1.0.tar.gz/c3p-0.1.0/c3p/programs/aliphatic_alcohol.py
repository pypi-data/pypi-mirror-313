"""
Classifies: CHEBI:2571 aliphatic alcohol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_aliphatic_alcohol(smiles: str):
    """
    Determines if a molecule contains an aliphatic alcohol group.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains aliphatic alcohol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
    
    # Find all OH groups
    oh_matches = mol.GetSubstructMatches(Chem.MolFromSmarts('[OH1]'))
    if not oh_matches:
        return False, "No hydroxyl groups found"
        
    # For each OH group, check if it's attached to an aliphatic carbon
    for match in oh_matches:
        oh_atom = mol.GetAtomWithIdx(match[0])
        carbon_neighbor = None
        
        # Get the carbon atom attached to OH
        for neighbor in oh_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'C':
                carbon_neighbor = neighbor
                break
                
        if carbon_neighbor is None:
            continue
            
        # Check if carbon is aliphatic (not aromatic)
        if not carbon_neighbor.GetIsAromatic():
            # Count the number of aliphatic alcohols found
            n_aliphatic_oh = sum(1 for m in oh_matches 
                               if not mol.GetAtomWithIdx(m[0]).GetNeighbors()[0].GetIsAromatic())
            return True, f"Contains {n_aliphatic_oh} aliphatic hydroxyl group(s)"
            
    return False, "No aliphatic hydroxyl groups found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:2571',
                          'name': 'aliphatic alcohol',
                          'definition': 'An  alcohol derived from an aliphatic '
                                        'compound.',
                          'parents': ['CHEBI:30879']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: 'Atom' object has no attribute "
               "'GetIsConjugated'",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 90,
    'num_false_positives': 100,
    'num_true_negatives': 73,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.47368421052631576,
    'recall': 1.0,
    'f1': 0.6428571428571429,
    'accuracy': 0.6197718631178707}