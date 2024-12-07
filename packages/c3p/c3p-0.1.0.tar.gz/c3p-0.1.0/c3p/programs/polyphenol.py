"""
Classifies: CHEBI:26195 polyphenol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_polyphenol(smiles: str):
    """
    Determines if a molecule is a polyphenol (contains 2 or more benzene rings each substituted by at least one hydroxy group).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a polyphenol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get all aromatic rings
    ri = mol.GetRingInfo()
    aromatic_rings = []
    for ring in ri.AtomRings():
        if len(ring) == 6:  # Only consider 6-membered rings
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms) and \
               all(atom.GetSymbol() == 'C' for atom in atoms):
                aromatic_rings.append(ring)

    if len(aromatic_rings) < 2:
        return False, "Less than 2 benzene rings found"

    # Check each aromatic ring for hydroxy substituents
    rings_with_oh = 0
    for ring in aromatic_rings:
        ring_atoms = set(ring)
        has_oh = False
        
        # Check each ring atom for OH substituents
        for atom_idx in ring_atoms:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O':
                    # Check if this oxygen has exactly one hydrogen
                    if neighbor.GetTotalNumHs() == 1 and neighbor.GetDegree() == 1:
                        has_oh = True
                        break
            if has_oh:
                break
                
        if has_oh:
            rings_with_oh += 1

    if rings_with_oh < 2:
        return False, f"Only {rings_with_oh} benzene rings with OH substituents found"

    return True, f"Found {rings_with_oh} benzene rings with OH substituents"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26195',
                          'name': 'polyphenol',
                          'definition': 'Members of the class of phenols that '
                                        'contain 2 or more benzene rings each '
                                        'of which is substituted by at least '
                                        'one hydroxy group.',
                          'parents': ['CHEBI:33853']},
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
    'num_true_positives': 74,
    'num_false_positives': 100,
    'num_true_negatives': 2098,
    'num_false_negatives': 11,
    'num_negatives': None,
    'precision': 0.42528735632183906,
    'recall': 0.8705882352941177,
    'f1': 0.5714285714285714,
    'accuracy': 0.9513797634691196}