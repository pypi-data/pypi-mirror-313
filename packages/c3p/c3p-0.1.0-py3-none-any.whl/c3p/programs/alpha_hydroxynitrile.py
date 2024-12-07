"""
Classifies: CHEBI:22455 alpha-hydroxynitrile
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_alpha_hydroxynitrile(smiles: str):
    """
    Determines if a molecule is an alpha-hydroxynitrile.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an alpha-hydroxynitrile, False otherwise
        str: Reason for classification
    """
    # Create RDKit mol object
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Look for CN triple bond (nitrile group)
    nitrile_pattern = Chem.MolFromSmarts('[C]#N')
    nitrile_matches = mol.GetSubstructMatches(nitrile_pattern)
    
    if not nitrile_matches:
        return False, "No nitrile group found"
        
    # Look for OH group
    hydroxy_pattern = Chem.MolFromSmarts('[OH1]')
    hydroxy_matches = mol.GetSubstructMatches(hydroxy_pattern)
    
    if not hydroxy_matches:
        return False, "No hydroxy group found"
    
    # Check if OH is on carbon alpha to CN
    for nitrile_match in nitrile_matches:
        nitrile_c = nitrile_match[0]  # Get carbon atom index of CN
        
        # Get atom connected to nitrile carbon
        alpha_atom = None
        for atom in mol.GetAtomWithIdx(nitrile_c).GetNeighbors():
            if atom.GetAtomicNum() != 7:  # Not nitrogen
                alpha_atom = atom
                break
                
        if alpha_atom is None:
            continue
            
        # Check if alpha carbon has OH attached
        for neighbor in alpha_atom.GetNeighbors():
            if neighbor.GetAtomicNum() == 8 and neighbor.GetTotalNumHs() == 1:
                return True, "Found hydroxy group on carbon alpha to nitrile"
                
    return False, "Hydroxy group not alpha to nitrile"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22455',
                          'name': 'alpha-hydroxynitrile',
                          'definition': 'A hydroxynitrile in which the hydroxy '
                                        'group is located on the carbon alpha '
                                        'to the carbonitrile group.',
                          'parents': ['CHEBI:24730']},
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
    'num_true_positives': 3,
    'num_false_positives': 9,
    'num_true_negatives': 183888,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.25,
    'recall': 1.0,
    'f1': 0.4,
    'accuracy': 0.9999510603588907}