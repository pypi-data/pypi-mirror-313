"""
Classifies: CHEBI:25633 octadecatrienoic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_octadecatrienoic_acid(smiles: str):
    """
    Determines if a molecule is an octadecatrienoic acid (C18 fatty acid with 3 double bonds).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an octadecatrienoic acid, False otherwise 
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"
        
    # Count carbon atoms
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count != 18:
        return False, f"Contains {carbon_count} carbons, not 18"

    # Count double bonds (excluding carboxylic acid)
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    double_bonds = len(mol.GetSubstructMatches(double_bond_pattern))
    
    if double_bonds != 3:
        return False, f"Contains {double_bonds} double bonds, not 3"

    # All checks passed
    return True, "Contains 18 carbons and 3 double bonds with carboxylic acid group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25633',
                          'name': 'octadecatrienoic acid',
                          'definition': 'Any trienoic fatty acid having '
                                        'eighteen carbons.',
                          'parents': [   'CHEBI:132502',
                                         'CHEBI:15904',
                                         'CHEBI:59202']},
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
    'num_true_positives': 5,
    'num_false_positives': 72,
    'num_true_negatives': 183795,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.06493506493506493,
    'recall': 0.8333333333333334,
    'f1': 0.12048192771084336,
    'accuracy': 0.9996029868441805}