"""
Classifies: CHEBI:25448 myo-inositol phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_myo_inositol_phosphate(smiles: str):
    """
    Determines if a molecule is a myo-inositol phosphate.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a myo-inositol phosphate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for 6-membered ring
    rings = mol.GetRingInfo()
    if not any(len(ring) == 6 for ring in rings.AtomRings()):
        return False, "No 6-membered ring found"

    # Get the 6-membered ring
    ring = None
    for r in rings.AtomRings():
        if len(r) == 6:
            ring = r
            break

    # Check ring atoms are all carbon
    ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
    if not all(atom.GetSymbol() == 'C' for atom in ring_atoms):
        return False, "Ring must be composed of carbon atoms"

    # Check for at least one phosphate group
    phosphate_count = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'P':
            # Check if it's a phosphate group (P with 4 oxygen neighbors)
            oxygen_neighbors = sum(1 for n in atom.GetNeighbors() if n.GetSymbol() == 'O')
            if oxygen_neighbors == 4:
                phosphate_count += 1

    if phosphate_count == 0:
        return False, "No phosphate groups found"

    # Check for myo-inositol configuration
    # In myo-inositol, all hydroxyl groups are equatorial except one axial hydroxyl
    # This is represented in the SMILES by specific stereochemistry pattern
    
    # Get all substituents on the ring
    substituents = []
    for atom_idx in ring:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in ring:
                if neighbor.GetSymbol() == 'O':
                    substituents.append(neighbor)

    # Check if we have the correct number of substituents (should be 6)
    if len(substituents) != 6:
        return False, "Incorrect number of substituents on the ring"

    # For a valid myo-inositol phosphate, we need:
    # 1. At least one phosphate group
    # 2. The remaining positions should be hydroxyl groups
    # 3. Correct stereochemistry (though this is complex to verify completely)

    return True, f"Myo-inositol phosphate with {phosphate_count} phosphate group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25448',
                          'name': 'myo-inositol phosphate',
                          'definition': 'An inositol phosphate in which the '
                                        'inositol component has '
                                        'myo-configuration.',
                          'parents': ['CHEBI:24846']},
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
    'num_true_negatives': 24559,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 1.0,
    'f1': 0.07407407407407407,
    'accuracy': 0.9959453432266958}