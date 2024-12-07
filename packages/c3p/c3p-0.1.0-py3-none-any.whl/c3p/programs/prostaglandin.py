"""
Classifies: CHEBI:26333 prostaglandin
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

def is_prostaglandin(smiles: str):
    """
    Determines if a molecule is a prostaglandin based on structural features.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a prostaglandin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Check carbon count - should be C20 or close
    formula = CalcMolFormula(mol)
    carbon_count = sum(1 for c in formula if c == 'C')
    if carbon_count < 18 or carbon_count > 22:
        return False, f"Carbon count {carbon_count} outside typical range for prostaglandins (18-22)"

    # Check for carboxylic acid group
    carboxylic_acid_pattern = Chem.MolFromSmarts('C(=O)[OH]')
    if not mol.HasSubstructMatch(carboxylic_acid_pattern):
        return False, "Missing carboxylic acid group characteristic of prostaglandins"

    # Check for cyclopentane ring
    cyclopentane_pattern = Chem.MolFromSmarts('C1CCCC1')
    if not mol.HasSubstructMatch(cyclopentane_pattern):
        return False, "Missing cyclopentane ring characteristic of prostaglandins"

    # Check for hydroxyl groups (most prostaglandins have at least one)
    hydroxyl_pattern = Chem.MolFromSmarts('[OH]')
    if not mol.HasSubstructMatch(hydroxyl_pattern):
        return False, "Missing hydroxyl groups typically found in prostaglandins"

    # Check for alkene groups (most prostaglandins have at least one)
    alkene_pattern = Chem.MolFromSmarts('C=C')
    if not mol.HasSubstructMatch(alkene_pattern):
        return False, "Missing alkene groups typically found in prostaglandins"

    # If all basic structural features are present, classify as prostaglandin
    features = []
    if mol.HasSubstructMatch(Chem.MolFromSmarts('C(=O)[OH]')):
        features.append("carboxylic acid")
    if mol.HasSubstructMatch(Chem.MolFromSmarts('C1CCCC1')):
        features.append("cyclopentane ring")
    if mol.HasSubstructMatch(Chem.MolFromSmarts('[OH]')):
        num_hydroxyls = len(mol.GetSubstructMatches(hydroxyl_pattern))
        features.append(f"{num_hydroxyls} hydroxyl groups")
    if mol.HasSubstructMatch(Chem.MolFromSmarts('C=C')):
        num_alkenes = len(mol.GetSubstructMatches(alkene_pattern))
        features.append(f"{num_alkenes} alkene groups")
        
    return True, f"Prostaglandin with {', '.join(features)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26333',
                          'name': 'prostaglandin',
                          'definition': 'Naturally occurring compounds derived '
                                        'from the parent C20 acid, prostanoic '
                                        'acid.',
                          'parents': ['CHEBI:26347']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183841,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999510470492249}