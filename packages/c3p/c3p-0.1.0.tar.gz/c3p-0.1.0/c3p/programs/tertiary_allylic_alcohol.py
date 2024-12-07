"""
Classifies: CHEBI:134397 tertiary allylic alcohol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_tertiary_allylic_alcohol(smiles: str):
    """
    Determines if a molecule is a tertiary allylic alcohol.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a tertiary allylic alcohol, False otherwise
        str: Reason for classification
    """
    # Convert SMILES to RDKit molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Find all OH groups
    pattern_oh = Chem.MolFromSmarts("[OH1]")
    oh_matches = mol.GetSubstructMatches(pattern_oh)
    
    if not oh_matches:
        return False, "No hydroxyl group found"
    
    # Find all double bonds
    pattern_db = Chem.MolFromSmarts("C=C")
    db_matches = mol.GetSubstructMatches(pattern_db)
    
    if not db_matches:
        return False, "No carbon-carbon double bond found"
        
    # For each OH group, check if it's attached to a carbon that's:
    # 1. Connected to a carbon involved in a double bond (allylic)
    # 2. Connected to two other carbons (tertiary)
    for oh_match in oh_matches:
        oh_atom = mol.GetAtomWithIdx(oh_match[0])
        c_atom = oh_atom.GetNeighbors()[0]  # Carbon attached to OH
        
        # Check if carbon is tertiary (connected to 3 other atoms)
        if c_atom.GetDegree() != 4:  # Including the OH
            continue
            
        # Count number of carbon neighbors (excluding OH)
        carbon_neighbors = sum(1 for neighbor in c_atom.GetNeighbors() 
                             if neighbor.GetSymbol() == 'C')
        if carbon_neighbors != 3:
            continue
            
        # Check if any of these carbons is connected to a double bond
        for neighbor in c_atom.GetNeighbors():
            if neighbor.GetSymbol() != 'C':
                continue
                
            # Check if this carbon or any of its neighbors is involved in a double bond
            for db_match in db_matches:
                if neighbor.GetIdx() in db_match:
                    return True, "Found tertiary carbon with OH group adjacent to C=C bond"
                
                # Check neighbors of neighbor
                for next_neighbor in neighbor.GetNeighbors():
                    if next_neighbor.GetIdx() in db_match:
                        return True, "Found tertiary carbon with OH group adjacent to C=C bond"
                    
    return False, "No tertiary allylic alcohol pattern found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134397',
                          'name': 'tertiary allylic alcohol',
                          'definition': 'An allylic alcohol in which the '
                                        'carbon atom that links the double '
                                        'bond to the hydroxy group is also '
                                        'attached to two other carbons (R4,R5 '
                                        '=/= H).',
                          'parents': ['CHEBI:134361', 'CHEBI:26878']},
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
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 3971,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9754480726737049}