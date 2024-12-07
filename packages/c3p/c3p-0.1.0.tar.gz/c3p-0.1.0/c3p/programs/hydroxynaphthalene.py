"""
Classifies: CHEBI:24727 hydroxynaphthalene
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroxynaphthalene(smiles: str):
    """
    Determines if a molecule is a hydroxynaphthalene (naphthalene with one or more OH groups).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydroxynaphthalene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for naphthalene core
    # Naphthalene consists of two fused benzene rings
    rings = mol.GetRingInfo()
    
    # Find aromatic 6-membered rings
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(set(ring))

    # Need at least 2 aromatic rings
    if len(aromatic_rings) < 2:
        return False, "No naphthalene core found (requires 2 fused aromatic rings)"

    # Check if there are two fused 6-membered aromatic rings
    found_naphthalene = False
    for i in range(len(aromatic_rings)):
        for j in range(i+1, len(aromatic_rings)):
            # Two rings are fused if they share exactly 2 atoms
            shared_atoms = aromatic_rings[i].intersection(aromatic_rings[j])
            if len(shared_atoms) == 2:
                # Check if the fused rings form a naphthalene (all carbons)
                ring1_atoms = [mol.GetAtomWithIdx(idx) for idx in aromatic_rings[i]]
                ring2_atoms = [mol.GetAtomWithIdx(idx) for idx in aromatic_rings[j]]
                if all(atom.GetSymbol() == 'C' for atom in ring1_atoms + ring2_atoms):
                    found_naphthalene = True
                    naphthalene_atoms = aromatic_rings[i].union(aromatic_rings[j])
                    break
        if found_naphthalene:
            break

    if not found_naphthalene:
        return False, "No naphthalene core found"

    # Check for OH groups
    hydroxyl_count = 0
    hydroxyl_positions = []
    
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O':
            # Check if oxygen is part of an OH group
            if atom.GetTotalNumHs() > 0:  # Has at least one H
                # Check if OH is attached to naphthalene core
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetIdx() in naphthalene_atoms:
                        hydroxyl_count += 1
                        hydroxyl_positions.append(str(neighbor.GetIdx()))

    if hydroxyl_count == 0:
        return False, "No hydroxyl groups found on naphthalene core"

    return True, f"Hydroxynaphthalene with {hydroxyl_count} OH group(s) at position(s): {', '.join(hydroxyl_positions)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24727',
                          'name': 'hydroxynaphthalene',
                          'definition': 'Any member of the class of  '
                                        'naphthalenes that is naphthalene '
                                        'carrying one or more hydroxy groups.',
                          'parents': ['CHEBI:25477', 'CHEBI:33853']},
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
    'num_true_positives': 24,
    'num_false_positives': 100,
    'num_true_negatives': 15866,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.1935483870967742,
    'recall': 1.0,
    'f1': 0.3243243243243243,
    'accuracy': 0.9937460913070669}