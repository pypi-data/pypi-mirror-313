"""
Classifies: CHEBI:189840 dicarboxylic fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_dicarboxylic_fatty_acid(smiles: str):
    """
    Determines if a molecule is a dicarboxylic fatty acid (contains 2 carboxylic acid groups).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a dicarboxylic fatty acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Find carboxylic acid groups (C(=O)OH)
    carboxyl_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    matches = mol.GetSubstructMatches(carboxyl_pattern)
    
    if len(matches) != 2:
        return False, f"Found {len(matches)} carboxylic acid groups, needs exactly 2"
        
    # Check if molecule contains a carbon chain
    carbon_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'C']
    if len(carbon_atoms) < 2:
        return False, "Insufficient carbon atoms for a fatty acid chain"

    # Success case - if we have 2 carboxylic acids and multiple carbons, consider it a dicarboxylic fatty acid
    num_carbons = len(carbon_atoms)
    return True, f"Valid dicarboxylic fatty acid with {num_carbons} carbons and 2 carboxylic acid groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:189840',
                          'name': 'dicarboxylic fatty acid',
                          'definition': 'Any fatty acid containing two carboxy '
                                        'groups.',
                          'parents': ['CHEBI:35692', 'CHEBI:61697']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Range Error\n'
               '\tidx\n'
               '\tViolation occurred on line 329 in file '
               'Code/GraphMol/ROMol.cpp\n'
               '\tFailed Expression: 24 < 24\n'
               '\tRDKIT: 2024.03.6\n'
               '\tBOOST: 1_85\n',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 8,
    'num_false_positives': 100,
    'num_true_negatives': 3174,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.07407407407407407,
    'recall': 1.0,
    'f1': 0.13793103448275862,
    'accuracy': 0.9695307739183425}