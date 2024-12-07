"""
Classifies: CHEBI:26667 sialic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_sialic_acid(smiles: str):
    """
    Determines if a molecule is a sialic acid (N-acylneuraminic acid or derivative).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a sialic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"

    # Core structure requirements:
    # - 9 carbons 
    # - N-acyl group
    # - Carboxylic acid or derivative
    # - Multiple hydroxyl groups
    # - Pyranose ring
    
    # Count carbons
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count != 9:
        return False, "Does not contain 9 carbons characteristic of sialic acid core"
        
    # Check for N-acyl group
    pattern_nacyl = Chem.MolFromSmarts('[NH][C](=O)')
    if not mol.HasSubstructMatch(pattern_nacyl):
        return False, "Missing N-acyl group"
        
    # Check for carboxylic acid or derivative
    pattern_acid = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
    pattern_ester = Chem.MolFromSmarts('[CX3](=O)[OX2][C]')
    if not (mol.HasSubstructMatch(pattern_acid) or mol.HasSubstructMatch(pattern_ester)):
        return False, "Missing carboxylic acid or derivative group"
        
    # Count hydroxyl groups (should have multiple)
    pattern_oh = Chem.MolFromSmarts('[OH]')
    oh_matches = len(mol.GetSubstructMatches(pattern_oh))
    if oh_matches < 3:
        return False, "Insufficient hydroxyl groups"
        
    # Check for pyranose ring
    pattern_pyranose = Chem.MolFromSmarts('O1CCCCC1')
    if not mol.HasSubstructMatch(pattern_pyranose):
        return False, "Missing pyranose ring"

    # If all requirements are met
    return True, "Contains characteristic sialic acid structural features: 9 carbons, N-acyl group, carboxylic acid/derivative, multiple hydroxyls, and pyranose ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26667',
                          'name': 'sialic acid',
                          'definition': 'Any of the N-acylneuraminic acids and '
                                        'their esters and other derivatives of '
                                        'the alcoholic hydroxy groups.',
                          'parents': ['CHEBI:25508']},
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
    'num_false_positives': 2,
    'num_true_negatives': 183911,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999782508223908}