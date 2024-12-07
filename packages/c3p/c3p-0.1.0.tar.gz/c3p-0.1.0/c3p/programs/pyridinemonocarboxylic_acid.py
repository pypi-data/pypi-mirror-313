"""
Classifies: CHEBI:26420 pyridinemonocarboxylic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_pyridinemonocarboxylic_acid(smiles: str):
    """
    Determines if a molecule is a pyridine monocarboxylic acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a pyridine monocarboxylic acid, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find pyridine rings
    pyridine_rings = []
    ring_info = mol.GetRingInfo()
    
    for ring in ring_info.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            # Check if ring is aromatic and contains exactly one nitrogen
            if (all(atom.GetIsAromatic() for atom in atoms) and
                sum(1 for atom in atoms if atom.GetSymbol() == 'N') == 1):
                pyridine_rings.append(ring)
                
    if not pyridine_rings:
        return False, "No pyridine ring found"

    # Find carboxylic acid groups (-C(=O)OH)
    carboxyl_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
    carboxyl_matches = mol.GetSubstructMatches(carboxyl_pattern)
    
    if not carboxyl_matches:
        return False, "No carboxylic acid group found"
        
    if len(carboxyl_matches) > 1:
        return False, "More than one carboxylic acid group found"

    # Check if carboxylic acid is attached to pyridine ring
    carboxyl_carbon = carboxyl_matches[0][0]
    carboxyl_atom = mol.GetAtomWithIdx(carboxyl_carbon)
    
    for pyridine_ring in pyridine_rings:
        ring_atoms = set(pyridine_ring)
        # Check neighbors of carboxyl carbon
        for neighbor in carboxyl_atom.GetNeighbors():
            if neighbor.GetIdx() in ring_atoms:
                position = get_pyridine_position(mol, pyridine_ring, neighbor.GetIdx())
                return True, f"Pyridine-{position}-carboxylic acid"
                
    return False, "Carboxylic acid group not directly attached to pyridine ring"

def get_pyridine_position(mol, ring_atoms, carbon_idx):
    """Helper function to determine position of substituent on pyridine ring"""
    # Find nitrogen atom in ring
    n_idx = None
    for idx in ring_atoms:
        if mol.GetAtomWithIdx(idx).GetSymbol() == 'N':
            n_idx = idx
            break
            
    # Get path around ring from N to substituted C
    path = Chem.GetShortestPath(mol, n_idx, carbon_idx)
    if len(path) == 1:
        return "2"  # Ortho
    elif len(path) == 2:
        return "3"  # Meta  
    else:
        return "4"  # Para


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26420',
                          'name': 'pyridinemonocarboxylic acid',
                          'definition': 'A monocarboxylic acid in which the '
                                        'carboxy group is attached to a '
                                        'pyridine (or substituted pyridine) '
                                        'ring.',
                          'parents': [   'CHEBI:25384',
                                         'CHEBI:26421',
                                         'CHEBI:33859']},
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
    'num_false_positives': 100,
    'num_true_negatives': 67113,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 0.3,
    'f1': 0.05309734513274337,
    'accuracy': 0.9984082828793717}