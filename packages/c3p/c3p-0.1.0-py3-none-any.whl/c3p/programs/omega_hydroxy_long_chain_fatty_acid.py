"""
Classifies: CHEBI:140997 omega-hydroxy-long-chain fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_omega_hydroxy_long_chain_fatty_acid(smiles: str):
    """
    Determines if a molecule is an omega-hydroxy-long-chain fatty acid (C13-C22).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an omega-hydroxy-long-chain fatty acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)O')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"
        
    # Check for terminal hydroxyl group (omega position)
    terminal_oh_pattern = Chem.MolFromSmarts('CCO')
    if not mol.HasSubstructMatch(terminal_oh_pattern):
        return False, "No terminal hydroxyl group found"
        
    # Count total carbons
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    
    if carbon_count < 13:
        return False, f"Chain too short ({carbon_count} carbons)"
    if carbon_count > 22:
        return False, f"Chain too long ({carbon_count} carbons)"
    
    # Count hydroxyl groups (excluding the carboxylic acid OH)
    oh_pattern = Chem.MolFromSmarts('O[CH]')  # Matches hydroxyl groups attached to carbon
    oh_count = len(mol.GetSubstructMatches(oh_pattern))
    
    # At least one hydroxyl group should be terminal (omega position)
    if oh_count < 1:
        return False, "No hydroxyl groups found"
    
    return True, f"Omega-hydroxy fatty acid with {carbon_count} carbons and {oh_count} hydroxyl groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140997',
                          'name': 'omega-hydroxy-long-chain fatty acid',
                          'definition': 'A omega-hydroxy-fatty acid with a '
                                        'chain length ranging from C13 to C22.',
                          'parents': ['CHEBI:10615', 'CHEBI:15904']},
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
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 1588,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.9409332545776727}