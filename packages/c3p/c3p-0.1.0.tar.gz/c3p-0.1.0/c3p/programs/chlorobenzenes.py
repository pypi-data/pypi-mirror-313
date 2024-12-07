"""
Classifies: CHEBI:23132 chlorobenzenes
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_chlorobenzenes(smiles: str):
    """
    Determines if a molecule is a chlorobenzene (contains a benzene ring substituted with one or more chlorines).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a chlorobenzene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all aromatic rings
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

    # Check for chlorine substituents on benzene rings
    chlorine_count = 0
    for ring in aromatic_rings:
        ring_atoms = set(ring)
        for atom_idx in ring_atoms:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() not in ring_atoms:
                    if neighbor.GetSymbol() == 'Cl':
                        chlorine_count += 1

    if chlorine_count > 0:
        return True, f"Benzene ring with {chlorine_count} chlorine substituent(s)"
    else:
        return False, "No chlorine substituents found on benzene ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23132',
                          'name': 'chlorobenzenes',
                          'definition': 'Any organochlorine compound '
                                        'containing a benzene ring which is '
                                        'substituted by one or more chlorines.',
                          'parents': ['CHEBI:22712', 'CHEBI:36683']},
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
    'num_true_positives': 113,
    'num_false_positives': 100,
    'num_true_negatives': 2728,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.5305164319248826,
    'recall': 0.9826086956521739,
    'f1': 0.6890243902439024,
    'accuracy': 0.9653414882772681}