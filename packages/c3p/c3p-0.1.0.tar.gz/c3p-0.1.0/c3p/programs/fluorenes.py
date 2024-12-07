"""
Classifies: CHEBI:24059 fluorenes
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetSymmSSSR

def is_fluorenes(smiles: str):
    """
    Determines if a molecule is a fluorene derivative.
    Fluorenes contain two benzene rings ortho-fused to a cyclopentane ring.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a fluorene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Get ring information
    rings = list(GetSymmSSSR(mol))
    if len(rings) < 3:
        return False, "Less than 3 rings found - fluorenes require 3 fused rings"

    # Find 5-membered rings
    five_rings = []
    for ring in rings:
        if len(ring) == 5:
            five_rings.append(ring)

    # Find 6-membered aromatic rings
    six_rings = []
    for ring in rings:
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                six_rings.append(ring)

    if len(six_rings) < 2:
        return False, "Less than 2 benzene rings found"
    
    if len(five_rings) < 1:
        return False, "No 5-membered ring found"

    # Check if rings are properly fused
    for five_ring in five_rings:
        benzene_count = 0
        for six_ring in six_rings:
            # Check if rings share exactly 2 atoms (ortho-fusion)
            shared_atoms = set(five_ring).intersection(set(six_ring))
            if len(shared_atoms) == 2:
                benzene_count += 1
        
        if benzene_count == 2:
            # Found a 5-membered ring fused to 2 benzene rings
            return True, "Contains fluorene core structure (two benzene rings ortho-fused to cyclopentane)"

    return False, "Rings are not properly fused in fluorene arrangement"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24059',
                          'name': 'fluorenes',
                          'definition': 'An ortho-fused polycyclic arene in '
                                        'which the skeleton is composed of two '
                                        'benzene rings ortho-fused to '
                                        'cyclopentane.',
                          'parents': ['CHEBI:38032']},
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
    'num_true_positives': 7,
    'num_false_positives': 100,
    'num_true_negatives': 15885,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.06542056074766354,
    'recall': 0.7,
    'f1': 0.11965811965811965,
    'accuracy': 0.9935604876523914}