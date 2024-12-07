"""
Classifies: CHEBI:22798 beta-D-glucoside
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_beta_D_glucoside(smiles: str):
    """
    Determines if a molecule is a beta-D-glucoside.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a beta-D-glucoside, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string"
        
    # Look for beta-D-glucose substructure
    glucose_pattern = Chem.MolFromSmarts('[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O')
    if not mol.HasSubstructMatch(glucose_pattern):
        return False, "No beta-D-glucose moiety found"
        
    # Check if it's a glycoside (connected via O-glycosidic bond)
    matches = mol.GetSubstructMatches(glucose_pattern)
    for match in matches:
        glucose_atoms = set(match)
        # Get the anomeric carbon (C1)
        anomeric_carbon = mol.GetAtomWithIdx(match[1]) 
        
        # Check its neighbors
        for neighbor in anomeric_carbon.GetNeighbors():
            if neighbor.GetIdx() not in glucose_atoms and neighbor.GetSymbol() == 'O':
                # Found O-glycosidic bond
                return True, "Contains beta-D-glucose moiety with O-glycosidic bond"
                
    return False, "Contains beta-D-glucose but no O-glycosidic bond found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22798',
                          'name': 'beta-D-glucoside',
                          'definition': 'Any D-glucoside in which the anomeric '
                                        'centre has beta-configuration.',
                          'parents': ['CHEBI:35436', 'CHEBI:60980']},
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
    'num_true_negatives': 183230,
    'num_false_negatives': 74,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9995962990442107}