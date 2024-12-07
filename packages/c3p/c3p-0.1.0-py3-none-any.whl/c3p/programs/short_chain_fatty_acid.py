"""
Classifies: CHEBI:26666 short-chain fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_short_chain_fatty_acid(smiles: str):
    """
    Determines if a molecule is a short-chain fatty acid (aliphatic monocarboxylic acid with <6 carbons).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a short-chain fatty acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Check for exactly one carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)O')
    matches = mol.GetSubstructMatches(carboxylic_pattern)
    if len(matches) == 0:
        return False, "No carboxylic acid group found"
    if len(matches) > 1:
        return False, "Multiple carboxylic acid groups found"

    # Count total carbons
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count > 5:
        return False, f"Carbon chain too long ({carbon_count} carbons)"

    # Check if aliphatic (no aromatic rings)
    if any(atom.GetIsAromatic() for atom in mol.GetAtoms()):
        return False, "Contains aromatic rings"

    # Check for non-hydrocarbon substituents (besides the carboxylic acid group)
    allowed_atoms = {'C', 'H', 'O'}
    for atom in mol.GetAtoms():
        if atom.GetSymbol() not in allowed_atoms:
            return False, f"Contains non-hydrocarbon substituent ({atom.GetSymbol()})"

    # Count oxygen atoms - should only be 2 from carboxylic acid group
    oxygen_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    if oxygen_count > 2:
        return False, "Contains additional oxygen substituents"

    # All checks passed
    return True, f"Valid short-chain fatty acid with {carbon_count} carbons"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26666',
                          'name': 'short-chain fatty acid',
                          'definition': 'An aliphatic monocarboxylic acid with '
                                        'a chain length of less than C6. If '
                                        'any non-hydrocarbon substituent is '
                                        'present, the compound is not normally '
                                        'regarded as a short-chain fatty acid.',
                          'parents': ['CHEBI:35366']},
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
    'num_true_positives': 1,
    'num_false_positives': 78,
    'num_true_negatives': 183804,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.012658227848101266,
    'recall': 0.2,
    'f1': 0.023809523809523808,
    'accuracy': 0.9995540739693398}