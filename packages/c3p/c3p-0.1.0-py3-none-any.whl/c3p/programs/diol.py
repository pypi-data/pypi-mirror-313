"""
Classifies: CHEBI:23824 diol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_diol(smiles: str):
    """
    Determines if a molecule is a diol (contains exactly two hydroxy groups).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a diol, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Count number of OH groups
    oh_pattern = Chem.MolFromSmarts('[OH]')
    oh_matches = mol.GetSubstructMatches(oh_pattern)
    
    # Count number of OH groups not part of carboxylic acids
    cooh_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
    cooh_matches = mol.GetSubstructMatches(cooh_pattern)
    
    # Get indices of OH groups that are part of COOH
    cooh_oh_indices = set()
    for match in cooh_matches:
        cooh_oh_indices.add(match[-1])  # Last atom in COOH pattern is the OH oxygen
        
    # Count OH groups that are not part of COOH
    true_oh_count = 0
    oh_positions = []
    for match in oh_matches:
        if match[0] not in cooh_oh_indices:
            true_oh_count += 1
            oh_positions.append(match[0])
            
    if true_oh_count != 2:
        return False, f"Contains {true_oh_count} hydroxyl groups instead of 2"
        
    # Check if the OH groups are alcoholic (attached to sp3 carbon)
    alcoholic_count = 0
    for oh_pos in oh_positions:
        oh_atom = mol.GetAtomWithIdx(oh_pos)
        for neighbor in oh_atom.GetNeighbors():
            if neighbor.GetHybridization() == Chem.HybridizationType.SP3 and neighbor.GetSymbol() == 'C':
                alcoholic_count += 1
                break
            
    if alcoholic_count == 2:
        return True, "Contains 2 alcoholic hydroxyl groups"
    elif alcoholic_count == 1:
        return True, "Contains 1 alcoholic and 1 non-alcoholic hydroxyl group"
    else:
        return True, "Contains 2 non-alcoholic hydroxyl groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23824',
                          'name': 'diol',
                          'definition': 'A compound that contains two hydroxy '
                                        'groups, generally assumed to be, but '
                                        'not necessarily, alcoholic. Aliphatic '
                                        'diols are also called glycols.',
                          'parents': ['CHEBI:26191']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
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
    'num_true_positives': 45,
    'num_false_positives': 100,
    'num_true_negatives': 740,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.3103448275862069,
    'recall': 0.9,
    'f1': 0.4615384615384615,
    'accuracy': 0.8820224719101124}