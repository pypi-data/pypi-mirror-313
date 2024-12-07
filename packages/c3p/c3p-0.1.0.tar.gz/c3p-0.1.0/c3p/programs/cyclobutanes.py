"""
Classifies: CHEBI:156473 cyclobutanes
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_cyclobutanes(smiles: str):
    """
    Determines if a molecule contains a cyclobutane ring or is a cyclobutane derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains cyclobutane, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Get ring information
    rings = mol.GetRingInfo()
    
    # Check for 4-membered rings
    four_membered_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 4:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            # Check if all atoms in ring are carbons
            if all(atom.GetSymbol() == 'C' for atom in atoms):
                # Check if ring is saturated (all single bonds)
                ring_bonds = [mol.GetBondBetweenAtoms(ring[i], ring[(i+1)%4]) 
                            for i in range(4)]
                if all(bond.GetBondType() == Chem.BondType.SINGLE for bond in ring_bonds):
                    four_membered_rings.append(ring)

    if not four_membered_rings:
        return False, "No cyclobutane ring found"

    # Find substituents on the cyclobutane ring
    ring_atoms = set(four_membered_rings[0])
    substituents = []
    
    for atom_idx in ring_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in ring_atoms:
                substituents.append(neighbor.GetSymbol())
                
    if len(substituents) > 0:
        return True, f"Cyclobutane derivative with substituents: {', '.join(set(substituents))}"
    else:
        return True, "Unsubstituted cyclobutane"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:156473',
                          'name': 'cyclobutanes',
                          'definition': 'Cyclobutane and its derivatives '
                                        'formed by substitution.',
                          'parents': ['CHEBI:33598']},
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
    'num_true_positives': 6,
    'num_false_positives': 100,
    'num_true_negatives': 17472,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 1.0,
    'f1': 0.10714285714285715,
    'accuracy': 0.9943110706565025}