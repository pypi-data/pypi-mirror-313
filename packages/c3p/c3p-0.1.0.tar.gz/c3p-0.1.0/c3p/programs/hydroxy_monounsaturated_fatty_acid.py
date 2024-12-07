"""
Classifies: CHEBI:131869 hydroxy monounsaturated fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_hydroxy_monounsaturated_fatty_acid(smiles: str):
    """
    Determines if a molecule is a hydroxy monounsaturated fatty acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a hydroxy monounsaturated fatty acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"

    # Check for hydroxyl groups (excluding the one in carboxylic acid)
    hydroxyl_pattern = Chem.MolFromSmarts('[CX4][OH]')
    hydroxy_matches = mol.GetSubstructMatches(hydroxyl_pattern)
    if not hydroxy_matches:
        return False, "No hydroxyl groups found"

    # Check for double bonds
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    double_bond_matches = mol.GetSubstructMatches(double_bond_pattern)
    
    if not double_bond_matches:
        return False, "No double bonds found"
    
    if len(double_bond_matches) > 1:
        return False, "More than one double bond found (not monounsaturated)"

    # Check if it's a fatty acid by verifying chain length (at least 4 carbons)
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count < 4:
        return False, "Chain too short to be a fatty acid"

    # Count number of hydroxyl groups
    num_hydroxy = len(hydroxy_matches)
    
    # Get stereochemistry of double bond if present
    double_bond = mol.GetBondBetweenAtoms(double_bond_matches[0][0], double_bond_matches[0][1])
    stereo = "E" if double_bond.GetStereo() == Chem.BondStereo.STEREOE else "Z" if double_bond.GetStereo() == Chem.BondStereo.STEREOZ else "unspecified"

    return True, f"Hydroxy monounsaturated fatty acid with {num_hydroxy} hydroxyl group(s) and {stereo} double bond"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131869',
                          'name': 'hydroxy monounsaturated fatty acid',
                          'definition': 'Any monounsaturated fatty acid '
                                        'carrying one or more hydroxy '
                                        'substituents.',
                          'parents': ['CHEBI:24654', 'CHEBI:25413']},
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
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 6404,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.9846366569365494}