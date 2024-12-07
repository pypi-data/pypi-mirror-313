"""
Classifies: CHEBI:13643 glycol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_glycol(smiles: str):
    """
    Determines if a molecule is a glycol (diol with hydroxy groups on different carbons).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glycol, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Find all OH groups
    oh_pattern = Chem.MolFromSmarts("[OH]")
    oh_matches = mol.GetSubstructMatches(oh_pattern)
    
    if len(oh_matches) < 2:
        return False, "Less than 2 OH groups found"
        
    # Get carbons attached to OH groups
    oh_carbons = set()
    for match in oh_matches:
        oh_oxygen = mol.GetAtomWithIdx(match[0])
        for neighbor in oh_oxygen.GetNeighbors():
            if neighbor.GetSymbol() == 'C':
                oh_carbons.add(neighbor.GetIdx())
                
    # Check if OH groups are on different carbons
    if len(oh_carbons) < 2:
        return False, "OH groups are on the same carbon"
        
    # Find shortest path between OH carbons to check if they are adjacent
    paths = []
    oh_carbons_list = list(oh_carbons)
    for i in range(len(oh_carbons_list)):
        for j in range(i+1, len(oh_carbons_list)):
            path = Chem.GetShortestPath(mol, oh_carbons_list[i], oh_carbons_list[j])
            if path:
                paths.append(len(path)-1)
    
    min_distance = min(paths) if paths else 0
    
    if min_distance == 1:
        return True, "Glycol with adjacent OH groups"
    elif min_distance > 1:
        return True, f"Glycol with OH groups separated by {min_distance-1} carbon(s)"
    else:
        return False, "OH groups are not properly connected"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:13643',
                          'name': 'glycol',
                          'definition': 'A diol in which the two hydroxy '
                                        'groups are on different carbon atoms, '
                                        'usually but not necessarily adjacent.',
                          'parents': ['CHEBI:23824']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: cannot import name 'rdDecomposition' from "
               "'rdkit.Chem' "
               '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 10,
    'num_false_positives': 100,
    'num_true_negatives': 150,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.09090909090909091,
    'recall': 1.0,
    'f1': 0.16666666666666669,
    'accuracy': 0.6153846153846154}