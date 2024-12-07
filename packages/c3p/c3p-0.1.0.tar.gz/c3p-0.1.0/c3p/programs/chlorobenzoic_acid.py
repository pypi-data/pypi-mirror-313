"""
Classifies: CHEBI:23134 chlorobenzoic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_chlorobenzoic_acid(smiles: str):
    """
    Determines if a molecule is a chlorobenzoic acid (benzoic acid with at least one chloro substituent).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a chlorobenzoic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of carboxylic acid group
    carboxylic_acid_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
    if not mol.HasSubstructMatch(carboxylic_acid_pattern):
        return False, "No carboxylic acid group found"

    # Check for aromatic ring
    rings = mol.GetRingInfo()
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)

    if not aromatic_rings:
        return False, "No aromatic 6-membered ring found"

    # Get the ring that's connected to the carboxylic acid
    carboxylic_matches = mol.GetSubstructMatches(carboxylic_acid_pattern)
    if not carboxylic_matches:
        return False, "Carboxylic acid not properly connected"
    
    carboxylic_c = carboxylic_matches[0][0]
    connected_ring = None
    
    for ring in aromatic_rings:
        for atom_idx in ring:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() == carboxylic_c:
                    connected_ring = ring
                    break
    
    if connected_ring is None:
        return False, "Carboxylic acid not connected to aromatic ring"

    # Check for chlorine substituents on the ring
    chlorine_count = 0
    ring_atoms = set(connected_ring)
    
    for atom_idx in ring_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in ring_atoms:
                if neighbor.GetSymbol() == 'Cl':
                    chlorine_count += 1

    if chlorine_count == 0:
        return False, "No chlorine substituents found on the benzene ring"
    
    positions = []
    for atom_idx in connected_ring:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetSymbol() == 'Cl':
                # Find position relative to COOH
                for i, ring_atom_idx in enumerate(connected_ring):
                    if ring_atom_idx == atom_idx:
                        positions.append(str(i+1))
                        break

    return True, f"Chlorobenzoic acid with {chlorine_count} chlorine(s) at position(s) {', '.join(positions)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23134',
                          'name': 'chlorobenzoic acid',
                          'definition': 'Any member of the class of benzoic '
                                        'acids in which the benzene ring is '
                                        'substituted by at least one chloro '
                                        'group.',
                          'parents': ['CHEBI:22723', 'CHEBI:36685']},
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
    'num_false_positives': 75,
    'num_true_negatives': 183838,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.025974025974025976,
    'recall': 1.0,
    'f1': 0.05063291139240507,
    'accuracy': 0.9995922029198271}