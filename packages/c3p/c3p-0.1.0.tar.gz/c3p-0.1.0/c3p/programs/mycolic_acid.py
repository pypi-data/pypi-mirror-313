"""
Classifies: CHEBI:25438 mycolic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_mycolic_acid(smiles: str):
    """
    Determines if a molecule is a mycolic acid based on structural features.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a mycolic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"
        
    # Check for beta-hydroxy group
    beta_hydroxy_pattern = Chem.MolFromSmarts('CC(O)C')
    if not mol.HasSubstructMatch(beta_hydroxy_pattern):
        return False, "No beta-hydroxy group found"
        
    # Check for long carbon chain (at least 20 carbons)
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 20:
        return False, "Carbon chain too short for mycolic acid"
        
    # Check for cyclopropyl groups (optional feature)
    cyclopropyl_pattern = Chem.MolFromSmarts('C1CC1')
    has_cyclopropyl = mol.HasSubstructMatch(cyclopropyl_pattern)
    
    # Check for keto group (optional feature)
    keto_pattern = Chem.MolFromSmarts('CC(=O)C')
    has_keto = mol.HasSubstructMatch(keto_pattern)
    
    # Classify type of mycolic acid
    if has_keto:
        return True, "Keto mycolic acid identified"
    elif has_cyclopropyl:
        return True, "Alpha-mycolic acid with cyclopropyl groups identified"
    else:
        return True, "Mycolic acid identified (basic structure)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25438',
                          'name': 'mycolic acid',
                          'definition': 'Mycolic acids are alpha-branched, '
                                        'beta-hydroxy long-chain fatty acids '
                                        'found in the cell walls of the '
                                        'mycolata taxon, a group of bacteria '
                                        'that includes Mycobacterium '
                                        'tuberculosis, the causative agent of '
                                        'the disease tuberculosis.',
                          'parents': ['CHEBI:35819']},
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
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 1464,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9361430395913155}