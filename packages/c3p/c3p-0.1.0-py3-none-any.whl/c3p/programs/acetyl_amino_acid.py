"""
Classifies: CHEBI:22195 acetyl-amino acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdmolops

def is_acetyl_amino_acid(smiles: str):
    """
    Determines if a molecule is an acetyl amino acid derivative.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an acetyl amino acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for carboxylic acid group
    carboxylic_acid_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_acid_pattern):
        return False, "No carboxylic acid group found"

    # Check for acetyl group (CH3C(=O)-)
    acetyl_pattern = Chem.MolFromSmarts('CC(=O)')
    if not mol.HasSubstructMatch(acetyl_pattern):
        return False, "No acetyl group found"
        
    # Check for N-acetyl pattern (CH3C(=O)N)
    n_acetyl_pattern = Chem.MolFromSmarts('CC(=O)N')
    n_acetyl_matches = mol.GetSubstructMatches(n_acetyl_pattern)
    
    # Check for O-acetyl pattern (CH3C(=O)O)
    o_acetyl_pattern = Chem.MolFromSmarts('CC(=O)O')
    o_acetyl_matches = mol.GetSubstructMatches(o_acetyl_pattern)
    
    if not (n_acetyl_matches or o_acetyl_matches):
        return False, "No N-acetyl or O-acetyl group found"
    
    # Check for alpha carbon with amine/amide group
    alpha_carbon_pattern = Chem.MolFromSmarts('[NH,NH2][CH]C(=O)[OH]')
    if not mol.HasSubstructMatch(alpha_carbon_pattern):
        return False, "No alpha carbon with amine/amide group found"
    
    # Determine if N-acetyl or O-acetyl
    if n_acetyl_matches:
        acetyl_type = "N-acetyl"
    else:
        acetyl_type = "O-acetyl"
        
    # Check for chirality
    chiral_centers = Chem.FindMolChiralCenters(mol)
    if chiral_centers:
        chirality = "with specified stereochemistry"
    else:
        chirality = "without specified stereochemistry"
        
    return True, f"{acetyl_type} amino acid derivative {chirality}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22195',
                          'name': 'acetyl-amino acid',
                          'definition': 'Any amino acid derivative that is the '
                                        'N-acetyl or O-acetyl derivative of an '
                                        'amino acid.',
                          'parents': ['CHEBI:83821']},
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
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 1361,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.931787175989086}