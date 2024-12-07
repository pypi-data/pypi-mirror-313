"""
Classifies: CHEBI:25389 monohydroxybenzoic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_monohydroxybenzoic_acid(smiles: str):
    """
    Determines if a molecule is a monohydroxybenzoic acid (single phenolic hydroxy substituent on benzene ring with carboxylic acid).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a monohydroxybenzoic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find aromatic rings
    rings = mol.GetRingInfo()
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)

    if not aromatic_rings:
        return False, "No aromatic 6-membered rings found"

    # Look for carboxylic acid group attached to aromatic ring
    carboxylic_pattern = Chem.MolFromSmarts('c-C(=O)O')
    carboxylic_matches = mol.GetSubstructMatches(carboxylic_pattern)
    
    if not carboxylic_matches:
        return False, "No carboxylic acid group attached to aromatic ring"

    # Look for phenolic OH group attached to aromatic ring
    phenol_pattern = Chem.MolFromSmarts('cO')
    phenol_matches = mol.GetSubstructMatches(phenol_pattern)
    
    if not phenol_matches:
        return False, "No phenolic OH group found"

    # Count number of phenolic OH groups on the ring with carboxylic acid
    phenol_count = 0
    ring_atoms = set()
    
    # Find the aromatic ring that has the carboxylic acid
    for match in carboxylic_matches:
        ring_atom = match[0]  # The aromatic carbon the COOH is attached to
        for ring in aromatic_rings:
            if ring_atom in ring:
                ring_atoms = set(ring)
                break
    
    # Count phenolic OH groups on this specific ring
    for match in phenol_matches:
        if match[0] in ring_atoms:  # Check if the aromatic carbon is part of our target ring
            phenol_count += 1

    if phenol_count == 0:
        return False, "No phenolic OH group on the benzene ring with carboxylic acid"
    elif phenol_count > 1:
        return False, f"Found {phenol_count} phenolic OH groups, but monohydroxybenzoic acid should have exactly one"
    
    return True, "Found benzene ring with one phenolic OH group and carboxylic acid substituent"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25389',
                          'name': 'monohydroxybenzoic acid',
                          'definition': 'Any hydroxybenzoic acid having a '
                                        'single phenolic hydroxy substituent '
                                        'on the benzene ring.',
                          'parents': ['CHEBI:24676']},
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
    'num_true_negatives': 11572,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.06542056074766354,
    'recall': 1.0,
    'f1': 0.12280701754385964,
    'accuracy': 0.9914376230841682}