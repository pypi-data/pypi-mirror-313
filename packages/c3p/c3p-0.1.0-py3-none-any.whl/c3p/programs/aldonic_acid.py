"""
Classifies: CHEBI:22301 aldonic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.MolStandardize import rdMolStandardize

def is_aldonic_acid(smiles: str):
    """
    Determines if a molecule is an aldonic acid - a carbohydrate acid formed by oxidizing 
    the aldehyde group of an aldose to a carboxylic acid.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is an aldonic acid, False otherwise
        str: Reason for classification
    """
    # Standardize the molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
        
    # Check for carboxylic acid group
    carboxylic_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_pattern):
        return False, "No carboxylic acid group found"
        
    # Count number of hydroxyl groups
    hydroxyl_pattern = Chem.MolFromSmarts('[CH]O')
    hydroxyl_matches = len(mol.GetSubstructMatches(hydroxyl_pattern))
    
    terminal_hydroxyl = Chem.MolFromSmarts('CO')
    terminal_matches = len(mol.GetSubstructMatches(terminal_hydroxyl))
    
    total_hydroxyls = hydroxyl_matches + terminal_matches
    
    if total_hydroxyls < 2:
        return False, "Insufficient hydroxyl groups for aldonic acid"
    
    # Check carbon chain length (should be at least 3)
    carbon_chain = Chem.MolFromSmarts('CCCC')
    if not mol.HasSubstructMatch(carbon_chain):
        return False, "Carbon chain too short for aldonic acid"
        
    # Check for presence of only C, H, O atoms
    allowed_atoms = {'C', 'H', 'O'}
    mol_atoms = {atom.GetSymbol() for atom in mol.GetAtoms()}
    if not mol_atoms.issubset(allowed_atoms):
        return False, f"Contains disallowed atoms: {mol_atoms - allowed_atoms}"
        
    # Check that carbons are sp3 hybridized (except carboxylic carbon)
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            if atom.GetHybridization() not in [Chem.HybridizationType.SP3, Chem.HybridizationType.SP2]:
                return False, "Contains carbons with incorrect hybridization"
    
    # Check for presence of aldehyde groups (shouldn't exist in aldonic acids)
    aldehyde_pattern = Chem.MolFromSmarts('[CH]=O')
    if mol.HasSubstructMatch(aldehyde_pattern):
        return False, "Contains aldehyde group"
        
    # If all checks pass, classify as aldonic acid
    return True, f"Aldonic acid with {total_hydroxyls} hydroxyl groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22301',
                          'name': 'aldonic acid',
                          'definition': 'Any carbohydrate acid formed by '
                                        'oxidising the aldehyde functional '
                                        'group of an aldose to a carboxylic '
                                        'acid functional group. Aldonic acids '
                                        'have the general formula '
                                        'HOCH2[CH(OH)]nC(=O)OH.',
                          'parents': ['CHEBI:25384', 'CHEBI:33720']},
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
    'num_false_positives': 100,
    'num_true_negatives': 2346,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.9592003263973888}