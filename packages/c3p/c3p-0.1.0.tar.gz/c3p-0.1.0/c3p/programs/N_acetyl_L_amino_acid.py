"""
Classifies: CHEBI:21545 N-acetyl-L-amino acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect

def is_N_acetyl_L_amino_acid(smiles: str):
    """
    Determines if a molecule is an N-acetyl-L-amino acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an N-acetyl-L-amino acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for carboxylic acid group
    carboxyl_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxyl_pattern):
        return False, "No carboxylic acid group found"
        
    # Check for N-acetyl group
    n_acetyl_pattern = Chem.MolFromSmarts('NC(=O)C')
    if not mol.HasSubstructMatch(n_acetyl_pattern):
        return False, "No N-acetyl group found"
        
    # Check for alpha carbon with correct stereochemistry
    alpha_carbon_pattern = Chem.MolFromSmarts('[C@@H](N)(C(=O)O)C')
    alpha_carbon_pattern_alt = Chem.MolFromSmarts('[C@H](N)(C(=O)O)C') 
    
    if not (mol.HasSubstructMatch(alpha_carbon_pattern) or mol.HasSubstructMatch(alpha_carbon_pattern_alt)):
        return False, "No alpha carbon with correct stereochemistry found"
        
    # Additional check to ensure N-acetyl is connected to alpha carbon
    matches = mol.GetSubstructMatches(Chem.MolFromSmarts('CC(=O)N[C@@H](C)C(O)=O'))
    matches_alt = mol.GetSubstructMatches(Chem.MolFromSmarts('CC(=O)N[C@H](C)C(O)=O'))
    
    if not (matches or matches_alt):
        return False, "N-acetyl group not properly connected to alpha carbon"
    
    # If all checks pass, it's an N-acetyl-L-amino acid
    return True, "Molecule contains N-acetyl group, carboxylic acid, and correct stereochemistry"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:21545',
                          'name': 'N-acetyl-L-amino acid',
                          'definition': 'An L-amino acid having an N-acetyl '
                                        'substituent.',
                          'parents': [   'CHEBI:21575',
                                         'CHEBI:21644',
                                         'CHEBI:22160']},
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
    'num_true_negatives': 1479,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 0.6666666666666666,
    'f1': 0.03809523809523809,
    'accuracy': 0.9361567635903919}