"""
Classifies: CHEBI:131620 C24-steroid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_C24_steroid(smiles: str):
    """
    Determines if a molecule is a C24-steroid (steroid with 24-carbon cholane skeleton).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a C24-steroid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check total number of carbons
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if num_carbons != 24:
        return False, f"Contains {num_carbons} carbons, not 24"
        
    # Check for steroid core structure (4 fused rings)
    # Generate ring info
    rings = mol.GetRingInfo()
    if not rings.NumRings():
        return False, "No rings found"
        
    # Get all rings of size 6 or 5 (steroid core has 3x6 + 1x5)
    ring_sizes = [len(ring) for ring in rings.AtomRings()]
    six_rings = sum(1 for size in ring_sizes if size == 6) 
    five_rings = sum(1 for size in ring_sizes if size == 5)
    
    if six_rings < 3 or five_rings < 1:
        return False, f"Does not have steroid core structure (3x6 + 1x5 rings). Found {six_rings}x6 and {five_rings}x5 rings"
        
    # Check for fused ring system by looking for shared atoms between rings
    ring_atoms = list(rings.AtomRings())
    
    # Check if rings share atoms (are fused)
    fused = False
    for i in range(len(ring_atoms)):
        for j in range(i+1, len(ring_atoms)):
            if set(ring_atoms[i]).intersection(set(ring_atoms[j])):
                fused = True
                break
        if fused:
            break
            
    if not fused:
        return False, "Rings are not fused"
        
    # If we get here, it has 24 carbons and steroid-like ring structure
    return True, "Contains 24 carbons and steroid core structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131620',
                          'name': 'C24-steroid',
                          'definition': 'A steroid compound with a structure '
                                        'based on a 24-carbon (cholane) '
                                        'skeleton.',
                          'parents': ['CHEBI:131657']},
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
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 12645,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9921550168667137}