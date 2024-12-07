"""
Classifies: CHEBI:25562 nitrophenol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_nitrophenol(smiles: str):
    """
    Determines if a molecule is a nitrophenol (phenol with at least one nitro group).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a nitrophenol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for phenol substructure
    phenol_pattern = Chem.MolFromSmarts('c1ccccc1[OH]')
    if not mol.HasSubstructMatch(phenol_pattern):
        return False, "No phenol substructure found"

    # Check for nitro group
    nitro_pattern = Chem.MolFromSmarts('[N+](=O)[O-]')
    nitro_matches = mol.GetSubstructMatches(nitro_pattern)
    
    if not nitro_matches:
        return False, "No nitro groups found"

    # Count nitro groups
    num_nitro = len(nitro_matches)

    # Get aromatic ring atoms
    phenol_match = mol.GetSubstructMatch(phenol_pattern)
    ring_atoms = set(phenol_match[:6])  # First 6 atoms are the aromatic ring

    # Check if any nitro group is attached to the phenol ring
    nitro_on_ring = False
    for nitro_match in nitro_matches:
        nitro_n = nitro_match[0]  # Index of nitrogen atom
        for neighbor in mol.GetAtomWithIdx(nitro_n).GetNeighbors():
            if neighbor.GetIdx() in ring_atoms:
                nitro_on_ring = True
                break
        if nitro_on_ring:
            break

    if not nitro_on_ring:
        return False, "Nitro group(s) not attached to phenol ring"

    # Get positions of substituents
    positions = []
    for i, atom_idx in enumerate(phenol_match[:6]):
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in phenol_match:
                positions.append(i+1)
                break

    return True, f"Nitrophenol with {num_nitro} nitro group(s) at position(s) {sorted(set(positions))}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25562',
                          'name': 'nitrophenol',
                          'definition': 'Any member of the class of  phenols '
                                        'or substituted phenols carrying  at '
                                        'least 1 nitro group.',
                          'parents': ['CHEBI:33853', 'CHEBI:35716']},
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
    'num_true_positives': 6,
    'num_false_positives': 100,
    'num_true_negatives': 180937,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 0.8571428571428571,
    'f1': 0.10619469026548672,
    'accuracy': 0.9994421245664038}