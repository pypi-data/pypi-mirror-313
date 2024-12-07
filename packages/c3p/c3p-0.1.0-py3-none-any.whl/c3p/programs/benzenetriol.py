"""
Classifies: CHEBI:22707 benzenetriol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_benzenetriol(smiles: str):
    """
    Determines if a molecule is a benzenetriol (benzene with 3 hydroxy substituents).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a benzenetriol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Find aromatic rings
    rings = mol.GetRingInfo()
    
    # Get all 6-membered aromatic rings
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                # Check if ring is all carbon
                if all(atom.GetSymbol() == 'C' for atom in atoms):
                    aromatic_rings.append(ring)
                    
    if not aromatic_rings:
        return False, "No benzene rings found"
        
    # For each aromatic ring, count hydroxy substituents
    for ring in aromatic_rings:
        hydroxy_count = 0
        ring_atoms = set(ring)
        
        for atom_idx in ring:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                # Check if neighbor is oxygen
                if neighbor.GetIdx() not in ring_atoms and neighbor.GetSymbol() == 'O':
                    # Check if oxygen has a hydrogen
                    for o_neighbor in neighbor.GetNeighbors():
                        if o_neighbor.GetSymbol() == 'H':
                            hydroxy_count += 1
                            break
        
        if hydroxy_count == 3:
            return True, "Benzene ring with exactly 3 hydroxy substituents found"
            
    return False, "No benzene ring with exactly 3 hydroxy substituents found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22707',
                          'name': 'benzenetriol',
                          'definition': 'A triol in which three hydroxy groups '
                                        'are substituted onto a benzene ring.',
                          'parents': ['CHEBI:27136', 'CHEBI:33853']},
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
    'num_true_negatives': 183795,
    'num_false_negatives': 14,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999238339798378}