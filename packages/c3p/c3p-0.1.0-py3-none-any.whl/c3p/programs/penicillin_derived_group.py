"""
Classifies: CHEBI:139226 penicillin-derived group
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_penicillin_derived_group(smiles: str):
    """
    Determines if a molecule is a penicillin-derived group.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a penicillin-derived group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for presence of beta-lactam fused to thiazolidine ring core structure
    beta_lactam_thiazolidine_pattern = Chem.MolFromSmarts('[#7]1[C@H]2SC([C@@H]1[*])[C@H]2[*]')
    if not mol.HasSubstructMatch(beta_lactam_thiazolidine_pattern):
        return False, "Missing characteristic beta-lactam fused to thiazolidine ring system"
        
    # Check for presence of carboxyl group or derivative
    carboxyl_pattern = Chem.MolFromSmarts('C(=O)[OH,O-,N,*]')
    if not mol.HasSubstructMatch(carboxyl_pattern):
        return False, "Missing carboxyl group or derivative"
        
    # Check for presence of at least one amide group
    amide_pattern = Chem.MolFromSmarts('NC(=O)')
    if not mol.HasSubstructMatch(amide_pattern):
        return False, "Missing amide group"
        
    # Check for presence of gem-dimethyl groups on thiazolidine ring
    gem_dimethyl_pattern = Chem.MolFromSmarts('C([CH3])([CH3])')
    if not mol.HasSubstructMatch(gem_dimethyl_pattern):
        return False, "Missing gem-dimethyl groups"
        
    # If all checks pass, determine specific type of penicillin derivative
    if mol.HasSubstructMatch(Chem.MolFromSmarts('NC(=O)C(C)OC1=CC=CC=C1')):
        return True, "Phenethicilloyl group"
    elif mol.HasSubstructMatch(Chem.MolFromSmarts('NC(=O)COC1=CC=CC=C1')):
        return True, "Phenoxymethylpenicillanyl group"
    else:
        return True, "Unspecified penicillin-derived group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139226',
                          'name': 'penicillin-derived group',
                          'definition': 'Any organyl group derived from a '
                                        'penicillin.',
                          'parents': ['CHEBI:33249']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183915,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999891255294507}