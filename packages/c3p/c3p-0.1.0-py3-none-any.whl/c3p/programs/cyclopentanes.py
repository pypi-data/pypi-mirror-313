"""
Classifies: CHEBI:23493 cyclopentanes
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_cyclopentanes(smiles: str):
    """
    Determines if a molecule contains a cyclopentane ring (saturated 5-membered carbocycle).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains cyclopentane, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Get ring information
    rings = mol.GetRingInfo()
    
    # Find 5-membered rings
    five_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 5:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            # Check if all atoms are carbons
            if all(atom.GetSymbol() == 'C' for atom in atoms):
                # Check if ring is saturated (all sp3 carbons)
                if all(atom.GetHybridization() == Chem.HybridizationType.SP3 for atom in atoms):
                    five_rings.append(ring)
    
    if not five_rings:
        return False, "No cyclopentane ring found"

    # Get substituents on the cyclopentane ring
    substituents = []
    for ring in five_rings:
        ring_atoms = set(ring)
        for atom_idx in ring:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() not in ring_atoms:
                    substituents.append(neighbor.GetSymbol())

    if len(substituents) > 0:
        return True, f"Cyclopentane with substituents: {', '.join(set(substituents))}"
    else:
        return True, "Unsubstituted cyclopentane"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23493',
                          'name': 'cyclopentanes',
                          'definition': 'Cyclopentane and its derivatives '
                                        'formed by substitution.',
                          'parents': ['CHEBI:33598']},
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
    'num_true_negatives': 1629,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 1.0,
    'f1': 0.07407407407407407,
    'accuracy': 0.9422965954991345}