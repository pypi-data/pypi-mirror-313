"""
Classifies: CHEBI:25340 methylpyridines
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_methylpyridines(smiles: str):
    """
    Determines if a molecule is a methylpyridine (pyridine with at least one methyl substituent).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a methylpyridine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find pyridine rings
    pyridine_rings = []
    for ring in mol.GetRingInfo().AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            # Check if ring is aromatic and contains exactly one nitrogen
            if all(atom.GetIsAromatic() for atom in atoms) and \
               sum(atom.GetSymbol() == 'N' for atom in atoms) == 1:
                pyridine_rings.append(ring)

    if not pyridine_rings:
        return False, "No pyridine ring found"

    # Find methyl substituents
    methyl_positions = []
    for ring in pyridine_rings:
        ring_atoms = set(ring)
        for atom_idx in ring:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() not in ring_atoms:
                    # Check if neighbor is carbon with exactly 3 hydrogens (methyl)
                    if neighbor.GetSymbol() == 'C' and \
                       neighbor.GetTotalNumHs() == 3 and \
                       len([n for n in neighbor.GetNeighbors() if n.GetIdx() != atom_idx]) == 0:
                        ring_pos = ring.index(atom_idx) + 1
                        methyl_positions.append(str(ring_pos))

    if methyl_positions:
        positions_str = ", ".join(methyl_positions)
        return True, f"Methylpyridine with methyl group(s) at position(s): {positions_str}"
    else:
        return False, "No methyl substituents found on pyridine ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25340',
                          'name': 'methylpyridines',
                          'definition': 'Any member of the class of pyridines '
                                        'that carries at least one methyl '
                                        'substituent.',
                          'parents': ['CHEBI:26421']},
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
    'num_true_negatives': 15985,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 0.8571428571428571,
    'f1': 0.10619469026548672,
    'accuracy': 0.9937235893611732}