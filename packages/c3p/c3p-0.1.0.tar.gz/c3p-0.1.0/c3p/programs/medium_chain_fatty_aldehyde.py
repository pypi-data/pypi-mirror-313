"""
Classifies: CHEBI:142621 medium-chain fatty aldehyde
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_medium_chain_fatty_aldehyde(smiles: str):
    """
    Determines if a molecule is a medium-chain fatty aldehyde (C6-C12).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a medium-chain fatty aldehyde, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of aldehyde group (C=O)
    aldehyde_pattern = Chem.MolFromSmarts('[CH1](=O)')
    if not mol.HasSubstructMatch(aldehyde_pattern):
        return False, "No aldehyde group found"

    # Count carbons in the main chain
    # First, find the aldehyde carbon
    matches = mol.GetSubstructMatches(aldehyde_pattern)
    if not matches:
        return False, "No aldehyde group found"
    
    aldehyde_carbon = matches[0][0]
    
    # Traverse the molecule from the aldehyde carbon to count the chain length
    visited = set()
    current_atom = mol.GetAtomWithIdx(aldehyde_carbon)
    chain_length = 1  # Start with 1 for the aldehyde carbon
    
    while True:
        # Get non-oxygen neighbors (to follow the carbon chain)
        carbon_neighbors = [neighbor for neighbor in current_atom.GetNeighbors() 
                          if neighbor.GetSymbol() == 'C' and 
                          neighbor.GetIdx() not in visited]
        
        if not carbon_neighbors:
            break
            
        # Follow the longest carbon chain
        current_atom = carbon_neighbors[0]
        visited.add(current_atom.GetIdx())
        chain_length += 1

    if chain_length < 6:
        return False, f"Chain too short (C{chain_length})"
    elif chain_length > 12:
        return False, f"Chain too long (C{chain_length})"
    else:
        # Count double bonds pattern [C]=[C]
        double_bond_pattern = Chem.MolFromSmarts('[C]=[C]')
        double_bonds = len(mol.GetSubstructMatches(double_bond_pattern))
        
        if double_bonds > 0:  # Has additional double bonds besides aldehyde
            return True, f"Unsaturated medium-chain fatty aldehyde (C{chain_length})"
        else:
            return True, f"Saturated medium-chain fatty aldehyde (C{chain_length})"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:142621',
                          'name': 'medium-chain fatty aldehyde',
                          'definition': 'Any fatty aldehyde with a chain '
                                        'length between C6 and C12.',
                          'parents': ['CHEBI:35746']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: module 'rdkit.Chem.rdMolDescriptors' has no "
               "attribute 'CalcNumAliphaticDoubleBonds'",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 12687,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9921807803581203}