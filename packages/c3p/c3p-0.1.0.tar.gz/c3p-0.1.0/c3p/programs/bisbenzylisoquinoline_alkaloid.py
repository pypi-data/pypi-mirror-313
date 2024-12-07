"""
Classifies: CHEBI:133004 bisbenzylisoquinoline alkaloid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdDecomposition

def is_bisbenzylisoquinoline_alkaloid(smiles: str):
    """
    Determines if a molecule is a bisbenzylisoquinoline alkaloid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a bisbenzylisoquinoline alkaloid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for presence of two isoquinoline cores
    isoquinoline_pattern = Chem.MolFromSmarts('c1cncc2ccccc12') 
    matches = mol.GetSubstructMatches(isoquinoline_pattern)
    if len(matches) < 2:
        return False, "Does not contain two isoquinoline cores"

    # Check for presence of ether bridges
    ether_pattern = Chem.MolFromSmarts('cOc')
    ether_matches = mol.GetSubstructMatches(ether_pattern)
    if len(ether_matches) < 1:
        return False, "Does not contain ether bridges between isoquinoline units"

    # Check for N-methylated amines
    n_methyl_pattern = Chem.MolFromSmarts('[NX3]C')
    n_methyl_matches = mol.GetSubstructMatches(n_methyl_pattern)
    if len(n_methyl_matches) < 2:
        return False, "Does not contain N-methylated amines"

    # Check for benzyl groups
    benzyl_pattern = Chem.MolFromSmarts('c1ccccc1C')
    benzyl_matches = mol.GetSubstructMatches(benzyl_pattern)
    if len(benzyl_matches) < 2:
        return False, "Does not contain benzyl groups"

    # Additional checks for common substituents
    methoxy_pattern = Chem.MolFromSmarts('OC')
    methylenedioxy_pattern = Chem.MolFromSmarts('OCO')
    
    methoxy_count = len(mol.GetSubstructMatches(methoxy_pattern))
    methylenedioxy_count = len(mol.GetSubstructMatches(methylenedioxy_pattern))

    substituents = []
    if methoxy_count > 0:
        substituents.append(f"{methoxy_count} methoxy groups")
    if methylenedioxy_count > 0:
        substituents.append(f"{methylenedioxy_count} methylenedioxy groups")

    reason = "Contains two benzylisoquinoline units connected by ether bridges"
    if substituents:
        reason += f" with {', '.join(substituents)}"

    return True, reason


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:133004',
                          'name': 'bisbenzylisoquinoline alkaloid',
                          'definition': 'A type of benzylisoquinoline alkaloid '
                                        'whose structures are built up of two '
                                        'benzylisoquinoline units linked by '
                                        'ether bridges. Various structural '
                                        'patterns resulting from additional '
                                        'bridging between the two units by '
                                        'direct carbon-carbon bridging or by '
                                        'methylenedioxy groups are common.',
                          'parents': ['CHEBI:22750']},
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
    'success': False,
    'best': True,
    'error': "cannot import name 'rdDecomposition' from 'rdkit.Chem' "
             '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}