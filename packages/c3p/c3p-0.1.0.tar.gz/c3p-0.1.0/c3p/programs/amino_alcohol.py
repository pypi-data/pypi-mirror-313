"""
Classifies: CHEBI:22478 amino alcohol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.MolStandardize import rdMolStandardize

def is_amino_alcohol(smiles: str):
    """
    Determines if a molecule is an amino alcohol (contains both amino and hydroxyl groups).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an amino alcohol, False otherwise
        str: Reason for classification
    """
    # Convert SMILES to molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Standardize the molecule (uncharge, neutralize, etc)
    uncharger = rdMolStandardize.Uncharger()
    mol = uncharger.uncharge(mol)

    # Find alcohol (hydroxyl) groups
    alcohol_pattern = Chem.MolFromSmarts("[#6][OX2H]")
    alcohols = mol.GetSubstructMatches(alcohol_pattern)
    
    # Find primary and secondary amino groups
    amino_patterns = [
        Chem.MolFromSmarts("[NX3;H2][CX4]"), # Primary amine
        Chem.MolFromSmarts("[NX3;H1]([CX4])[CX4]"), # Secondary amine
        Chem.MolFromSmarts("[NX3]([CX4])([CX4])[CX4]"), # Tertiary amine
        Chem.MolFromSmarts("[NX3]"), # Any amine
    ]
    
    amino_groups = []
    for pattern in amino_patterns:
        matches = mol.GetSubstructMatches(pattern)
        amino_groups.extend(matches)
    
    # Remove duplicates
    amino_groups = list(set(amino_groups))
    
    if not alcohols:
        return False, "No alcohol groups found"
        
    if not amino_groups:
        return False, "No amino groups found"
        
    # Count the functional groups
    n_alcohols = len(alcohols)
    n_amines = len(amino_groups)
    
    return True, f"Found {n_alcohols} alcohol group(s) and {n_amines} amino group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22478',
                          'name': 'amino alcohol',
                          'definition': 'An alcohol containing an amino '
                                        'functional group in addition to the '
                                        'alcohol-defining hydroxy group.',
                          'parents': ['CHEBI:30879', 'CHEBI:50047']},
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
    'num_true_positives': 33,
    'num_false_positives': 100,
    'num_true_negatives': 137,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.24812030075187969,
    'recall': 1.0,
    'f1': 0.3975903614457831,
    'accuracy': 0.6296296296296297}