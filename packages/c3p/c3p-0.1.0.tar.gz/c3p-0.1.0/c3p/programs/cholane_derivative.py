"""
Classifies: CHEBI:131657 cholane derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect
from rdkit.Chem import rdMolDescriptors

def is_cholane_derivative(smiles: str):
    """
    Determines if a molecule is a cholane derivative based on steroid skeleton.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a cholane derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for basic molecular properties consistent with cholane derivatives
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if num_carbons < 24:  # Cholane skeleton has 24 carbons
        return False, "Too few carbons for cholane skeleton"

    # Count number of rings
    ring_info = mol.GetRingInfo()
    if len(ring_info.AtomRings()) < 4:
        return False, "Missing required ring systems"

    # Check for steroid core - should have 4 fused rings
    ring_counts = rdMolDescriptors.CalcNumRings(mol)
    if ring_counts < 4:
        return False, "Does not contain required 4-ring steroid core"

    # Check for characteristic 6-6-6-5 ring pattern of steroids
    rings = ring_info.AtomRings()
    six_membered = sum(1 for ring in rings if len(ring) == 6)
    five_membered = sum(1 for ring in rings if len(ring) == 5)
    
    if six_membered < 3 or five_membered < 1:
        return False, "Does not match characteristic steroid ring pattern (6-6-6-5)"

    # Look for characteristic methyl groups at C-18 and C-19 positions
    # This is a simplified check for branching patterns
    branching_points = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and len([n for n in atom.GetNeighbors()]) == 4:
            branching_points += 1

    if branching_points < 2:
        return False, "Missing characteristic methyl branching points"

    # If all checks pass, it's likely a cholane derivative
    return True, "Contains cholane skeleton with characteristic steroid core structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131657',
                          'name': 'cholane derivative',
                          'definition': 'Any steroid (or derivative) based on '
                                        'a cholane skeleton.',
                          'parents': ['CHEBI:35341']},
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
    'num_true_negatives': 2128,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9551569506726457}