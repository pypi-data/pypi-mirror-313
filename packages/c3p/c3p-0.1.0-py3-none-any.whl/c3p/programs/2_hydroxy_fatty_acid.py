"""
Classifies: CHEBI:10283 2-hydroxy fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_2_hydroxy_fatty_acid(smiles: str):
    """
    Determines if a molecule is a 2-hydroxy fatty acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 2-hydroxy fatty acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)O')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"
        
    # Check for 2-hydroxy group (alpha position)
    hydroxy_pattern = Chem.MolFromSmarts('OC(C(=O)O)')
    if not mol.HasSubstructMatch(hydroxy_pattern):
        return False, "No hydroxy group in alpha position"
    
    # Check for aliphatic chain
    # Get the carbon atom of the carboxylic group
    matches = mol.GetSubstructMatches(carboxylic_pattern)
    if not matches:
        return False, "Could not find carboxylic carbon"
        
    carboxylic_carbon = matches[0][0]
    
    # Count carbons in the main chain
    visited = set()
    def count_chain_carbons(atom_idx):
        if atom_idx in visited:
            return 0
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetSymbol() != 'C':
            return 0
        visited.add(atom_idx)
        max_branch = 0
        for neighbor in atom.GetNeighbors():
            if neighbor.GetSymbol() == 'C':
                branch_length = count_chain_carbons(neighbor.GetIdx())
                max_branch = max(max_branch, branch_length)
        return max_branch + 1
    
    chain_length = count_chain_carbons(carboxylic_carbon)
    
    if chain_length < 2:
        return False, "Carbon chain too short for fatty acid"
        
    # Check if molecule has aromatic rings (fatty acids shouldn't have them)
    aromatic_atoms = [atom.GetIsAromatic() for atom in mol.GetAtoms()]
    if any(aromatic_atoms):
        return False, "Contains aromatic rings"
        
    return True, f"2-hydroxy fatty acid with approximately {chain_length} carbons in longest chain"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:10283',
                          'name': '2-hydroxy fatty acid',
                          'definition': 'Any fatty acid with a hydroxy '
                                        'functional group in the alpha- or '
                                        '2-position.',
                          'parents': ['CHEBI:24654', 'CHEBI:49302']},
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
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 2439,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.960691823899371}