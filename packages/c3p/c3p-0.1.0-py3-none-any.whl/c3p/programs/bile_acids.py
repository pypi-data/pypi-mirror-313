"""
Classifies: CHEBI:138366 bile acids
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_bile_acids(smiles: str):
    """
    Determines if a molecule is a bile acid based on structural characteristics.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a bile acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for steroid core (tetracyclic)
    ring_info = mol.GetRingInfo()
    if len(ring_info.AtomRings()) < 4:
        return False, "Missing tetracyclic steroid core"
        
    # Look for carboxylic acid group or hydroxy groups
    has_carboxyl = False
    has_hydroxy = False
    
    for atom in mol.GetAtoms():
        # Check for carboxylic acid
        if atom.GetSymbol() == 'O':
            neighbors = atom.GetNeighbors()
            if len(neighbors) == 1 and neighbors[0].GetSymbol() == 'C':
                carbon = neighbors[0]
                if len([n for n in carbon.GetNeighbors() if n.GetSymbol() == 'O']) == 2:
                    has_carboxyl = True
                    
        # Check for hydroxy groups
        if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 1:
            has_hydroxy = True
            
    if not (has_carboxyl or has_hydroxy):
        return False, "Missing characteristic acid/hydroxy groups"
        
    # Check for steroid skeleton with correct carbon count
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 20:
        return False, "Too few carbons for bile acid skeleton"
        
    # Check for cyclopentanoperhydrophenanthrene core
    matches = mol.GetSubstructMatches(Chem.MolFromSmarts('[C]1[C][C]2[C][C][C]3[C][C][C]4[C][C][C][C]4[C]3[C][C]2[C]1'))
    if not matches:
        return False, "Missing steroid core structure"
        
    return True, "Contains steroid core with characteristic acid/hydroxy groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:138366',
                          'name': 'bile acids',
                          'definition': 'Any member of a group of hydroxy '
                                        'steroids occuring in bile, where they '
                                        'are present as the sodium salts of '
                                        'their amides with glycine or taurine. '
                                        'In mammals bile acids almost '
                                        'invariably have 5beta-configuration, '
                                        'while in lower vertebrates, some bile '
                                        'acids, known as allo-bile acids, have '
                                        '5alpha-configuration.',
                          'parents': [   'CHEBI:25384',
                                         'CHEBI:35350',
                                         'CHEBI:36078']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183512,
    'num_false_negatives': 42,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9997711845015635}