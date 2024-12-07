"""
Classifies: CHEBI:23697 dichlorobenzene
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_dichlorobenzene(smiles: str):
    """
    Determines if a molecule contains a dichlorobenzene moiety (benzene with exactly 2 chloro substituents).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains dichlorobenzene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find all benzene rings
    rings = mol.GetRingInfo()
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                if all(atom.GetSymbol() == 'C' for atom in atoms):
                    aromatic_rings.append(ring)

    if not aromatic_rings:
        return False, "No benzene rings found"

    # For each benzene ring, check if it has exactly 2 chloro substituents
    for ring in aromatic_rings:
        ring_atoms = set(ring)
        chloro_count = 0
        chloro_positions = []
        
        # Check substituents
        for atom_idx in ring_atoms:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() not in ring_atoms:
                    if neighbor.GetSymbol() == 'Cl':
                        chloro_count += 1
                        chloro_positions.append(atom_idx)

        if chloro_count == 2:
            # Get the positions of the chloro substituents
            positions = []
            for idx in chloro_positions:
                pos = list(ring).index(idx) + 1
                positions.append(str(pos))
            positions.sort()
            return True, f"Dichlorobenzene found with chloro substituents at positions {','.join(positions)}"

    return False, "No benzene ring with exactly 2 chloro substituents found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23697',
                          'name': 'dichlorobenzene',
                          'definition': 'Any member of the class of '
                                        'chlorobenzenes carrying two chloro '
                                        'groups at unspecified positions.',
                          'parents': ['CHEBI:23132']},
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
    'num_true_positives': 55,
    'num_false_positives': 100,
    'num_true_negatives': 16864,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.3548387096774194,
    'recall': 1.0,
    'f1': 0.5238095238095238,
    'accuracy': 0.9941242141136377}