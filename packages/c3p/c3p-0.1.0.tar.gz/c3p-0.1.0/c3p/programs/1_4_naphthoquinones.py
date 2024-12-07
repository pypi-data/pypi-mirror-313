"""
Classifies: CHEBI:132142 1,4-naphthoquinones
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetSymmSSSR

def is_1_4_naphthoquinones(smiles: str):
    """
    Determines if a molecule is a 1,4-naphthoquinone.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a 1,4-naphthoquinone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for naphthalene core
    rings = list(GetSymmSSSR(mol))
    fused_rings = []
    for i, ring1 in enumerate(rings):
        for j, ring2 in enumerate(rings):
            if i < j:
                shared_atoms = set(ring1).intersection(set(ring2))
                if len(shared_atoms) == 2:
                    fused_rings.append((ring1, ring2))

    if not fused_rings:
        return False, "No fused ring system found"

    # Check for naphthalene with two 6-membered rings
    naphthalene_found = False
    for ring1, ring2 in fused_rings:
        if len(ring1) == 6 and len(ring2) == 6:
            naphthalene_found = True
            naphthalene_atoms = set(ring1).union(set(ring2))
            break

    if not naphthalene_found:
        return False, "No naphthalene core found"

    # Find carbonyl groups
    carbonyl_positions = []
    for atom_idx in naphthalene_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetSymbol() == 'C':
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 0 and \
                   sum(1 for bond in neighbor.GetBonds() if bond.GetBondType() == Chem.BondType.DOUBLE) == 1:
                    carbonyl_positions.append(atom_idx)

    if len(carbonyl_positions) != 2:
        return False, "Does not contain exactly two carbonyl groups"

    # Check if carbonyls are at positions 1 and 4
    # This is a simplified check - assumes carbonyls are on same ring and para to each other
    carbonyl_atoms = [mol.GetAtomWithIdx(pos) for pos in carbonyl_positions]
    path_length = len(Chem.GetShortestPath(mol, carbonyl_positions[0], carbonyl_positions[1]))
    
    if path_length != 5:  # Para position in 6-membered ring
        return False, "Carbonyl groups not in 1,4 positions"

    # Additional check for quinone structure
    for c_idx in carbonyl_positions:
        c_atom = mol.GetAtomWithIdx(c_idx)
        if not any(bond.GetBondType() == Chem.BondType.DOUBLE for bond in c_atom.GetBonds()):
            return False, "Not a quinone structure"

    return True, "1,4-naphthoquinone structure confirmed"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:132142',
                          'name': '1,4-naphthoquinones',
                          'definition': 'A naphthoquinone in which the oxo '
                                        'groups of the quinone moiety are at '
                                        'positions 1 and 4 of the parent '
                                        'naphthalene ring.',
                          'parents': ['CHEBI:25481', 'CHEBI:25830']},
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
    'num_true_positives': 0,
    'num_false_positives': 100,
    'num_true_negatives': 101737,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9989297566914753}