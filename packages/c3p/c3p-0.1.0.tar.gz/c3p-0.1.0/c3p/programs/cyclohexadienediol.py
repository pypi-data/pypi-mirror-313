"""
Classifies: CHEBI:23469 cyclohexadienediol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_cyclohexadienediol(smiles: str):
    """
    Determines if a molecule is a cyclohexadienediol (cyclohexadiene with two OH groups on the ring).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cyclohexadienediol, False otherwise 
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find 6-membered rings
    rings = mol.GetRingInfo()
    six_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            six_rings.append(ring)

    if not six_rings:
        return False, "No 6-membered rings found"

    # For each 6-membered ring, check if it's a cyclohexadiene with 2 OH groups
    for ring in six_rings:
        # Count double bonds in ring
        double_bond_count = 0
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        
        for atom in ring_atoms:
            for bond in atom.GetBonds():
                # Only count double bonds where both atoms are in the ring
                if bond.GetBondType() == Chem.BondType.DOUBLE and \
                   bond.GetBeginAtomIdx() in ring and \
                   bond.GetEndAtomIdx() in ring:
                    double_bond_count += 0.5  # Count each double bond once

        if double_bond_count != 2:
            continue

        # Count OH groups attached to ring
        oh_count = 0
        oh_positions = []
        
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O' and \
                   neighbor.GetTotalNumHs() == 1 and \
                   neighbor.GetIdx() not in ring:
                    oh_count += 1
                    oh_positions.append(idx + 1)  # +1 for 1-based position numbering

        if oh_count == 2:
            return True, f"Cyclohexadiene with OH groups at positions {oh_positions}"

    return False, "No cyclohexadiene ring with exactly 2 OH groups found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23469',
                          'name': 'cyclohexadienediol',
                          'definition': 'Any cyclohexadiene in which two '
                                        'hydroxy groups are located on the '
                                        'cyclohexadiene ring.',
                          'parents': ['CHEBI:23824', 'CHEBI:37613']},
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
    'num_true_negatives': 98361,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9989843900754598}