"""
Classifies: CHEBI:25388 monohydroxybenzoate
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_monohydroxybenzoate(smiles: str):
    """
    Determines if a molecule is a monohydroxybenzoate (benzoate with single hydroxy substituent).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a monohydroxybenzoate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

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

    # Check for benzoate group (carboxylate attached to benzene ring)
    carboxylate_pattern = Chem.MolFromSmarts('c-C([O-])=O')
    if not mol.HasSubstructMatch(carboxylate_pattern):
        return False, "No benzoate group found"

    # Count hydroxy groups attached to the aromatic ring
    hydroxy_pattern = Chem.MolFromSmarts('c-[OH]')
    hydroxy_matches = mol.GetSubstructMatches(hydroxy_pattern)
    
    if len(hydroxy_matches) == 0:
        return False, "No hydroxy substituent found"
    elif len(hydroxy_matches) > 1:
        return False, f"Found {len(hydroxy_matches)} hydroxy groups, expected exactly one"
    
    # Verify hydroxy is attached to the same aromatic ring as carboxylate
    ring_atoms = set(aromatic_rings[0])
    hydroxy_carbon = mol.GetAtomWithIdx(hydroxy_matches[0][0])
    if hydroxy_carbon.GetIdx() not in ring_atoms:
        return False, "Hydroxy group not attached to main aromatic ring"
        
    # Get position of hydroxy group relative to carboxylate
    carboxylate_matches = mol.GetSubstructMatches(carboxylate_pattern)
    carboxylate_carbon = mol.GetAtomWithIdx(carboxylate_matches[0][0])
    
    positions = []
    for i, atom_idx in enumerate(aromatic_rings[0]):
        if atom_idx == hydroxy_carbon.GetIdx():
            hydroxy_pos = i + 1
            positions.append(f"{hydroxy_pos}-hydroxy")
            
    return True, f"Monohydroxybenzoate: {', '.join(positions)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25388',
                          'name': 'monohydroxybenzoate',
                          'definition': 'A hydroxybenzoate carrying a single '
                                        'hydroxy substituent at unspecified '
                                        'position.',
                          'parents': ['CHEBI:24675']},
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
    'num_false_positives': 60,
    'num_true_negatives': 183855,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.03225806451612903,
    'recall': 1.0,
    'f1': 0.0625,
    'accuracy': 0.9996737658835235}