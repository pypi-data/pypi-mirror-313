"""
Classifies: CHEBI:25392 naphthols
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_naphthols(smiles: str):
    """
    Determines if a molecule is a naphthol (hydroxynaphthalene derivative with single OH group).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a naphthol, False otherwise
        str: Reason for classification
    """
    # Parse SMILES
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for naphthalene core
    rings = mol.GetRingInfo()
    
    # Find fused 6-membered rings
    fused_rings = []
    for ring1 in rings.AtomRings():
        if len(ring1) != 6:
            continue
        for ring2 in rings.AtomRings():
            if len(ring2) != 6 or ring1 == ring2:
                continue
            # Check if rings share exactly 2 atoms
            shared = set(ring1).intersection(set(ring2))
            if len(shared) == 2:
                fused_rings.append((ring1, ring2))
                
    if not fused_rings:
        return False, "No fused 6-membered rings found"
        
    # Check for naphthalene core (two fused aromatic 6-membered rings)
    naphthalene_found = False
    for ring1, ring2 in fused_rings:
        atoms1 = [mol.GetAtomWithIdx(i) for i in ring1]
        atoms2 = [mol.GetAtomWithIdx(i) for i in ring2]
        
        if (all(atom.GetIsAromatic() for atom in atoms1) and 
            all(atom.GetIsAromatic() for atom in atoms2) and
            all(atom.GetSymbol() == 'C' for atom in atoms1) and 
            all(atom.GetSymbol() == 'C' for atom in atoms2)):
            naphthalene_found = True
            naphthalene_atoms = set(ring1).union(set(ring2))
            break
            
    if not naphthalene_found:
        return False, "No naphthalene core found"
        
    # Count hydroxy groups
    hydroxy_count = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O':
            # Check if oxygen is part of a hydroxy group
            neighbors = [n for n in atom.GetNeighbors()]
            if len(neighbors) == 1 and neighbors[0].GetSymbol() == 'C':
                hydroxy_count += 1
                
    if hydroxy_count == 0:
        return False, "No hydroxy groups found"
    elif hydroxy_count > 1:
        return False, f"Multiple ({hydroxy_count}) hydroxy groups found"
        
    # Check if at least one OH is attached to naphthalene core
    oh_on_core = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O':
            neighbors = [n for n in atom.GetNeighbors()]
            if (len(neighbors) == 1 and 
                neighbors[0].GetSymbol() == 'C' and 
                neighbors[0].GetIdx() in naphthalene_atoms):
                oh_on_core = True
                break
                
    if not oh_on_core:
        return False, "Hydroxy group not attached to naphthalene core"
        
    return True, "Single hydroxy group attached to naphthalene core"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25392',
                          'name': 'naphthols',
                          'definition': 'Any hydroxynaphthalene derivative '
                                        'that has a single hydroxy '
                                        'substituent.',
                          'parents': ['CHEBI:24727']},
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
    'num_true_positives': 3,
    'num_false_positives': 96,
    'num_true_negatives': 183643,
    'num_false_negatives': 16,
    'num_negatives': None,
    'precision': 0.030303030303030304,
    'recall': 0.15789473684210525,
    'f1': 0.05084745762711865,
    'accuracy': 0.999390502726412}