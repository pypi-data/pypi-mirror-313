"""
Classifies: CHEBI:22750 benzylisoquinoline alkaloid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_benzylisoquinoline_alkaloid(smiles: str):
    """
    Determines if a molecule is a benzylisoquinoline alkaloid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a benzylisoquinoline alkaloid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of nitrogen (required for alkaloid)
    if not any(atom.GetAtomicNum() == 7 for atom in mol.GetAtoms()):
        return False, "No nitrogen atoms found - required for alkaloid"

    # Look for isoquinoline core structure (including reduced forms)
    isoquinoline_patterns = [
        Chem.MolFromSmarts('c1nccc2ccccc12'), # Basic isoquinoline
        Chem.MolFromSmarts('[#6]1[#7][#6][#6][#6]2[#6][#6][#6][#6][#6]12'), # Reduced isoquinoline
        Chem.MolFromSmarts('[#6]1[#7][#6][#6][#6]2[#6][#6][#6][#6][#6]12') # Alternative reduced form
    ]
    
    has_isoquinoline = False
    for pattern in isoquinoline_patterns:
        if pattern is not None and mol.HasSubstructMatch(pattern):
            has_isoquinoline = True
            break
            
    if not has_isoquinoline:
        return False, "No isoquinoline or reduced isoquinoline core found"

    # Look for benzyl group or modified benzyl group attachment
    benzyl_patterns = [
        Chem.MolFromSmarts('c1ccccc1C'), # Basic benzyl
        Chem.MolFromSmarts('c1ccccc1[CH2,CH]'), # Modified benzyl
        Chem.MolFromSmarts('c1c(O)c(O)ccc1C') # Hydroxylated benzyl
    ]
    
    has_benzyl = False
    for pattern in benzyl_patterns:
        if pattern is not None and mol.HasSubstructMatch(pattern):
            has_benzyl = True
            break
            
    if not has_benzyl:
        return False, "No benzyl or modified benzyl group found"

    # Check for common substituents
    substituent_patterns = {
        'methoxy': Chem.MolFromSmarts('OC'),
        'hydroxy': Chem.MolFromSmarts('[OH]'),
        'methylenedioxy': Chem.MolFromSmarts('OCO')
    }
    
    features = []
    for name, pattern in substituent_patterns.items():
        if pattern is not None and mol.HasSubstructMatch(pattern):
            features.append(name)

    # Count rings
    ring_info = mol.GetRingInfo()
    num_rings = ring_info.NumRings()
    
    if num_rings < 2:
        return False, "Insufficient ring systems for benzylisoquinoline structure"

    feature_str = ", ".join(features) if features else "no additional"
    return True, f"Contains isoquinoline core, benzyl group, and {feature_str} substituents with {num_rings} ring systems"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22750',
                          'name': 'benzylisoquinoline alkaloid',
                          'definition': 'Any isoquinoline alkaloid based on a '
                                        'benzylisoquinoline skeleton.',
                          'parents': ['CHEBI:24921']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: cannot import name 'rdDecomposition' from "
               "'rdkit.Chem' "
               '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 12,
    'num_false_positives': 100,
    'num_true_negatives': 11544,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.10714285714285714,
    'recall': 1.0,
    'f1': 0.19354838709677416,
    'accuracy': 0.9914207275223061}