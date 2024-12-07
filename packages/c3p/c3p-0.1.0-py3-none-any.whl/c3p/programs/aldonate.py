"""
Classifies: CHEBI:22299 aldonate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMolFrags

def is_aldonate(smiles: str):
    """
    Determines if a molecule is an aldonate (deprotonated aldonic acid).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an aldonate, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for carboxylate group (-COO-)
    carboxylate_pattern = Chem.MolFromSmarts('[C](=O)[O-]')
    if not mol.HasSubstructMatch(carboxylate_pattern):
        return False, "No carboxylate group found"
    
    # Get number of carboxylate groups
    carboxylate_matches = mol.GetSubstructMatches(carboxylate_pattern)
    if len(carboxylate_matches) > 1:
        return False, "Multiple carboxylate groups found"
        
    # Check for hydroxy groups (-OH) attached to carbons
    hydroxy_pattern = Chem.MolFromSmarts('[C]-[OH]')
    if not mol.HasSubstructMatch(hydroxy_pattern):
        return False, "No hydroxy groups found"
        
    # Check carbon chain with OH groups
    carbon_chain = []
    carboxylate_carbon = carboxylate_matches[0][0]
    
    # Start from carboxylate carbon and follow carbon chain
    visited = set()
    current = carboxylate_carbon
    while current is not None:
        visited.add(current)
        carbon_chain.append(current)
        
        # Get neighboring carbons not yet visited
        atom = mol.GetAtomWithIdx(current)
        next_carbon = None
        for neighbor in atom.GetNeighbors():
            if neighbor.GetSymbol() == 'C' and neighbor.GetIdx() not in visited:
                next_carbon = neighbor.GetIdx()
                break
                
        current = next_carbon
        
    # Check that chain has hydroxy groups
    has_oh = False
    for carbon_idx in carbon_chain:
        atom = mol.GetAtomWithIdx(carbon_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 1:
                has_oh = True
                break
                
    if not has_oh:
        return False, "No hydroxy groups on carbon chain"

    # All checks passed
    return True, "Molecule contains deprotonated carboxyl group with hydroxylated carbon chain"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22299',
                          'name': 'aldonate',
                          'definition': 'A monocarboxylic acid anion resulting '
                                        'from the deprotonation of the carboxy '
                                        'group of an aldonic acid.',
                          'parents': ['CHEBI:33721', 'CHEBI:35757']},
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
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 9582,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 0.8,
    'f1': 0.07339449541284404,
    'accuracy': 0.989573655414473}