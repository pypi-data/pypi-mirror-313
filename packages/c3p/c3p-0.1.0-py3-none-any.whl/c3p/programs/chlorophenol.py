"""
Classifies: CHEBI:23150 chlorophenol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_chlorophenol(smiles: str):
    """
    Determines if a molecule is a chlorophenol (phenol with one or more chlorine substituents).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a chlorophenol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of phenol structure
    phenol_pattern = Chem.MolFromSmarts('c1ccccc1[OH]')
    if not mol.HasSubstructMatch(phenol_pattern):
        return False, "No phenol structure found"

    # Check for presence of chlorine atoms
    chlorine_pattern = Chem.MolFromSmarts('[Cl]')
    chlorine_matches = mol.GetSubstructMatches(chlorine_pattern)
    
    if not chlorine_matches:
        return False, "No chlorine atoms found"

    # Find the phenol ring atoms
    phenol_matches = mol.GetSubstructMatches(phenol_pattern)
    phenol_ring_atoms = set(phenol_matches[0][:6])  # First 6 atoms are the ring atoms

    # Count chlorines attached to the phenol ring
    ring_chlorines = 0
    for chlorine_match in chlorine_matches:
        chlorine_idx = chlorine_match[0]
        chlorine_atom = mol.GetAtomWithIdx(chlorine_idx)
        
        # Check if the chlorine is connected to the phenol ring
        for neighbor in chlorine_atom.GetNeighbors():
            if neighbor.GetIdx() in phenol_ring_atoms:
                ring_chlorines += 1

    if ring_chlorines == 0:
        return False, "No chlorine atoms attached to the phenol ring"

    # Get positions of chlorine atoms on the ring
    positions = []
    for atom_idx in phenol_ring_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetSymbol() == 'Cl':
                positions.append(str(len(positions) + 1))

    return True, f"Chlorophenol with {ring_chlorines} chlorine atom(s) on the phenol ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23150',
                          'name': 'chlorophenol',
                          'definition': 'A halophenol that is any phenol '
                                        'containing one or more covalently '
                                        'bonded chlorine atoms.',
                          'parents': ['CHEBI:23132', 'CHEBI:38856']},
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
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 21068,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.995276334435522}