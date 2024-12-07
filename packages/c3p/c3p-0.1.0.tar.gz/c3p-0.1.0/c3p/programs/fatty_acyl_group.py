"""
Classifies: CHEBI:24027 fatty-acyl group
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_fatty_acyl_group(smiles: str):
    """
    Determines if a molecule is a fatty acyl group.
    A fatty acyl group is formed by loss of OH from the carboxy group of a fatty acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a fatty acyl group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check for presence of C=O group
    carbonyl_pattern = Chem.MolFromSmarts('[C](=O)[*]')
    if not mol.HasSubstructMatch(carbonyl_pattern):
        return False, "No acyl group (C=O) found"

    # Check for aliphatic chain
    carbon_chain = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            carbon_chain += 1
            
    if carbon_chain < 4:
        return False, "Carbon chain too short for fatty acyl group (less than 4 carbons)"

    # Check for allowed features
    allowed_elements = {'C', 'H', 'O', '*'}
    for atom in mol.GetAtoms():
        if atom.GetSymbol() not in allowed_elements:
            return False, f"Contains disallowed element: {atom.GetSymbol()}"

    # Count number of double/triple bonds
    double_bonds = 0
    triple_bonds = 0
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.DOUBLE:
            double_bonds += 1
        elif bond.GetBondType() == Chem.BondType.TRIPLE:
            triple_bonds += 1
            
    # Subtract 1 from double bonds to account for the C=O
    double_bonds -= 1
    
    # Build description
    features = []
    if double_bonds > 0:
        features.append(f"{double_bonds} double bond(s)")
    if triple_bonds > 0:
        features.append(f"{triple_bonds} triple bond(s)")
    if not features:
        features.append("saturated")
        
    chain_desc = f"{carbon_chain}-carbon"
    
    reason = f"Valid fatty acyl group: {chain_desc} chain, {', '.join(features)}"
    
    return True, reason


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24027',
                          'name': 'fatty-acyl group',
                          'definition': 'A fatty-acyl group is a group formed '
                                        'by loss of OH from the carboxy group '
                                        'of a fatty acid.',
                          'parents': ['CHEBI:27207']},
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
    'num_true_positives': 7,
    'num_false_positives': 100,
    'num_true_negatives': 430,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.06542056074766354,
    'recall': 1.0,
    'f1': 0.12280701754385964,
    'accuracy': 0.813780260707635}