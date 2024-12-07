"""
Classifies: CHEBI:13209 long-chain fatty acid ethyl ester
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_long_chain_fatty_acid_ethyl_ester(smiles: str):
    """
    Determines if a molecule is a long-chain fatty acid ethyl ester.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a long-chain fatty acid ethyl ester, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of ethyl ester group (C(=O)OCC)
    ethyl_ester_pattern = Chem.MolFromSmarts('C(=O)OCC')
    if not mol.HasSubstructMatch(ethyl_ester_pattern):
        return False, "No ethyl ester group found"
    
    # Get carbon chain length
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 12:  # Generally long chain fatty acids have 12+ carbons
        return False, "Carbon chain too short for long-chain fatty acid"

    # Check for linear chain structure
    # Count number of carbons with more than 2 carbon neighbors (branching points)
    branching_points = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            carbon_neighbors = sum(1 for neighbor in atom.GetNeighbors() 
                                if neighbor.GetSymbol() == 'C')
            if carbon_neighbors > 2:
                branching_points += 1
    
    if branching_points > 0:
        return False, "Structure contains branching points"

    # Count double bonds using SMARTS pattern
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    double_bonds = len(mol.GetSubstructMatches(double_bond_pattern))
    
    # Classify based on saturation
    if double_bonds == 0:
        return True, f"Saturated long-chain fatty acid ethyl ester with {carbon_count} carbons"
    else:
        return True, f"Unsaturated long-chain fatty acid ethyl ester with {carbon_count} carbons and {double_bonds} double bonds"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:13209',
                          'name': 'long-chain fatty acid ethyl ester',
                          'definition': 'A fatty acid ethyl ester resulting '
                                        'from the formal condensation of the '
                                        'carboxy group of a long-chain fatty '
                                        'acid with the hydroxy group of '
                                        'ethanol.',
                          'parents': ['CHEBI:78206']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: module 'rdkit.Chem.rdMolDescriptors' has no "
               "attribute 'CalcNumAliphaticDoubleBonds'",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 1762,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9463519313304721}