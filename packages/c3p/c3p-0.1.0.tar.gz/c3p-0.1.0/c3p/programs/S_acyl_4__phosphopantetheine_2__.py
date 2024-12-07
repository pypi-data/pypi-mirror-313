"""
Classifies: CHEBI:132023 S-acyl-4'-phosphopantetheine(2-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_S_acyl_4__phosphopantetheine_2__(smiles: str):
    """
    Determines if a molecule is an S-acyl-4'-phosphopantetheine(2-).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an S-acyl-4'-phosphopantetheine(2-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for phosphate group with 2 negative charges
    phosphate_pattern = Chem.MolFromSmarts("[O-]P(=O)([O-])O")
    if not mol.HasSubstructMatch(phosphate_pattern):
        return False, "Missing phosphate group with 2 negative charges"

    # Check for pantetheine core structure
    pantetheine_pattern = Chem.MolFromSmarts("NC(=O)CCNC(=O)C(O)C(C)(C)COP([O-])(=O)[O-]")
    if not mol.HasSubstructMatch(pantetheine_pattern):
        return False, "Missing pantetheine core structure"

    # Check for S-acyl group
    s_acyl_pattern = Chem.MolFromSmarts("CSC(=O)C")
    if not mol.HasSubstructMatch(s_acyl_pattern):
        return False, "Missing S-acyl group"

    # Get length of acyl chain
    acyl_chain_pattern = Chem.MolFromSmarts("CSC(=O)CCCCC")
    matches = mol.GetSubstructMatches(acyl_chain_pattern)
    if matches:
        chain_atoms = len(matches[0])
        return True, f"S-acyl-4'-phosphopantetheine(2-) with {chain_atoms-5} carbon acyl chain"
    
    return True, "S-acyl-4'-phosphopantetheine(2-)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:132023',
                          'name': "S-acyl-4'-phosphopantetheine(2-)",
                          'definition': 'A phosphopantetheine anion obtained '
                                        'by deprotonation of the phosphate OH '
                                        'groups of any '
                                        "S-acyl-4'-phosphopantetheine; major "
                                        'species at pH 7.3.',
                          'parents': ['CHEBI:67051']},
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
    'num_false_positives': 1,
    'num_true_negatives': 183913,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.6666666666666666,
    'recall': 1.0,
    'f1': 0.8,
    'accuracy': 0.9999945627351617}