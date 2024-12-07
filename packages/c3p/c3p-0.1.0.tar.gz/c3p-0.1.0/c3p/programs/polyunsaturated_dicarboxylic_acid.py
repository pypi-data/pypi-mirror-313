"""
Classifies: CHEBI:134531 polyunsaturated dicarboxylic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_polyunsaturated_dicarboxylic_acid(smiles: str):
    """
    Determines if a molecule is a polyunsaturated dicarboxylic acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a polyunsaturated dicarboxylic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for exactly 2 carboxylic acid groups
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    carboxylic_matches = mol.GetSubstructMatches(carboxylic_pattern)
    
    if len(carboxylic_matches) != 2:
        return False, f"Found {len(carboxylic_matches)} carboxylic acid groups, need exactly 2"
        
    # Count double bonds excluding those in carboxylic groups
    double_bond_count = 0
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE:
            # Get atoms connected by this double bond
            begin_atom = bond.GetBeginAtom()
            end_atom = bond.GetEndAtom()
            
            # Skip if double bond is part of carboxylic group
            if not (begin_atom.GetSymbol() == 'O' or end_atom.GetSymbol() == 'O'):
                double_bond_count += 1
                
    if double_bond_count < 2:
        return False, f"Found {double_bond_count} C=C double bonds, need at least 2"
        
    return True, f"Valid polyunsaturated dicarboxylic acid with {double_bond_count} C=C double bonds"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134531',
                          'name': 'polyunsaturated dicarboxylic acid',
                          'definition': 'A dicarboxylic acid having 2 or more '
                                        'units of unsaturation.',
                          'parents': ['CHEBI:35692']},
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
    'num_false_positives': 100,
    'num_true_negatives': 21569,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.99538553827696}