"""
Classifies: CHEBI:24302 glucosiduronic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_glucosiduronic_acid(smiles: str):
    """
    Determines if a molecule is a glucosiduronic acid (contains glucuronic acid linked via glycosidic bond).
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if molecule is a glucosiduronic acid, False otherwise
        str: Reason for classification
    """
    
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # SMARTS pattern for glucuronic acid core with glycosidic bond
    # Matches a pyranose ring with carboxylic acid and OH groups in glucuronic acid configuration
    # connected via an oxygen to another carbon (glycosidic bond)
    glucuronic_pattern = Chem.MolFromSmarts('[OX2]([#6])[C@@H]1O[C@@H]([C@@H](O)[C@H](O)[C@H]1O)C(=O)O')
    
    if not mol.HasSubstructMatch(glucuronic_pattern):
        return False, "No glucuronic acid core with glycosidic linkage found"
    
    # Count matches
    matches = len(mol.GetSubstructMatches(glucuronic_pattern))
    
    if matches >= 1:
        if matches == 1:
            return True, "Contains one glucuronic acid moiety with glycosidic linkage"
        else:
            return True, f"Contains {matches} glucuronic acid moieties with glycosidic linkages"
            
    return False, "Structure does not match glucosiduronic acid pattern"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24302',
                          'name': 'glucosiduronic acid',
                          'definition': 'Any substance produced by linking '
                                        'glucuronic acid to another substance '
                                        'via a glycosidic bond.',
                          'parents': ['CHEBI:35314', 'CHEBI:63436']},
    'config': {   'llm_model_name': 'lbl/claude-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: cannot import name 'rdDecomposition' from "
               "'rdkit.Chem' "
               '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/__init__.py)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 46,
    'num_false_positives': 100,
    'num_true_negatives': 16901,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.3150684931506849,
    'recall': 0.9787234042553191,
    'f1': 0.47668393782383417,
    'accuracy': 0.9940755513843266}