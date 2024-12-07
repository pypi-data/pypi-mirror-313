"""
Classifies: CHEBI:24646 hydroquinones
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_hydroquinones(smiles: str):
    """
    Determines if a molecule is a hydroquinone (benzene with hydroxy groups at 1,4 positions).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydroquinone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Generate the aromatic ring information
    rings = mol.GetRingInfo()

    # Check for at least one 6-membered ring
    if not any(len(ring) == 6 for ring in rings.AtomRings()):
        return False, "No 6-membered rings found"

    # Find all aromatic 6-membered rings
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)

    if not aromatic_rings:
        return False, "No aromatic 6-membered rings found"

    # For each aromatic ring, check if it has hydroxy groups at para positions
    for ring in aromatic_rings:
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        
        # Find hydroxy substituents
        hydroxy_positions = []
        for i, atom in enumerate(ring_atoms):
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 1:
                    hydroxy_positions.append(i)
        
        # Check if there are exactly 2 hydroxy groups
        if len(hydroxy_positions) != 2:
            continue
            
        # Check if hydroxy groups are para to each other (positions differ by 3)
        pos_diff = abs(hydroxy_positions[0] - hydroxy_positions[1])
        if pos_diff == 3 or pos_diff == 3:
            return True, "Found benzene ring with hydroxy groups in 1,4 positions"

    return False, "No benzene ring with hydroxy groups in 1,4 positions found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24646',
                          'name': 'hydroquinones',
                          'definition': 'Benzenediols that have the hydroxy '
                                        'substituents in the 1- and '
                                        '4-positions.',
                          'parents': ['CHEBI:33570']},
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
    'num_true_positives': 17,
    'num_false_positives': 100,
    'num_true_negatives': 20956,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.1452991452991453,
    'recall': 1.0,
    'f1': 0.2537313432835821,
    'accuracy': 0.9952545911830304}