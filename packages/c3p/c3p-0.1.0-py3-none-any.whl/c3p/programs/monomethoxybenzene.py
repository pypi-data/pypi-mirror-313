"""
Classifies: CHEBI:25235 monomethoxybenzene
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_monomethoxybenzene(smiles: str):
    """
    Determines if a molecule contains a benzene ring substituted with exactly one methoxy group.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule contains monomethoxybenzene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Find all benzene rings
    rings = mol.GetRingInfo()
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms) and \
               all(atom.GetSymbol() == 'C' for atom in atoms):
                aromatic_rings.append(ring)
                
    if not aromatic_rings:
        return False, "No benzene rings found"

    # Look for methoxy groups (-OCH3) attached to benzene rings
    methoxy_count = 0
    for ring in aromatic_rings:
        ring_atoms = set(ring)
        for atom_idx in ring:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O' and neighbor.GetIdx() not in ring_atoms:
                    # Check if oxygen is connected to a methyl group
                    for o_neighbor in neighbor.GetNeighbors():
                        if o_neighbor.GetIdx() not in ring_atoms:
                            if o_neighbor.GetSymbol() == 'C' and \
                               len([n for n in o_neighbor.GetNeighbors() if n.GetSymbol() == 'H']) == 3:
                                methoxy_count += 1

    if methoxy_count == 0:
        return False, "No methoxy groups found"
    elif methoxy_count == 1:
        return True, "Contains exactly one methoxy group attached to benzene"
    else:
        return False, f"Found {methoxy_count} methoxy groups (more than one)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25235',
                          'name': 'monomethoxybenzene',
                          'definition': 'Compounds containing a benzene '
                                        'skeleton substituted with one methoxy '
                                        'group.',
                          'parents': ['CHEBI:51683']},
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
    'num_false_positives': 1,
    'num_true_negatives': 183602,
    'num_false_negatives': 33,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9998148511185171}