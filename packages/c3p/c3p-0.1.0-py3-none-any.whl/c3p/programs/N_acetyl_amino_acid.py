"""
Classifies: CHEBI:21575 N-acetyl-amino acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_N_acetyl_amino_acid(smiles: str):
    """
    Determines if a molecule is an N-acetyl amino acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an N-acetyl amino acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Look for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"

    # Look for N-acetyl group (N-C(=O)-CH3)
    acetyl_pattern = Chem.MolFromSmarts('[NX3;H1,H2][CX3](=O)[CH3]')
    if not mol.HasSubstructMatch(acetyl_pattern):
        return False, "No N-acetyl group found"

    # Look for alpha carbon with NH group
    alpha_carbon_pattern = Chem.MolFromSmarts('[NX3;H1,H2][CX4;H1]C(=O)[OH1]')
    if not mol.HasSubstructMatch(alpha_carbon_pattern):
        return False, "No alpha carbon with NH group found"

    # Additional check to ensure the N-acetyl is connected to the alpha carbon
    connected_pattern = Chem.MolFromSmarts('[CH3]C(=O)[NH1][CH1]C(=O)[OH1]')
    if not mol.HasSubstructMatch(connected_pattern):
        return False, "N-acetyl group not connected to amino acid alpha carbon"

    # Get the alpha carbon and check its substitution pattern
    matches = mol.GetSubstructMatches(alpha_carbon_pattern)
    if matches:
        alpha_carbon_idx = matches[0][1]  # Index of alpha carbon from pattern match
        alpha_carbon = mol.GetAtomWithIdx(alpha_carbon_idx)
        
        # Count non-H substituents on alpha carbon
        non_h_neighbors = len([n for n in alpha_carbon.GetNeighbors() 
                             if n.GetSymbol() != 'H'])
        
        if non_h_neighbors != 3:  # Should have exactly 3 non-H neighbors
            return False, "Incorrect substitution pattern on alpha carbon"

    # If we've passed all checks, it's an N-acetyl amino acid
    return True, "Molecule contains N-acetyl group attached to amino acid structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:21575',
                          'name': 'N-acetyl-amino acid',
                          'definition': 'An N-acyl-amino acid that has acetyl '
                                        'as the acyl group.',
                          'parents': [   'CHEBI:22160',
                                         'CHEBI:22195',
                                         'CHEBI:51569']},
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
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 122680,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 0.8,
    'f1': 0.07339449541284404,
    'accuracy': 0.9991774239524371}