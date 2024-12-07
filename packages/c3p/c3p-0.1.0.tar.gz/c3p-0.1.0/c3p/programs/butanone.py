"""
Classifies: CHEBI:22951 butanone
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_butanone(smiles: str):
    """
    Determines if a molecule is a butanone (ketone with a butane chain and oxo group).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a butanone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Look for ketone groups (C=O)
    pattern = Chem.MolFromSmarts('[C;!$(C=O)]-C(=O)-[C;!$(C=O)]')
    matches = mol.GetSubstructMatches(pattern)
    
    if not matches:
        return False, "No ketone group found"
        
    for match in matches:
        # Get the carbon atoms connected to the carbonyl carbon
        carbonyl_carbon = mol.GetAtomWithIdx(match[1])
        neighbors = [n.GetIdx() for n in carbonyl_carbon.GetNeighbors() if n.GetAtomicNum() == 6]
        
        for neighbor in neighbors:
            # Try to find a chain of 4 carbons including the carbonyl carbon
            visited = set([match[1]])  # Start with carbonyl carbon
            current = neighbor
            chain_length = 1
            
            while chain_length < 4:
                visited.add(current)
                next_carbons = [n.GetIdx() for n in mol.GetAtomWithIdx(current).GetNeighbors() 
                              if n.GetAtomicNum() == 6 and n.GetIdx() not in visited]
                
                if not next_carbons:
                    break
                    
                current = next_carbons[0]
                chain_length += 1
                
            if chain_length == 4:
                return True, "Found butanone structure: 4-carbon chain with ketone group"
                
    return False, "No butanone structure found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22951',
                          'name': 'butanone',
                          'definition': 'Any  ketone that is butane '
                                        'substituted by an oxo group at '
                                        'unspecified position.',
                          'parents': ['CHEBI:17087']},
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
    'num_true_positives': 0,
    'num_false_positives': 100,
    'num_true_negatives': 1017,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9080357142857143}