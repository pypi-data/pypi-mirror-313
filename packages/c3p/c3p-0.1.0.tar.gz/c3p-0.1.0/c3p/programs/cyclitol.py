"""
Classifies: CHEBI:23451 cyclitol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_cyclitol(smiles: str):
    """
    Determines if a molecule is a cyclitol (cycloalkane with at least 3 hydroxy groups on different ring carbons)

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cyclitol, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Get ring information
    rings = mol.GetRingInfo()
    if not rings.NumRings():
        return False, "No rings found"

    # Look for cycloalkane rings
    cycloalkane_rings = []
    for ring in rings.AtomRings():
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        # Check if all atoms in ring are carbons and saturated
        if all(atom.GetSymbol() == 'C' and atom.GetHybridization() == Chem.HybridizationType.SP3 for atom in atoms):
            cycloalkane_rings.append(ring)

    if not cycloalkane_rings:
        return False, "No cycloalkane rings found"

    # For each cycloalkane ring, check for at least 3 hydroxy groups on different carbons
    for ring in cycloalkane_rings:
        hydroxy_count = 0
        ring_atoms = set(ring)
        used_carbons = set()

        for atom_idx in ring:
            atom = mol.GetAtomWithIdx(atom_idx)
            # Check each neighbor of ring carbon
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 1:
                    # Check if this oxygen is only connected to this ring carbon
                    o_neighbors = [n.GetIdx() for n in neighbor.GetNeighbors()]
                    if len(o_neighbors) == 1 and o_neighbors[0] == atom_idx:
                        if atom_idx not in used_carbons:
                            hydroxy_count += 1
                            used_carbons.add(atom_idx)

        if hydroxy_count >= 3:
            return True, f"Cycloalkane ring found with {hydroxy_count} hydroxy groups on different carbons"

    return False, "No cycloalkane ring with at least 3 hydroxy groups on different carbons found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23451',
                          'name': 'cyclitol',
                          'definition': 'A polyol consisting of a cycloalkane '
                                        'containing at least three hydroxy '
                                        'groups, each attached to a different '
                                        'ring carbon atom.',
                          'parents': ['CHEBI:26191']},
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
    'num_true_positives': 14,
    'num_false_positives': 100,
    'num_true_negatives': 11965,
    'num_false_negatives': 17,
    'num_negatives': None,
    'precision': 0.12280701754385964,
    'recall': 0.45161290322580644,
    'f1': 0.19310344827586207,
    'accuracy': 0.9903273809523809}