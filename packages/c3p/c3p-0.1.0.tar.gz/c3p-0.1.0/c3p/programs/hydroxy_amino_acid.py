"""
Classifies: CHEBI:24662 hydroxy-amino acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroxy_amino_acid(smiles: str):
    """
    Determines if a molecule is a hydroxy-amino acid (non-proteinogenic alpha-amino acid with one or more hydroxy groups).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydroxy-amino acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"

    # Check for amine group (primary, secondary or tertiary)
    amine_pattern = Chem.MolFromSmarts('[NX3;H2,H1,H0]')
    if not mol.HasSubstructMatch(amine_pattern):
        return False, "No amine group found"

    # Check for hydroxy group
    hydroxy_pattern = Chem.MolFromSmarts('[OH]')
    hydroxy_matches = mol.GetSubstructMatches(hydroxy_pattern)
    
    # Don't count the OH from carboxylic acid
    carboxylic_matches = mol.GetSubstructMatches(carboxylic_pattern)
    carboxylic_o_indices = set(match[1] for match in carboxylic_matches)  # Get O indices from COOH
    
    true_hydroxy_matches = []
    for match in hydroxy_matches:
        if match[0] not in carboxylic_o_indices:
            true_hydroxy_matches.append(match)
            
    if not true_hydroxy_matches:
        return False, "No hydroxy groups found (excluding carboxylic acid OH)"

    # Check if amine and carboxylic acid are on same carbon (alpha position)
    alpha_amino_acid_pattern = Chem.MolFromSmarts('[NX3;H2,H1,H0][CH1]C(=O)[OH]')
    if not mol.HasSubstructMatch(alpha_amino_acid_pattern):
        return False, "Amine and carboxylic acid groups not in alpha position"

    # Count number of hydroxy groups (excluding carboxylic acid OH)
    num_hydroxy = len(true_hydroxy_matches)

    return True, f"Hydroxy-amino acid with {num_hydroxy} hydroxy group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24662',
                          'name': 'hydroxy-amino acid',
                          'definition': 'A non-proteinogenic alpha-amino acid '
                                        'bearing one or more hydroxy groups at '
                                        'unspecified positions.',
                          'parents': ['CHEBI:83925']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Invariant Violation\n'
               '\t\n'
               '\tViolation occurred on line 341 in file '
               'Code/GraphMol/Matrices.cpp\n'
               '\tFailed Expression: aid1 != aid2\n'
               '\tRDKIT: 2024.03.6\n'
               '\tBOOST: 1_85\n',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 12,
    'num_false_positives': 100,
    'num_true_negatives': 1437,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.10714285714285714,
    'recall': 1.0,
    'f1': 0.19354838709677416,
    'accuracy': 0.9354422207876049}