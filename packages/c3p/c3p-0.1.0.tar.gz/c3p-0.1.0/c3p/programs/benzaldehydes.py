"""
Classifies: CHEBI:22698 benzaldehydes
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_benzaldehydes(smiles: str):
    """
    Determines if a molecule is a benzaldehyde (formyl substituted benzene and derivatives).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a benzaldehyde, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Generate aromatic ring information
    rings = mol.GetRingInfo()
    
    # Find aromatic 6-membered rings
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)
                
    if not aromatic_rings:
        return False, "No aromatic 6-membered rings found"

    # Check for formyl group (-CHO) attached to aromatic ring
    formyl_pattern = Chem.MolFromSmarts('[$(C(=O)[H])]')
    matches = mol.GetSubstructMatches(formyl_pattern)
    
    if not matches:
        return False, "No formyl group found"

    # Check if formyl is attached to aromatic ring
    formyl_carbons = [match[0] for match in matches]
    
    for ring in aromatic_rings:
        ring_atoms = set(ring)
        for formyl_c in formyl_carbons:
            atom = mol.GetAtomWithIdx(formyl_c)
            neighbors = [n.GetIdx() for n in atom.GetNeighbors()]
            if any(n in ring_atoms for n in neighbors):
                # Find other substituents
                substituents = []
                for ring_atom_idx in ring_atoms:
                    ring_atom = mol.GetAtomWithIdx(ring_atom_idx)
                    for neighbor in ring_atom.GetNeighbors():
                        if neighbor.GetIdx() not in ring_atoms:
                            if neighbor.GetAtomicNum() != 1:  # Exclude hydrogens
                                symbol = neighbor.GetSymbol()
                                if neighbor.GetIdx() not in formyl_carbons:
                                    substituents.append(symbol)
                
                if substituents:
                    return True, f"Benzaldehyde with substituents: {', '.join(set(substituents))}"
                else:
                    return True, "Unsubstituted benzaldehyde"
                    
    return False, "Formyl group not attached to aromatic ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22698',
                          'name': 'benzaldehydes',
                          'definition': 'Any arenecarbaldehyde that consists '
                                        'of a formyl substituted benzene ring '
                                        'and its substituted derivatives '
                                        'thereof.',
                          'parents': ['CHEBI:33855']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183810,
    'num_false_negatives': 12,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999347194568659}