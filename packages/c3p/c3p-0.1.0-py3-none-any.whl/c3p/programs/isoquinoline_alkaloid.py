"""
Classifies: CHEBI:24921 isoquinoline alkaloid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_isoquinoline_alkaloid(smiles: str):
    """
    Determines if a molecule is an isoquinoline alkaloid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an isoquinoline alkaloid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for nitrogen atom
    if not any(atom.GetSymbol() == 'N' for atom in mol.GetAtoms()):
        return False, "No nitrogen atom found - required for alkaloid"
        
    # Generate ring information
    rings = mol.GetRingInfo()
    if not rings.NumRings():
        return False, "No rings found"
        
    # Look for fused ring systems
    ring_atoms = rings.AtomRings()
    
    # Find 6,6 fused ring systems where one ring contains N
    found_isoquinoline = False
    for i in range(len(ring_atoms)):
        for j in range(i+1, len(ring_atoms)):
            ring1 = set(ring_atoms[i])
            ring2 = set(ring_atoms[j])
            shared = ring1.intersection(ring2)
            
            # Check if rings share exactly 2 atoms (fused)
            if len(shared) == 2:
                # Check ring sizes
                if len(ring1) == 6 and len(ring2) == 6:
                    # Check if one ring contains N
                    ring1_atoms = [mol.GetAtomWithIdx(idx) for idx in ring1]
                    ring2_atoms = [mol.GetAtomWithIdx(idx) for idx in ring2]
                    
                    if (any(atom.GetSymbol() == 'N' for atom in ring1_atoms) or 
                        any(atom.GetSymbol() == 'N' for atom in ring2_atoms)):
                        found_isoquinoline = True
                        break
                        
    if not found_isoquinoline:
        return False, "No isoquinoline core structure found"
        
    # Check for aromaticity in at least one ring
    aromatic_atoms = sum(1 for atom in mol.GetAtoms() if atom.GetIsAromatic())
    if aromatic_atoms < 6:
        return False, "No aromatic ring found"
        
    # Additional check for typical alkaloid characteristics
    # Most alkaloids have at least one N with a methyl group or in a ring
    n_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'N']
    valid_n = False
    for n in n_atoms:
        if n.IsInRing() or any(neighbor.GetSymbol() == 'C' for neighbor in n.GetNeighbors()):
            valid_n = True
            break
            
    if not valid_n:
        return False, "Nitrogen atom not characteristic of alkaloid structure"
        
    return True, "Contains isoquinoline core structure with alkaloid characteristics"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24921',
                          'name': 'isoquinoline alkaloid',
                          'definition': 'Any alkaloid that has a structure '
                                        'based on an isoquinoline nucleus. '
                                        'They are derived from the amino acids '
                                        'like tyrosine and phenylalanine.',
                          'parents': ['CHEBI:22315']},
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
    'num_true_positives': 32,
    'num_false_positives': 100,
    'num_true_negatives': 2252,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.24242424242424243,
    'recall': 0.8421052631578947,
    'f1': 0.3764705882352941,
    'accuracy': 0.9556485355648535}