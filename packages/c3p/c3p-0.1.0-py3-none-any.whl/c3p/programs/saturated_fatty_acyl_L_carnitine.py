"""
Classifies: CHEBI:133445 saturated fatty acyl-L-carnitine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_saturated_fatty_acyl_L_carnitine(smiles: str):
    """
    Determines if a molecule is a saturated fatty acyl-L-carnitine.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a saturated fatty acyl-L-carnitine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for carnitine core structure with ester linkage
    carnitine_pattern = Chem.MolFromSmarts('[C:1](=O)[O:2][C@H:3]([C:4][C:5](=O)[O-:6])[C:7][N+:8]([C:9])([C:10])[C:11]')
    if not mol.HasSubstructMatch(carnitine_pattern):
        return False, "Missing L-carnitine core structure with ester linkage"
    
    # Check for unsaturation in the molecule
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    if double_bond_pattern and mol.HasSubstructMatch(double_bond_pattern):
        return False, "Contains double bonds"
        
    triple_bond_pattern = Chem.MolFromSmarts('C#C')
    if triple_bond_pattern and mol.HasSubstructMatch(triple_bond_pattern):
        return False, "Contains triple bonds"
        
    aromatic_pattern = Chem.MolFromSmarts('a')
    if aromatic_pattern and mol.HasSubstructMatch(aromatic_pattern):
        return False, "Contains aromatic bonds"

    # Check for presence of exactly two ester/carboxylate groups
    ester_pattern = Chem.MolFromSmarts('C(=O)O')
    if ester_pattern and len(mol.GetSubstructMatches(ester_pattern)) != 2:
        return False, "Incorrect number of ester/carboxylate groups"

    # Count carbons in fatty acyl chain
    carnitine_carbons = 6  # Number of carbons in carnitine core
    total_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    acyl_chain_carbons = total_carbons - carnitine_carbons

    if acyl_chain_carbons < 1:
        return False, "No fatty acyl chain present"

    return True, f"Saturated fatty acyl-L-carnitine with {acyl_chain_carbons} carbons in fatty acyl chain"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:133445',
                          'name': 'saturated fatty acyl-L-carnitine',
                          'definition': 'An O-acylcarnitine in which the R is '
                                        'a saturated fatty acyl chain.',
                          'parents': ['CHEBI:176910', 'CHEBI:75659']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'True positives: []\n'
               'False positives: []\n'
               "False negatives: [('CCCC(=O)O[C@H](CC([O-])=O)C[N+](C)(C)C', "
               "'Incorrect number of ester groups'), "
               "('CC(C)C(=O)O[C@H](CC([O-])=O)C[N+](C)(C)C', 'Incorrect number "
               "of ester groups')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 87,
    'num_true_negatives': 183826,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02247191011235955,
    'recall': 1.0,
    'f1': 0.04395604395604395,
    'accuracy': 0.9995269553869994}